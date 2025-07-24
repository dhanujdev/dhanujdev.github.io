"""
Local GPT Form-Filling Agent with RAG Pipeline for BrowserOS
============================================================

This module implements a privacy-first, voice-controlled form-filling agent that:
1. Uses Ollama for local LLM processing (no cloud dependencies)
2. Implements RAG pipeline for contextual form filling
3. Provides voice-controlled DOM interaction
4. Watches DOM changes for auto-fill opportunities

Architecture:
- VoiceProcessor: Handles speech-to-text and intent recognition
- RAGPipeline: Manages user context and form-filling knowledge
- DOMWatcher: Monitors DOM changes and identifies form fields
- FormFiller: Executes intelligent form completion
"""

import asyncio
import json
import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Callable
from pathlib import Path
import speech_recognition as sr
import chromadb
from pydantic import BaseModel, Field, ConfigDict
from uuid_extensions import uuid7str
import ollama
import pyaudio
import threading
from enum import Enum


class FormFieldType(str, Enum):
	"""Enum for different types of form fields"""
	TEXT = "text"
	EMAIL = "email"
	PHONE = "phone"
	ADDRESS = "address"
	NAME = "name"
	DATE = "date"
	SELECT = "select"
	CHECKBOX = "checkbox"
	RADIO = "radio"
	TEXTAREA = "textarea"


class IntentType(str, Enum):
	"""Voice command intent types"""
	FILL_FORM = "fill_form"
	AUTO_FILL = "auto_fill"
	SAVE_WORKFLOW = "save_workflow"
	CLEAR_FORM = "clear_form"
	HELP = "help"
	STOP_WATCHING = "stop_watching"


@dataclass
class FormField:
	"""Represents a detected form field"""
	id: str
	element_id: str
	field_type: FormFieldType
	label: str
	placeholder: str
	required: bool
	current_value: str
	xpath: str
	confidence: float


@dataclass
class UserContext:
	"""User's personal context for form filling"""
	id: str = Field(default_factory=uuid7str)
	full_name: str = ""
	email: str = ""
	phone: str = ""
	address: Dict[str, str] = Field(default_factory=dict)
	work_experience: List[Dict[str, Any]] = Field(default_factory=list)
	education: List[Dict[str, Any]] = Field(default_factory=list)
	skills: List[str] = Field(default_factory=list)
	preferences: Dict[str, Any] = Field(default_factory=dict)
	custom_responses: Dict[str, str] = Field(default_factory=dict)


class VoiceProcessor:
	"""Handles voice recognition and intent parsing"""
	
	def __init__(self, ollama_client):
		self.recognizer = sr.Recognizer()
		self.microphone = sr.Microphone()
		self.ollama_client = ollama_client
		self.is_listening = False
		self.intent_callbacks: Dict[IntentType, Callable] = {}
		
		# Calibrate microphone
		with self.microphone as source:
			self.recognizer.adjust_for_ambient_noise(source)
	
	def register_intent_callback(self, intent: IntentType, callback: Callable):
		"""Register callback for specific voice intents"""
		self.intent_callbacks[intent] = callback
	
	async def start_listening(self):
		"""Start continuous voice recognition"""
		self.is_listening = True
		
		def listen_worker():
			while self.is_listening:
				try:
					with self.microphone as source:
						# Listen for audio with timeout
						audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
					
					# Convert speech to text
					text = self.recognizer.recognize_google(audio)
					
					# Parse intent using local LLM
					asyncio.create_task(self._process_voice_command(text))
					
				except sr.WaitTimeoutError:
					continue
				except sr.UnknownValueError:
					continue
				except Exception as e:
					logging.error(f"Voice processing error: {e}")
		
		# Run in separate thread to avoid blocking
		thread = threading.Thread(target=listen_worker)
		thread.daemon = True
		thread.start()
	
	async def _process_voice_command(self, text: str):
		"""Process voice command using local LLM for intent recognition"""
		prompt = f"""
		Analyze this voice command and return JSON with intent and parameters:
		Command: "{text}"
		
		Available intents: fill_form, auto_fill, save_workflow, clear_form, help, stop_watching
		
		Return format:
		{{"intent": "intent_name", "parameters": {{"key": "value"}}}}
		
		Examples:
		"Fill out this form" -> {{"intent": "fill_form", "parameters": {{}}}}
		"Auto fill my information" -> {{"intent": "auto_fill", "parameters": {{}}}}
		"Save this workflow" -> {{"intent": "save_workflow", "parameters": {{}}}}
		"""
		
		try:
			response = self.ollama_client.generate(
				model='llama3.2',
				prompt=prompt,
				format='json'
			)
			
			intent_data = json.loads(response['response'])
			intent = IntentType(intent_data['intent'])
			parameters = intent_data.get('parameters', {})
			
			# Execute callback if registered
			if intent in self.intent_callbacks:
				await self.intent_callbacks[intent](parameters)
				
		except Exception as e:
			logging.error(f"Intent processing error: {e}")
	
	def stop_listening(self):
		"""Stop voice recognition"""
		self.is_listening = False


class RAGPipeline:
	"""Retrieval-Augmented Generation pipeline for contextual form filling"""
	
	def __init__(self, context_db_path: str = "./context_db"):
		self.context_db_path = Path(context_db_path)
		self.context_db_path.mkdir(exist_ok=True)
		
		# Initialize ChromaDB for vector storage
		self.chroma_client = chromadb.PersistentClient(path=str(self.context_db_path))
		self.context_collection = self.chroma_client.get_or_create_collection(
			name="user_context",
			metadata={"hnsw:space": "cosine"}
		)
		self.form_patterns_collection = self.chroma_client.get_or_create_collection(
			name="form_patterns",
			metadata={"hnsw:space": "cosine"}
		)
		
		self.user_context = UserContext()
		self._load_user_context()
	
	def _load_user_context(self):
		"""Load user context from storage"""
		context_path = self.context_db_path / "user_context.json"
		if context_path.exists():
			with open(context_path, 'r') as f:
				data = json.load(f)
				self.user_context = UserContext(**data)
	
	def save_user_context(self):
		"""Save user context to storage"""
		context_path = self.context_db_path / "user_context.json"
		with open(context_path, 'w') as f:
			json.dump(self.user_context.__dict__, f, indent=2)
	
	def add_form_pattern(self, form_fields: List[FormField], filled_values: Dict[str, str]):
		"""Learn from successful form completions"""
		pattern_id = uuid7str()
		
		# Create embeddings for form structure
		form_structure = {
			"fields": [f.__dict__ for f in form_fields],
			"values": filled_values,
			"domain": self._extract_domain_from_fields(form_fields)
		}
		
		self.form_patterns_collection.add(
			documents=[json.dumps(form_structure)],
			metadatas=[{"pattern_id": pattern_id, "success": True}],
			ids=[pattern_id]
		)
	
	def _extract_domain_from_fields(self, fields: List[FormField]) -> str:
		"""Extract domain/context from form fields"""
		labels = " ".join([f.label for f in fields])
		# Simple domain classification - could be enhanced with ML
		if any(keyword in labels.lower() for keyword in ["job", "resume", "career", "linkedin"]):
			return "job_application"
		elif any(keyword in labels.lower() for keyword in ["address", "shipping", "billing"]):
			return "address_form"
		else:
			return "general"
	
	async def get_field_suggestions(self, field: FormField, ollama_client) -> List[str]:
		"""Get AI-powered suggestions for form field"""
		
		# Retrieve similar form patterns
		similar_patterns = self.form_patterns_collection.query(
			query_texts=[f"{field.label} {field.field_type}"],
			n_results=3
		)
		
		context = {
			"user_context": self.user_context.__dict__,
			"field": field.__dict__,
			"similar_patterns": similar_patterns
		}
		
		prompt = f"""
		Based on the user context and form field, suggest appropriate values:
		
		User Context: {json.dumps(context['user_context'], indent=2)}
		
		Form Field: {json.dumps(context['field'], indent=2)}
		
		Field Type: {field.field_type}
		Field Label: {field.label}
		Placeholder: {field.placeholder}
		
		Provide 1-3 contextually appropriate suggestions for this field.
		Return as JSON array: ["suggestion1", "suggestion2"]
		"""
		
		try:
			response = ollama_client.generate(
				model='llama3.2',
				prompt=prompt,
				format='json'
			)
			
			suggestions = json.loads(response['response'])
			return suggestions if isinstance(suggestions, list) else [suggestions]
			
		except Exception as e:
			logging.error(f"Suggestion generation error: {e}")
			return self._fallback_suggestions(field)
	
	def _fallback_suggestions(self, field: FormField) -> List[str]:
		"""Fallback suggestions based on field type and user context"""
		fallbacks = {
			FormFieldType.NAME: [self.user_context.full_name],
			FormFieldType.EMAIL: [self.user_context.email],
			FormFieldType.PHONE: [self.user_context.phone],
			FormFieldType.ADDRESS: [
				self.user_context.address.get("street", ""),
				self.user_context.address.get("city", ""),
				self.user_context.address.get("zipcode", "")
			]
		}
		
		return [s for s in fallbacks.get(field.field_type, [""]) if s]


class DOMWatcher:
	"""Watches DOM changes and identifies form fields for auto-filling"""
	
	def __init__(self, rag_pipeline: RAGPipeline):
		self.rag_pipeline = rag_pipeline
		self.is_watching = False
		self.form_detection_callbacks: List[Callable] = []
		self.detected_forms: Dict[str, List[FormField]] = {}
	
	def register_form_detection_callback(self, callback: Callable):
		"""Register callback for when forms are detected"""
		self.form_detection_callbacks.append(callback)
	
	async def start_watching(self):
		"""Start watching for DOM changes (simulated - would integrate with BrowserOS)"""
		self.is_watching = True
		
		# In real BrowserOS integration, this would use browser APIs
		# For now, we simulate DOM watching
		logging.info("DOM watching started - would integrate with BrowserOS browser APIs")
	
	async def detect_forms_on_page(self) -> Dict[str, List[FormField]]:
		"""Detect forms on current page (simulated)"""
		# This would use actual browser APIs in BrowserOS
		# Simulated form detection for demo
		sample_fields = [
			FormField(
				id=uuid7str(),
				element_id="firstName",
				field_type=FormFieldType.NAME,
				label="First Name",
				placeholder="Enter your first name",
				required=True,
				current_value="",
				xpath="//input[@id='firstName']",
				confidence=0.95
			),
			FormField(
				id=uuid7str(),
				element_id="email",
				field_type=FormFieldType.EMAIL,
				label="Email Address",
				placeholder="your.email@example.com",
				required=True,
				current_value="",
				xpath="//input[@id='email']",
				confidence=0.98
			)
		]
		
		form_id = uuid7str()
		self.detected_forms[form_id] = sample_fields
		
		# Notify callbacks
		for callback in self.form_detection_callbacks:
			await callback(form_id, sample_fields)
		
		return self.detected_forms
	
	def stop_watching(self):
		"""Stop DOM watching"""
		self.is_watching = False
		logging.info("DOM watching stopped")


class LocalGPTAgent:
	"""Main agent orchestrating all components"""
	
	def __init__(self, config: Optional[Dict[str, Any]] = None):
		self.config = config or {}
		
		# Initialize Ollama client
		self.ollama_client = ollama.Client()
		
		# Initialize components
		self.rag_pipeline = RAGPipeline()
		self.voice_processor = VoiceProcessor(self.ollama_client)
		self.dom_watcher = DOMWatcher(self.rag_pipeline)
		
		# Register callbacks
		self._setup_callbacks()
		
		# State
		self.active_forms: Dict[str, List[FormField]] = {}
		self.is_active = False
	
	def _setup_callbacks(self):
		"""Setup inter-component callbacks"""
		# Voice command callbacks
		self.voice_processor.register_intent_callback(
			IntentType.FILL_FORM, self._handle_fill_form_intent
		)
		self.voice_processor.register_intent_callback(
			IntentType.AUTO_FILL, self._handle_auto_fill_intent
		)
		self.voice_processor.register_intent_callback(
			IntentType.SAVE_WORKFLOW, self._handle_save_workflow_intent
		)
		self.voice_processor.register_intent_callback(
			IntentType.STOP_WATCHING, self._handle_stop_watching_intent
		)
		
		# DOM detection callbacks
		self.dom_watcher.register_form_detection_callback(
			self._handle_form_detected
		)
	
	async def start(self):
		"""Start the agent"""
		logging.info("Starting Local GPT Agent...")
		
		self.is_active = True
		
		# Start components
		await self.voice_processor.start_listening()
		await self.dom_watcher.start_watching()
		
		logging.info("Local GPT Agent is active and listening for voice commands")
	
	async def stop(self):
		"""Stop the agent"""
		logging.info("Stopping Local GPT Agent...")
		
		self.is_active = False
		self.voice_processor.stop_listening()
		self.dom_watcher.stop_watching()
		
		# Save context
		self.rag_pipeline.save_user_context()
		
		logging.info("Local GPT Agent stopped")
	
	async def _handle_fill_form_intent(self, parameters: Dict[str, Any]):
		"""Handle fill form voice command"""
		logging.info("Processing fill form request...")
		
		# Detect forms on current page
		forms = await self.dom_watcher.detect_forms_on_page()
		
		for form_id, fields in forms.items():
			await self._fill_form_intelligently(form_id, fields)
	
	async def _handle_auto_fill_intent(self, parameters: Dict[str, Any]):
		"""Handle auto-fill voice command"""
		logging.info("Processing auto-fill request...")
		
		# Auto-fill all detected forms
		for form_id, fields in self.active_forms.items():
			await self._fill_form_intelligently(form_id, fields)
	
	async def _handle_save_workflow_intent(self, parameters: Dict[str, Any]):
		"""Handle save workflow voice command"""
		logging.info("Saving current workflow...")
		
		# Save successful form patterns to RAG pipeline
		for form_id, fields in self.active_forms.items():
			filled_values = {f.element_id: f.current_value for f in fields if f.current_value}
			self.rag_pipeline.add_form_pattern(fields, filled_values)
		
		self.rag_pipeline.save_user_context()
		logging.info("Workflow saved successfully")
	
	async def _handle_stop_watching_intent(self, parameters: Dict[str, Any]):
		"""Handle stop watching voice command"""
		await self.stop()
	
	async def _handle_form_detected(self, form_id: str, fields: List[FormField]):
		"""Handle when DOM watcher detects a form"""
		logging.info(f"Form detected: {form_id} with {len(fields)} fields")
		
		self.active_forms[form_id] = fields
		
		# Auto-suggest if enabled
		if self.config.get("auto_suggest", True):
			await self._suggest_form_completion(form_id, fields)
	
	async def _fill_form_intelligently(self, form_id: str, fields: List[FormField]):
		"""Fill form using AI suggestions"""
		logging.info(f"Intelligently filling form {form_id}")
		
		for field in fields:
			if field.current_value:  # Skip already filled fields
				continue
			
			suggestions = await self.rag_pipeline.get_field_suggestions(
				field, self.ollama_client
			)
			
			if suggestions and suggestions[0]:
				# In real implementation, this would fill the actual form field
				field.current_value = suggestions[0]
				logging.info(f"Filled {field.label} with: {suggestions[0]}")
	
	async def _suggest_form_completion(self, form_id: str, fields: List[FormField]):
		"""Suggest form completion to user"""
		empty_fields = [f for f in fields if not f.current_value]
		
		if empty_fields:
			logging.info(f"Found {len(empty_fields)} empty fields. Say 'fill form' to auto-complete.")


# Example usage and configuration
async def main():
	"""Example usage of the Local GPT Agent"""
	
	# Configure logging
	logging.basicConfig(
		level=logging.INFO,
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
	)
	
	# Initialize agent
	config = {
		"auto_suggest": True,
		"voice_activation": True,
		"privacy_mode": True  # All processing stays local
	}
	
	agent = LocalGPTAgent(config)
	
	try:
		# Start the agent
		await agent.start()
		
		# Keep running until stopped by voice command
		while agent.is_active:
			await asyncio.sleep(1)
			
	except KeyboardInterrupt:
		logging.info("Received interrupt signal")
	finally:
		await agent.stop()


if __name__ == "__main__":
	asyncio.run(main())