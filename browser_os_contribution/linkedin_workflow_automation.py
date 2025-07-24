"""
LinkedIn Easy Apply Workflow Automation System
==============================================

This module implements intelligent LinkedIn Easy Apply automation that:
1. Detects LinkedIn job pages and Easy Apply buttons
2. Creates reusable workflows for job applications
3. Handles dynamic form fields and screening questions
4. Integrates with the Local GPT Agent for intelligent responses
5. Maintains compliance with LinkedIn's terms while being respectful

Architecture:
- LinkedInDetector: Identifies LinkedIn job pages and Easy Apply opportunities
- WorkflowEngine: Records, saves, and replays application workflows
- ScreeningHandler: Handles screening questions intelligently
- ApplicationTracker: Tracks application status and history
"""

import asyncio
import json
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Callable
from pathlib import Path
from datetime import datetime, timedelta
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict
from uuid_extensions import uuid7str
import hashlib
from local_gpt_agent import LocalGPTAgent, FormField, FormFieldType, RAGPipeline


class ApplicationStatus(str, Enum):
	"""Status of job applications"""
	PENDING = "pending"
	IN_PROGRESS = "in_progress"
	SUBMITTED = "submitted"
	REJECTED = "rejected"
	INTERVIEW = "interview"
	OFFER = "offer"
	WITHDRAWN = "withdrawn"


class WorkflowStepType(str, Enum):
	"""Types of workflow steps"""
	CLICK = "click"
	FILL_FORM = "fill_form"
	SELECT_OPTION = "select_option"
	UPLOAD_FILE = "upload_file"
	WAIT = "wait"
	VERIFY = "verify"
	SCREENING_QUESTION = "screening_question"


@dataclass
class WorkflowStep:
	"""Individual step in a workflow"""
	id: str = field(default_factory=uuid7str)
	step_type: WorkflowStepType = WorkflowStepType.CLICK
	selector: str = ""
	action: str = ""
	value: str = ""
	description: str = ""
	required: bool = True
	retry_count: int = 0
	max_retries: int = 3
	delay_after: float = 1.0
	conditions: Dict[str, Any] = field(default_factory=dict)


@dataclass
class JobPosting:
	"""LinkedIn job posting information"""
	id: str = field(default_factory=uuid7str)
	job_id: str = ""
	title: str = ""
	company: str = ""
	location: str = ""
	url: str = ""
	description: str = ""
	requirements: List[str] = field(default_factory=list)
	salary_range: str = ""
	job_type: str = ""
	experience_level: str = ""
	posted_date: datetime = field(default_factory=datetime.now)
	easy_apply_available: bool = False
	application_deadline: Optional[datetime] = None


@dataclass
class ApplicationRecord:
	"""Record of a job application"""
	id: str = field(default_factory=uuid7str)
	job_posting: JobPosting = field(default_factory=JobPosting)
	status: ApplicationStatus = ApplicationStatus.PENDING
	applied_date: datetime = field(default_factory=datetime.now)
	workflow_used: str = ""
	screening_responses: Dict[str, str] = field(default_factory=dict)
	cover_letter: str = ""
	resume_used: str = ""
	notes: str = ""
	follow_up_dates: List[datetime] = field(default_factory=list)


@dataclass
class WorkflowTemplate:
	"""Reusable workflow for similar job applications"""
	id: str = field(default_factory=uuid7str)
	name: str = ""
	description: str = ""
	company_pattern: str = ""
	job_type_pattern: str = ""
	steps: List[WorkflowStep] = field(default_factory=list)
	success_rate: float = 0.0
	usage_count: int = 0
	created_date: datetime = field(default_factory=datetime.now)
	last_updated: datetime = field(default_factory=datetime.now)
	tags: List[str] = field(default_factory=list)


class LinkedInDetector:
	"""Detects LinkedIn pages and Easy Apply opportunities"""
	
	def __init__(self):
		self.linkedin_patterns = {
			"job_page": r"linkedin\.com/jobs/view/(\d+)",
			"easy_apply_button": ".jobs-apply-button--top-card",
			"job_title": ".top-card-layout__title",
			"company_name": ".top-card-layout__card .app-aware-link",
			"job_location": ".top-card-layout__second-subline",
			"job_description": ".description__text"
		}
		
		self.detected_jobs: Dict[str, JobPosting] = {}
	
	async def is_linkedin_job_page(self, url: str) -> bool:
		"""Check if current page is a LinkedIn job posting"""
		import re
		return bool(re.search(self.linkedin_patterns["job_page"], url))
	
	async def detect_easy_apply_opportunity(self) -> List[JobPosting]:
		"""Detect Easy Apply opportunities on current page"""
		# In real implementation, this would use browser APIs
		# For demonstration, we simulate detection
		
		sample_job = JobPosting(
			job_id="3456789012",
			title="Senior Software Engineer",
			company="Tech Innovators Inc.",
			location="San Francisco, CA",
			url="https://linkedin.com/jobs/view/3456789012",
			description="We are looking for a senior software engineer...",
			requirements=["Python", "JavaScript", "React", "Node.js"],
			salary_range="$120k - $180k",
			job_type="Full-time",
			experience_level="Senior level",
			easy_apply_available=True
		)
		
		job_hash = self._generate_job_hash(sample_job)
		self.detected_jobs[job_hash] = sample_job
		
		logging.info(f"Detected Easy Apply opportunity: {sample_job.title} at {sample_job.company}")
		return [sample_job]
	
	def _generate_job_hash(self, job: JobPosting) -> str:
		"""Generate unique hash for job posting"""
		hash_string = f"{job.company}_{job.title}_{job.location}_{job.job_id}"
		return hashlib.md5(hash_string.encode()).hexdigest()
	
	async def extract_job_details(self, job_url: str) -> JobPosting:
		"""Extract detailed job information from LinkedIn page"""
		# In real implementation, this would scrape the actual page
		# For demonstration, we return sample data
		
		return JobPosting(
			job_id="extracted_123",
			title="Full Stack Developer",
			company="Startup Dynamics",
			location="Remote",
			url=job_url,
			description="Join our fast-growing startup...",
			requirements=["React", "Python", "AWS", "Docker"],
			easy_apply_available=True
		)


class ScreeningHandler:
	"""Handles LinkedIn screening questions intelligently"""
	
	def __init__(self, rag_pipeline: RAGPipeline, ollama_client):
		self.rag_pipeline = rag_pipeline
		self.ollama_client = ollama_client
		self.common_questions = self._load_common_questions()
		self.response_cache: Dict[str, str] = {}
	
	def _load_common_questions(self) -> Dict[str, str]:
		"""Load common screening questions and suggested responses"""
		return {
			"years_experience": "How many years of experience do you have with [technology]?",
			"salary_expectation": "What are your salary expectations?",
			"availability": "When can you start?",
			"work_authorization": "Are you authorized to work in [country]?",
			"relocation": "Are you willing to relocate?",
			"remote_work": "Are you open to remote work?",
			"cover_letter": "Why are you interested in this role?",
			"notice_period": "What is your notice period?",
			"degree_required": "Do you have a degree in [field]?",
			"certification": "Do you have [specific certification]?"
		}
	
	async def handle_screening_question(self, question: str, job_context: JobPosting) -> str:
		"""Generate intelligent response to screening question"""
		
		# Check cache first
		question_hash = hashlib.md5(question.encode()).hexdigest()
		if question_hash in self.response_cache:
			return self.response_cache[question_hash]
		
		# Use RAG pipeline for context-aware response
		user_context = self.rag_pipeline.user_context
		
		prompt = f"""
		You are helping with a LinkedIn job application. Based on the user's context and the job details,
		provide an appropriate, honest, and professional response to this screening question.
		
		Job Context:
		- Title: {job_context.title}
		- Company: {job_context.company}
		- Requirements: {', '.join(job_context.requirements)}
		- Location: {job_context.location}
		
		User Context:
		- Experience: {json.dumps(user_context.work_experience, indent=2)}
		- Skills: {', '.join(user_context.skills)}
		- Location: {user_context.address}
		
		Screening Question: "{question}"
		
		Provide a concise, professional response that is truthful and aligns with the user's background.
		If specific numbers or dates are needed, base them on the user's actual experience.
		Keep the response under 100 words and professional in tone.
		
		Response:
		"""
		
		try:
			response = self.ollama_client.generate(
				model='llama3.2',
				prompt=prompt
			)
			
			answer = response['response'].strip()
			
			# Cache the response
			self.response_cache[question_hash] = answer
			
			return answer
			
		except Exception as e:
			logging.error(f"Error generating screening response: {e}")
			return "I would be happy to discuss this further in an interview."
	
	def classify_question_type(self, question: str) -> str:
		"""Classify the type of screening question"""
		question_lower = question.lower()
		
		if any(word in question_lower for word in ["years", "experience", "long"]):
			return "years_experience"
		elif any(word in question_lower for word in ["salary", "compensation", "pay"]):
			return "salary_expectation"
		elif any(word in question_lower for word in ["start", "available", "when"]):
			return "availability"
		elif any(word in question_lower for word in ["authorized", "eligible", "visa"]):
			return "work_authorization"
		elif any(word in question_lower for word in ["relocate", "move", "location"]):
			return "relocation"
		elif any(word in question_lower for word in ["remote", "work from home"]):
			return "remote_work"
		else:
			return "general"


class WorkflowEngine:
	"""Records, saves, and replays application workflows"""
	
	def __init__(self, storage_path: str = "./workflows"):
		self.storage_path = Path(storage_path)
		self.storage_path.mkdir(exist_ok=True)
		
		self.templates: Dict[str, WorkflowTemplate] = {}
		self.active_workflows: Dict[str, List[WorkflowStep]] = {}
		self.recording_mode = False
		
		self._load_templates()
	
	def _load_templates(self):
		"""Load existing workflow templates"""
		templates_file = self.storage_path / "templates.json"
		if templates_file.exists():
			with open(templates_file, 'r') as f:
				data = json.load(f)
				for template_data in data:
					template = WorkflowTemplate(**template_data)
					self.templates[template.id] = template
	
	def save_templates(self):
		"""Save workflow templates to storage"""
		templates_file = self.storage_path / "templates.json"
		data = [template.__dict__ for template in self.templates.values()]
		
		# Convert datetime objects to strings for JSON serialization
		for template_data in data:
			template_data['created_date'] = template_data['created_date'].isoformat()
			template_data['last_updated'] = template_data['last_updated'].isoformat()
		
		with open(templates_file, 'w') as f:
			json.dump(data, f, indent=2, default=str)
	
	def start_recording_workflow(self, workflow_name: str) -> str:
		"""Start recording a new workflow"""
		workflow_id = uuid7str()
		self.active_workflows[workflow_id] = []
		self.recording_mode = True
		
		logging.info(f"Started recording workflow: {workflow_name}")
		return workflow_id
	
	def record_step(self, workflow_id: str, step: WorkflowStep):
		"""Record a step in the active workflow"""
		if workflow_id in self.active_workflows:
			self.active_workflows[workflow_id].append(step)
			logging.info(f"Recorded step: {step.description}")
	
	def stop_recording_workflow(self, workflow_id: str, name: str, description: str = "") -> WorkflowTemplate:
		"""Stop recording and create a template"""
		if workflow_id not in self.active_workflows:
			raise ValueError(f"No active workflow with id: {workflow_id}")
		
		steps = self.active_workflows[workflow_id]
		template = WorkflowTemplate(
			name=name,
			description=description,
			steps=steps
		)
		
		self.templates[template.id] = template
		del self.active_workflows[workflow_id]
		self.recording_mode = False
		
		self.save_templates()
		logging.info(f"Saved workflow template: {name}")
		return template
	
	async def replay_workflow(self, template_id: str, job_context: JobPosting) -> bool:
		"""Replay a workflow template for a job application"""
		if template_id not in self.templates:
			logging.error(f"Template not found: {template_id}")
			return False
		
		template = self.templates[template_id]
		logging.info(f"Replaying workflow: {template.name}")
		
		success = True
		for step in template.steps:
			try:
				success = await self._execute_step(step, job_context)
				if not success and step.required:
					logging.error(f"Required step failed: {step.description}")
					break
				
				# Wait between steps
				await asyncio.sleep(step.delay_after)
				
			except Exception as e:
				logging.error(f"Error executing step {step.description}: {e}")
				if step.required:
					success = False
					break
		
		# Update template statistics
		template.usage_count += 1
		if success:
			template.success_rate = (template.success_rate * (template.usage_count - 1) + 1) / template.usage_count
		else:
			template.success_rate = (template.success_rate * (template.usage_count - 1)) / template.usage_count
		
		template.last_updated = datetime.now()
		self.save_templates()
		
		return success
	
	async def _execute_step(self, step: WorkflowStep, job_context: JobPosting) -> bool:
		"""Execute a single workflow step"""
		logging.info(f"Executing step: {step.description}")
		
		# In real implementation, this would interact with browser APIs
		# For demonstration, we simulate step execution
		
		if step.step_type == WorkflowStepType.CLICK:
			return await self._simulate_click(step.selector)
		elif step.step_type == WorkflowStepType.FILL_FORM:
			return await self._simulate_form_fill(step.selector, step.value)
		elif step.step_type == WorkflowStepType.SCREENING_QUESTION:
			return await self._handle_screening_step(step, job_context)
		else:
			logging.info(f"Simulated execution of {step.step_type}")
			return True
	
	async def _simulate_click(self, selector: str) -> bool:
		"""Simulate clicking an element"""
		logging.info(f"Clicking element: {selector}")
		await asyncio.sleep(0.5)  # Simulate action delay
		return True
	
	async def _simulate_form_fill(self, selector: str, value: str) -> bool:
		"""Simulate filling a form field"""
		logging.info(f"Filling field {selector} with: {value}")
		await asyncio.sleep(0.5)
		return True
	
	async def _handle_screening_step(self, step: WorkflowStep, job_context: JobPosting) -> bool:
		"""Handle screening question step"""
		# This would integrate with ScreeningHandler
		logging.info(f"Handling screening question: {step.description}")
		return True
	
	def find_matching_templates(self, job: JobPosting) -> List[WorkflowTemplate]:
		"""Find workflow templates that match the job posting"""
		matching = []
		
		for template in self.templates.values():
			# Simple matching logic - could be enhanced with ML
			if template.company_pattern and template.company_pattern.lower() in job.company.lower():
				matching.append(template)
			elif template.job_type_pattern and template.job_type_pattern.lower() in job.job_type.lower():
				matching.append(template)
			elif any(tag.lower() in job.title.lower() for tag in template.tags):
				matching.append(template)
		
		# Sort by success rate
		matching.sort(key=lambda t: t.success_rate, reverse=True)
		return matching


class ApplicationTracker:
	"""Tracks application status and history"""
	
	def __init__(self, storage_path: str = "./applications"):
		self.storage_path = Path(storage_path)
		self.storage_path.mkdir(exist_ok=True)
		
		self.applications: Dict[str, ApplicationRecord] = {}
		self.daily_limits = {
			"max_applications_per_day": 50,  # Respectful limit
			"min_delay_between_applications": 30  # seconds
		}
		
		self._load_applications()
	
	def _load_applications(self):
		"""Load existing application records"""
		apps_file = self.storage_path / "applications.json"
		if apps_file.exists():
			with open(apps_file, 'r') as f:
				data = json.load(f)
				for app_data in data:
					# Convert datetime strings back to datetime objects
					app_data['applied_date'] = datetime.fromisoformat(app_data['applied_date'])
					if app_data.get('application_deadline'):
						app_data['application_deadline'] = datetime.fromisoformat(app_data['application_deadline'])
					
					app = ApplicationRecord(**app_data)
					self.applications[app.id] = app
	
	def save_applications(self):
		"""Save application records to storage"""
		apps_file = self.storage_path / "applications.json"
		data = []
		
		for app in self.applications.values():
			app_data = app.__dict__.copy()
			app_data['applied_date'] = app_data['applied_date'].isoformat()
			if app_data.get('application_deadline'):
				app_data['application_deadline'] = app_data['application_deadline'].isoformat()
			data.append(app_data)
		
		with open(apps_file, 'w') as f:
			json.dump(data, f, indent=2, default=str)
	
	def can_apply_today(self) -> bool:
		"""Check if daily application limit allows more applications"""
		today = datetime.now().date()
		today_applications = [
			app for app in self.applications.values()
			if app.applied_date.date() == today
		]
		
		return len(today_applications) < self.daily_limits["max_applications_per_day"]
	
	def get_last_application_time(self) -> Optional[datetime]:
		"""Get timestamp of last application"""
		if not self.applications:
			return None
		
		return max(app.applied_date for app in self.applications.values())
	
	def should_wait_before_next_application(self) -> bool:
		"""Check if we should wait before next application"""
		last_app_time = self.get_last_application_time()
		if not last_app_time:
			return False
		
		time_since_last = datetime.now() - last_app_time
		min_delay = timedelta(seconds=self.daily_limits["min_delay_between_applications"])
		
		return time_since_last < min_delay
	
	def record_application(self, job: JobPosting, workflow_id: str) -> ApplicationRecord:
		"""Record a new job application"""
		app = ApplicationRecord(
			job_posting=job,
			workflow_used=workflow_id,
			status=ApplicationStatus.SUBMITTED
		)
		
		self.applications[app.id] = app
		self.save_applications()
		
		logging.info(f"Recorded application: {job.title} at {job.company}")
		return app
	
	def update_application_status(self, app_id: str, status: ApplicationStatus, notes: str = ""):
		"""Update application status"""
		if app_id in self.applications:
			self.applications[app_id].status = status
			if notes:
				self.applications[app_id].notes += f"\n{datetime.now()}: {notes}"
			self.save_applications()
	
	def get_applications_summary(self) -> Dict[str, Any]:
		"""Get summary of applications"""
		total = len(self.applications)
		by_status = {}
		
		for app in self.applications.values():
			status = app.status
			by_status[status] = by_status.get(status, 0) + 1
		
		today_count = len([
			app for app in self.applications.values()
			if app.applied_date.date() == datetime.now().date()
		])
		
		return {
			"total_applications": total,
			"applications_by_status": by_status,
			"applications_today": today_count,
			"daily_limit_remaining": self.daily_limits["max_applications_per_day"] - today_count
		}


class LinkedInWorkflowAutomation:
	"""Main orchestrator for LinkedIn Easy Apply automation"""
	
	def __init__(self, gpt_agent: LocalGPTAgent):
		self.gpt_agent = gpt_agent
		self.linkedin_detector = LinkedInDetector()
		self.screening_handler = ScreeningHandler(
			gpt_agent.rag_pipeline, 
			gpt_agent.ollama_client
		)
		self.workflow_engine = WorkflowEngine()
		self.application_tracker = ApplicationTracker()
		
		self.is_active = False
		self.automation_callbacks: List[Callable] = []
	
	def register_automation_callback(self, callback: Callable):
		"""Register callback for automation events"""
		self.automation_callbacks.append(callback)
	
	async def start_automation(self):
		"""Start LinkedIn automation"""
		logging.info("Starting LinkedIn Easy Apply automation...")
		
		self.is_active = True
		
		# Start monitoring for LinkedIn pages
		while self.is_active:
			try:
				await self._check_for_linkedin_opportunities()
				await asyncio.sleep(5)  # Check every 5 seconds
				
			except Exception as e:
				logging.error(f"Error in automation loop: {e}")
				await asyncio.sleep(10)  # Wait longer on error
	
	async def _check_for_linkedin_opportunities(self):
		"""Check current page for LinkedIn Easy Apply opportunities"""
		# In real implementation, this would check the actual browser URL
		current_url = "https://linkedin.com/jobs/view/3456789012"  # Simulated
		
		if await self.linkedin_detector.is_linkedin_job_page(current_url):
			jobs = await self.linkedin_detector.detect_easy_apply_opportunity()
			
			for job in jobs:
				if self._should_apply_to_job(job):
					await self.apply_to_job(job)
	
	def _should_apply_to_job(self, job: JobPosting) -> bool:
		"""Determine if we should apply to this job"""
		# Check daily limits
		if not self.application_tracker.can_apply_today():
			logging.info("Daily application limit reached")
			return False
		
		# Check timing between applications
		if self.application_tracker.should_wait_before_next_application():
			logging.info("Waiting before next application")
			return False
		
		# Check if already applied
		job_hash = hashlib.md5(f"{job.company}_{job.title}".encode()).hexdigest()
		existing_apps = [
			app for app in self.application_tracker.applications.values()
			if hashlib.md5(f"{app.job_posting.company}_{app.job_posting.title}".encode()).hexdigest() == job_hash
		]
		
		if existing_apps:
			logging.info(f"Already applied to {job.title} at {job.company}")
			return False
		
		return True
	
	async def apply_to_job(self, job: JobPosting) -> bool:
		"""Apply to a job using saved workflows"""
		logging.info(f"Applying to: {job.title} at {job.company}")
		
		# Find matching workflow templates
		matching_templates = self.workflow_engine.find_matching_templates(job)
		
		if not matching_templates:
			# No existing workflow, start recording a new one
			logging.info("No matching workflow found, manual application required")
			return await self._manual_application_with_recording(job)
		
		# Use the best matching template
		best_template = matching_templates[0]
		logging.info(f"Using workflow template: {best_template.name}")
		
		# Execute the workflow
		success = await self.workflow_engine.replay_workflow(best_template.id, job)
		
		if success:
			# Record the application
			self.application_tracker.record_application(job, best_template.id)
			
			# Notify callbacks
			for callback in self.automation_callbacks:
				await callback("application_submitted", job, success)
		
		return success
	
	async def _manual_application_with_recording(self, job: JobPosting) -> bool:
		"""Handle manual application while recording for future use"""
		workflow_name = f"{job.company}_{job.job_type}_application"
		workflow_id = self.workflow_engine.start_recording_workflow(workflow_name)
		
		# In real implementation, this would guide the user through manual application
		# while recording each step for future automation
		
		logging.info("Manual application mode - recording steps for future automation")
		
		# Simulate some steps
		steps = [
			WorkflowStep(
				step_type=WorkflowStepType.CLICK,
				selector=".jobs-apply-button",
				description="Click Easy Apply button"
			),
			WorkflowStep(
				step_type=WorkflowStepType.FILL_FORM,
				selector="#resume-upload",
				description="Upload resume",
				value="default_resume.pdf"
			),
			WorkflowStep(
				step_type=WorkflowStepType.SCREENING_QUESTION,
				description="Answer screening questions"
			)
		]
		
		for step in steps:
			self.workflow_engine.record_step(workflow_id, step)
			await asyncio.sleep(1)  # Simulate user interaction time
		
		# Save the workflow template
		template = self.workflow_engine.stop_recording_workflow(
			workflow_id,
			workflow_name,
			f"Workflow for {job.company} {job.job_type} positions"
		)
		
		# Add relevant tags
		template.tags = [job.job_type.lower(), job.company.lower()]
		template.company_pattern = job.company
		template.job_type_pattern = job.job_type
		
		self.workflow_engine.save_templates()
		
		return True
	
	async def save_current_workflow(self, name: str, description: str = ""):
		"""Save current page interaction as a workflow"""
		if not self.workflow_engine.recording_mode:
			logging.error("No active workflow recording")
			return None
		
		# This would be called by voice command or user action
		active_workflow_id = list(self.workflow_engine.active_workflows.keys())[0]
		template = self.workflow_engine.stop_recording_workflow(
			active_workflow_id, name, description
		)
		
		logging.info(f"Saved workflow: {name}")
		return template
	
	def get_automation_summary(self) -> Dict[str, Any]:
		"""Get summary of automation activity"""
		app_summary = self.application_tracker.get_applications_summary()
		workflow_summary = {
			"total_templates": len(self.workflow_engine.templates),
			"average_success_rate": sum(t.success_rate for t in self.workflow_engine.templates.values()) / len(self.workflow_engine.templates) if self.workflow_engine.templates else 0
		}
		
		return {
			"applications": app_summary,
			"workflows": workflow_summary,
			"is_active": self.is_active
		}
	
	def stop_automation(self):
		"""Stop LinkedIn automation"""
		logging.info("Stopping LinkedIn automation...")
		self.is_active = False


# Integration with the main GPT Agent
async def integrate_with_gpt_agent():
	"""Example of integrating LinkedIn automation with the Local GPT Agent"""
	
	# Initialize the Local GPT Agent
	from local_gpt_agent import LocalGPTAgent
	
	gpt_agent = LocalGPTAgent({
		"auto_suggest": True,
		"voice_activation": True,
		"privacy_mode": True
	})
	
	# Initialize LinkedIn automation
	linkedin_automation = LinkedInWorkflowAutomation(gpt_agent)
	
	# Register voice commands for LinkedIn automation
	async def handle_linkedin_automation_intent(parameters: Dict[str, Any]):
		command = parameters.get("command", "")
		
		if "start applying" in command.lower():
			await linkedin_automation.start_automation()
		elif "save workflow" in command.lower():
			await linkedin_automation.save_current_workflow("User Saved Workflow")
		elif "stop automation" in command.lower():
			linkedin_automation.stop_automation()
		elif "application summary" in command.lower():
			summary = linkedin_automation.get_automation_summary()
			logging.info(f"Application Summary: {json.dumps(summary, indent=2)}")
	
	# Start both systems
	await gpt_agent.start()
	
	# Register LinkedIn-specific voice commands
	gpt_agent.voice_processor.register_intent_callback(
		"linkedin_automation", 
		handle_linkedin_automation_intent
	)
	
	return gpt_agent, linkedin_automation


# Example usage
async def main():
	"""Example usage of LinkedIn automation system"""
	
	logging.basicConfig(
		level=logging.INFO,
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
	)
	
	try:
		gpt_agent, linkedin_automation = await integrate_with_gpt_agent()
		
		# Keep running until stopped
		while gpt_agent.is_active:
			await asyncio.sleep(1)
			
	except KeyboardInterrupt:
		logging.info("Received interrupt signal")
	finally:
		if 'gpt_agent' in locals():
			await gpt_agent.stop()
		if 'linkedin_automation' in locals():
			linkedin_automation.stop_automation()


if __name__ == "__main__":
	asyncio.run(main())