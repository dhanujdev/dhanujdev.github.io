"""
BrowserOS Integration Layer
===========================

This module provides the integration layer between the Local GPT Agent,
LinkedIn Automation, and BrowserOS native APIs. It bridges the gap between
our Python-based AI agents and BrowserOS's Chromium-based architecture.

Integration Points:
- Native browser extension interface
- Voice command integration with browser
- DOM manipulation through BrowserOS APIs
- Local AI model management
- Privacy-first data handling
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Callable
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
import subprocess
import sys
import os

from local_gpt_agent import LocalGPTAgent, FormField, FormFieldType
from linkedin_workflow_automation import LinkedInWorkflowAutomation, JobPosting


class BrowserOSAPI:
	"""Interface to BrowserOS native APIs"""
	
	def __init__(self):
		self.extension_path = Path("./browser_extension")
		self.native_host_path = Path("./native_host")
		self.is_connected = False
		self.message_handlers: Dict[str, Callable] = {}
	
	async def initialize(self) -> bool:
		"""Initialize connection to BrowserOS"""
		try:
			# Check if BrowserOS is running
			if not self._is_browseros_running():
				logging.error("BrowserOS is not running. Please start BrowserOS first.")
				return False
			
			# Setup native messaging host
			await self._setup_native_messaging()
			
			# Install browser extension if needed
			await self._install_extension()
			
			self.is_connected = True
			logging.info("Successfully connected to BrowserOS")
			return True
			
		except Exception as e:
			logging.error(f"Failed to initialize BrowserOS connection: {e}")
			return False
	
	def _is_browseros_running(self) -> bool:
		"""Check if BrowserOS process is running"""
		try:
			# Check for BrowserOS process
			import psutil
			for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
				if 'browseros' in proc.info['name'].lower():
					return True
			return False
		except ImportError:
			logging.warning("psutil not available, cannot check BrowserOS status")
			return True  # Assume it's running
	
	async def _setup_native_messaging(self):
		"""Setup native messaging host for browser communication"""
		self.native_host_path.mkdir(exist_ok=True)
		
		# Create native messaging host manifest
		manifest = {
			"name": "com.local_gpt_agent.native_host",
			"description": "Local GPT Agent Native Host",
			"path": str(self.native_host_path / "native_host.py"),
			"type": "stdio",
			"allowed_origins": [
				"chrome-extension://your-extension-id/"
			]
		}
		
		manifest_path = self.native_host_path / "manifest.json"
		with open(manifest_path, 'w') as f:
			json.dump(manifest, f, indent=2)
		
		# Create native host script
		native_host_script = '''#!/usr/bin/env python3
"""
Native messaging host for Local GPT Agent
Handles communication between browser extension and Python agent
"""

import sys
import json
import struct
import asyncio
import logging

class NativeHost:
    def __init__(self):
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(
            filename='/tmp/local_gpt_agent.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def read_message(self):
        """Read message from browser extension"""
        raw_length = sys.stdin.buffer.read(4)
        if len(raw_length) == 0:
            return None
        
        message_length = struct.unpack('@I', raw_length)[0]
        message = sys.stdin.buffer.read(message_length).decode('utf-8')
        return json.loads(message)
    
    def send_message(self, message):
        """Send message to browser extension"""
        encoded_message = json.dumps(message).encode('utf-8')
        sys.stdout.buffer.write(struct.pack('@I', len(encoded_message)))
        sys.stdout.buffer.write(encoded_message)
        sys.stdout.buffer.flush()
    
    def run(self):
        """Main message handling loop"""
        logging.info("Native host started")
        
        while True:
            try:
                message = self.read_message()
                if message is None:
                    break
                
                logging.info(f"Received message: {message}")
                
                # Handle different message types
                response = self.handle_message(message)
                self.send_message(response)
                
            except Exception as e:
                logging.error(f"Error handling message: {e}")
                self.send_message({"error": str(e)})
    
    def handle_message(self, message):
        """Handle incoming messages from extension"""
        msg_type = message.get('type', '')
        
        if msg_type == 'ping':
            return {"type": "pong", "timestamp": message.get('timestamp')}
        elif msg_type == 'detect_forms':
            return self.detect_forms(message.get('data', {}))
        elif msg_type == 'fill_form':
            return self.fill_form(message.get('data', {}))
        elif msg_type == 'voice_command':
            return self.handle_voice_command(message.get('data', {}))
        else:
            return {"error": f"Unknown message type: {msg_type}"}
    
    def detect_forms(self, data):
        """Detect forms on the page"""
        # This would integrate with the LocalGPTAgent
        return {
            "type": "forms_detected",
            "forms": [
                {
                    "id": "sample_form",
                    "fields": [
                        {"id": "name", "type": "text", "label": "Name"},
                        {"id": "email", "type": "email", "label": "Email"}
                    ]
                }
            ]
        }
    
    def fill_form(self, data):
        """Fill form with AI suggestions"""
        return {
            "type": "form_filled",
            "success": True,
            "filled_fields": data.get('fields', [])
        }
    
    def handle_voice_command(self, data):
        """Handle voice commands"""
        command = data.get('command', '')
        return {
            "type": "voice_command_processed",
            "command": command,
            "response": f"Processed command: {command}"
        }

if __name__ == "__main__":
    host = NativeHost()
    host.run()
'''
		
		host_script_path = self.native_host_path / "native_host.py"
		with open(host_script_path, 'w') as f:
			f.write(native_host_script)
		
		# Make script executable
		os.chmod(host_script_path, 0o755)
	
	async def _install_extension(self):
		"""Install browser extension in BrowserOS"""
		self.extension_path.mkdir(exist_ok=True)
		
		# Create extension manifest
		manifest = {
			"manifest_version": 3,
			"name": "Local GPT Agent",
			"version": "1.0.0",
			"description": "Privacy-first AI assistant for form filling and automation",
			"permissions": [
				"activeTab",
				"storage",
				"nativeMessaging",
				"scripting"
			],
			"host_permissions": [
				"https://linkedin.com/*",
				"https://*.linkedin.com/*"
			],
			"background": {
				"service_worker": "background.js"
			},
			"content_scripts": [
				{
					"matches": ["<all_urls>"],
					"js": ["content.js"],
					"run_at": "document_end"
				}
			],
			"action": {
				"default_popup": "popup.html",
				"default_title": "Local GPT Agent"
			},
			"native_messaging_hosts": {
				"com.local_gpt_agent.native_host": {
					"description": "Local GPT Agent Native Host"
				}
			}
		}
		
		with open(self.extension_path / "manifest.json", 'w') as f:
			json.dump(manifest, f, indent=2)
		
		# Create background script
		background_js = '''
// Background script for Local GPT Agent
// Handles communication with native host and coordinates between content scripts

class LocalGPTBackground {
    constructor() {
        this.nativePort = null;
        this.setupNativeMessaging();
        this.setupMessageHandlers();
    }
    
    setupNativeMessaging() {
        try {
            this.nativePort = chrome.runtime.connectNative('com.local_gpt_agent.native_host');
            
            this.nativePort.onMessage.addListener((message) => {
                this.handleNativeMessage(message);
            });
            
            this.nativePort.onDisconnect.addListener(() => {
                console.log('Native host disconnected');
                // Attempt to reconnect
                setTimeout(() => this.setupNativeMessaging(), 5000);
            });
            
            console.log('Connected to native host');
        } catch (error) {
            console.error('Failed to connect to native host:', error);
        }
    }
    
    setupMessageHandlers() {
        // Handle messages from content scripts
        chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
            this.handleContentMessage(request, sender, sendResponse);
            return true; // Keep message channel open for async response
        });
        
        // Handle extension icon clicks
        chrome.action.onClicked.addListener((tab) => {
            this.handleIconClick(tab);
        });
    }
    
    handleNativeMessage(message) {
        console.log('Message from native host:', message);
        
        // Forward message to appropriate content script
        chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
            if (tabs[0]) {
                chrome.tabs.sendMessage(tabs[0].id, {
                    type: 'native_message',
                    data: message
                });
            }
        });
    }
    
    handleContentMessage(request, sender, sendResponse) {
        console.log('Message from content script:', request);
        
        if (request.type === 'form_detected') {
            // Forward to native host
            if (this.nativePort) {
                this.nativePort.postMessage({
                    type: 'detect_forms',
                    data: request.data
                });
            }
        } else if (request.type === 'voice_command') {
            // Forward voice command to native host
            if (this.nativePort) {
                this.nativePort.postMessage({
                    type: 'voice_command',
                    data: request.data
                });
            }
        }
        
        sendResponse({success: true});
    }
    
    handleIconClick(tab) {
        // Inject content script or show popup
        chrome.tabs.sendMessage(tab.id, {
            type: 'toggle_agent',
            data: {}
        });
    }
}

new LocalGPTBackground();
'''
		
		with open(self.extension_path / "background.js", 'w') as f:
			f.write(background_js)
		
		# Create content script
		content_js = '''
// Content script for Local GPT Agent
// Monitors DOM for forms and handles user interactions

class LocalGPTContent {
    constructor() {
        this.isActive = false;
        this.detectedForms = [];
        this.setupEventListeners();
        this.setupMessageHandlers();
        this.startFormDetection();
    }
    
    setupEventListeners() {
        // Listen for keyboard shortcuts
        document.addEventListener('keydown', (event) => {
            if (event.ctrlKey && event.shiftKey && event.key === 'G') {
                this.toggleAgent();
            }
        });
        
        // Listen for DOM changes
        this.observer = new MutationObserver((mutations) => {
            this.handleDOMChanges(mutations);
        });
        
        this.observer.observe(document.body, {
            childList: true,
            subtree: true,
            attributes: true
        });
    }
    
    setupMessageHandlers() {
        chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
            this.handleMessage(request, sender, sendResponse);
            return true;
        });
    }
    
    handleMessage(request, sender, sendResponse) {
        switch (request.type) {
            case 'toggle_agent':
                this.toggleAgent();
                break;
            case 'native_message':
                this.handleNativeMessage(request.data);
                break;
            case 'fill_form':
                this.fillForm(request.data);
                break;
        }
        
        sendResponse({success: true});
    }
    
    toggleAgent() {
        this.isActive = !this.isActive;
        
        if (this.isActive) {
            this.showNotification('Local GPT Agent activated');
            this.detectForms();
        } else {
            this.showNotification('Local GPT Agent deactivated');
        }
    }
    
    startFormDetection() {
        // Automatically detect forms on page load
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                this.detectForms();
            });
        } else {
            this.detectForms();
        }
    }
    
    detectForms() {
        const forms = document.querySelectorAll('form');
        const formData = [];
        
        forms.forEach((form, index) => {
            const fields = [];
            const inputs = form.querySelectorAll('input, select, textarea');
            
            inputs.forEach((input) => {
                if (input.type !== 'hidden' && input.type !== 'submit') {
                    fields.push({
                        id: input.id || input.name || `field_${index}`,
                        type: input.type || 'text',
                        label: this.getFieldLabel(input),
                        placeholder: input.placeholder || '',
                        required: input.required,
                        value: input.value
                    });
                }
            });
            
            if (fields.length > 0) {
                formData.push({
                    id: form.id || `form_${index}`,
                    action: form.action || window.location.href,
                    method: form.method || 'POST',
                    fields: fields
                });
            }
        });
        
        this.detectedForms = formData;
        
        if (formData.length > 0) {
            // Send to background script
            chrome.runtime.sendMessage({
                type: 'form_detected',
                data: {
                    url: window.location.href,
                    forms: formData
                }
            });
        }
    }
    
    getFieldLabel(input) {
        // Try to find associated label
        if (input.id) {
            const label = document.querySelector(`label[for="${input.id}"]`);
            if (label) return label.textContent.trim();
        }
        
        // Check for parent label
        const parentLabel = input.closest('label');
        if (parentLabel) return parentLabel.textContent.trim();
        
        // Check for nearby text
        const previousElement = input.previousElementSibling;
        if (previousElement && previousElement.textContent) {
            return previousElement.textContent.trim();
        }
        
        return input.name || input.placeholder || 'Unknown field';
    }
    
    handleDOMChanges(mutations) {
        // Re-detect forms when DOM changes
        let shouldRedetect = false;
        
        mutations.forEach((mutation) => {
            if (mutation.type === 'childList') {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        if (node.tagName === 'FORM' || node.querySelector('form')) {
                            shouldRedetect = true;
                        }
                    }
                });
            }
        });
        
        if (shouldRedetect) {
            setTimeout(() => this.detectForms(), 500);
        }
    }
    
    handleNativeMessage(message) {
        console.log('Native message received:', message);
        
        if (message.type === 'form_filled') {
            this.showNotification('Form filled successfully');
        } else if (message.type === 'voice_command_processed') {
            this.showNotification(`Voice command: ${message.command}`);
        }
    }
    
    fillForm(data) {
        // Fill form fields with provided data
        data.fields.forEach((fieldData) => {
            const field = document.querySelector(`#${fieldData.id}, [name="${fieldData.id}"]`);
            if (field && fieldData.value) {
                field.value = fieldData.value;
                field.dispatchEvent(new Event('input', { bubbles: true }));
                field.dispatchEvent(new Event('change', { bubbles: true }));
            }
        });
    }
    
    showNotification(message) {
        // Create and show notification
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #4CAF50;
            color: white;
            padding: 12px 24px;
            border-radius: 4px;
            z-index: 10000;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            font-size: 14px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        `;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// Initialize content script
new LocalGPTContent();
'''
		
		with open(self.extension_path / "content.js", 'w') as f:
			f.write(content_js)
		
		# Create popup HTML
		popup_html = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {
            width: 300px;
            padding: 16px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }
        .header {
            text-align: center;
            margin-bottom: 20px;
        }
        .status {
            padding: 8px;
            border-radius: 4px;
            margin-bottom: 16px;
            text-align: center;
        }
        .status.active {
            background: #e8f5e8;
            color: #2e7d32;
        }
        .status.inactive {
            background: #fff3e0;
            color: #f57c00;
        }
        .controls {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        button {
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
        }
        .primary {
            background: #1976d2;
            color: white;
        }
        .secondary {
            background: #f5f5f5;
            color: #333;
        }
        .stats {
            margin-top: 16px;
            font-size: 12px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="header">
        <h3>Local GPT Agent</h3>
        <div id="status" class="status inactive">Inactive</div>
    </div>
    
    <div class="controls">
        <button id="toggleBtn" class="primary">Activate Agent</button>
        <button id="detectFormsBtn" class="secondary">Detect Forms</button>
        <button id="voiceBtn" class="secondary">Voice Command</button>
        <button id="settingsBtn" class="secondary">Settings</button>
    </div>
    
    <div class="stats">
        <div>Forms detected: <span id="formsCount">0</span></div>
        <div>Applications today: <span id="appsCount">0</span></div>
    </div>
    
    <script src="popup.js"></script>
</body>
</html>
'''
		
		with open(self.extension_path / "popup.html", 'w') as f:
			f.write(popup_html)
		
		# Create popup JavaScript
		popup_js = '''
// Popup script for Local GPT Agent

class LocalGPTPopup {
    constructor() {
        this.setupEventListeners();
        this.updateStatus();
    }
    
    setupEventListeners() {
        document.getElementById('toggleBtn').addEventListener('click', () => {
            this.toggleAgent();
        });
        
        document.getElementById('detectFormsBtn').addEventListener('click', () => {
            this.detectForms();
        });
        
        document.getElementById('voiceBtn').addEventListener('click', () => {
            this.activateVoice();
        });
        
        document.getElementById('settingsBtn').addEventListener('click', () => {
            this.openSettings();
        });
    }
    
    async toggleAgent() {
        const [tab] = await chrome.tabs.query({active: true, currentWindow: true});
        
        chrome.tabs.sendMessage(tab.id, {
            type: 'toggle_agent',
            data: {}
        });
        
        setTimeout(() => this.updateStatus(), 500);
    }
    
    async detectForms() {
        const [tab] = await chrome.tabs.query({active: true, currentWindow: true});
        
        chrome.tabs.sendMessage(tab.id, {
            type: 'detect_forms',
            data: {}
        });
    }
    
    activateVoice() {
        chrome.runtime.sendMessage({
            type: 'voice_command',
            data: {
                command: 'activate_voice_recognition'
            }
        });
    }
    
    openSettings() {
        chrome.tabs.create({
            url: chrome.runtime.getURL('settings.html')
        });
    }
    
    updateStatus() {
        // Update UI based on agent status
        chrome.storage.local.get(['agentActive', 'formsDetected', 'applicationsToday'], (result) => {
            const statusEl = document.getElementById('status');
            const toggleBtn = document.getElementById('toggleBtn');
            
            if (result.agentActive) {
                statusEl.textContent = 'Active';
                statusEl.className = 'status active';
                toggleBtn.textContent = 'Deactivate Agent';
            } else {
                statusEl.textContent = 'Inactive';
                statusEl.className = 'status inactive';
                toggleBtn.textContent = 'Activate Agent';
            }
            
            document.getElementById('formsCount').textContent = result.formsDetected || 0;
            document.getElementById('appsCount').textContent = result.applicationsToday || 0;
        });
    }
}

new LocalGPTPopup();
'''
		
		with open(self.extension_path / "popup.js", 'w') as f:
			f.write(popup_js)
	
	async def send_message(self, message_type: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		"""Send message to browser extension"""
		if not self.is_connected:
			logging.error("Not connected to BrowserOS")
			return None
		
		message = {
			"type": message_type,
			"data": data,
			"timestamp": asyncio.get_event_loop().time()
		}
		
		# In real implementation, this would use the native messaging protocol
		logging.info(f"Sending message to BrowserOS: {message}")
		return {"success": True}
	
	async def get_current_page_info(self) -> Dict[str, Any]:
		"""Get information about the current page"""
		response = await self.send_message("get_page_info", {})
		return response or {}
	
	async def detect_forms(self) -> List[FormField]:
		"""Detect forms on current page"""
		response = await self.send_message("detect_forms", {})
		if response and response.get("forms"):
			# Convert browser form data to FormField objects
			forms = []
			for form_data in response["forms"]:
				for field_data in form_data.get("fields", []):
					forms.append(FormField(
						id=field_data["id"],
						element_id=field_data["id"],
						field_type=FormFieldType(field_data.get("type", "text")),
						label=field_data.get("label", ""),
						placeholder=field_data.get("placeholder", ""),
						required=field_data.get("required", False),
						current_value=field_data.get("value", ""),
						xpath=f"//input[@id='{field_data['id']}']",
						confidence=0.9
					))
			return forms
		return []
	
	async def fill_form_field(self, field_id: str, value: str) -> bool:
		"""Fill a specific form field"""
		response = await self.send_message("fill_field", {
			"field_id": field_id,
			"value": value
		})
		return response and response.get("success", False)


class BrowserOSIntegration:
	"""Main integration class that coordinates all components"""
	
	def __init__(self):
		self.browser_api = BrowserOSAPI()
		self.gpt_agent: Optional[LocalGPTAgent] = None
		self.linkedin_automation: Optional[LinkedInWorkflowAutomation] = None
		self.is_initialized = False
	
	async def initialize(self, config: Optional[Dict[str, Any]] = None) -> bool:
		"""Initialize the complete integration"""
		logging.info("Initializing BrowserOS integration...")
		
		config = config or {}
		
		try:
			# Initialize BrowserOS API connection
			if not await self.browser_api.initialize():
				logging.error("Failed to initialize BrowserOS API")
				return False
			
			# Initialize Local GPT Agent
			self.gpt_agent = LocalGPTAgent(config)
			
			# Initialize LinkedIn automation
			self.linkedin_automation = LinkedInWorkflowAutomation(self.gpt_agent)
			
			# Setup integration callbacks
			await self._setup_integration_callbacks()
			
			# Start components
			await self.gpt_agent.start()
			
			self.is_initialized = True
			logging.info("BrowserOS integration initialized successfully")
			return True
			
		except Exception as e:
			logging.error(f"Failed to initialize BrowserOS integration: {e}")
			return False
	
	async def _setup_integration_callbacks(self):
		"""Setup callbacks between components"""
		
		# DOM watcher callback to use BrowserOS APIs
		async def browser_form_detected(form_id: str, fields: List[FormField]):
			"""Handle form detection through BrowserOS APIs"""
			browser_forms = await self.browser_api.detect_forms()
			
			# Merge browser-detected forms with agent forms
			for browser_form in browser_forms:
				if browser_form.element_id not in [f.element_id for f in fields]:
					fields.append(browser_form)
			
			logging.info(f"Integrated form detection: {len(fields)} fields found")
		
		if self.gpt_agent:
			self.gpt_agent.dom_watcher.register_form_detection_callback(browser_form_detected)
		
		# Voice command callback for browser integration
		async def handle_browser_voice_commands(parameters: Dict[str, Any]):
			"""Handle voice commands that need browser interaction"""
			command = parameters.get("command", "").lower()
			
			if "scroll down" in command:
				await self.browser_api.send_message("scroll", {"direction": "down"})
			elif "scroll up" in command:
				await self.browser_api.send_message("scroll", {"direction": "up"})
			elif "go back" in command:
				await self.browser_api.send_message("navigate", {"action": "back"})
			elif "refresh page" in command:
				await self.browser_api.send_message("navigate", {"action": "refresh"})
		
		if self.gpt_agent:
			self.gpt_agent.voice_processor.register_intent_callback(
				"browser_control", handle_browser_voice_commands
			)
	
	async def start_linkedin_automation(self):
		"""Start LinkedIn automation with browser integration"""
		if not self.is_initialized:
			logging.error("Integration not initialized")
			return False
		
		if self.linkedin_automation:
			await self.linkedin_automation.start_automation()
			return True
		
		return False
	
	async def process_current_page(self) -> Dict[str, Any]:
		"""Process the current browser page for automation opportunities"""
		if not self.is_initialized:
			return {"error": "Integration not initialized"}
		
		try:
			# Get current page info
			page_info = await self.browser_api.get_current_page_info()
			
			# Check if it's a LinkedIn page
			is_linkedin = "linkedin.com" in page_info.get("url", "")
			
			# Detect forms
			forms = await self.browser_api.detect_forms()
			
			# Get AI suggestions for forms
			suggestions = {}
			if forms and self.gpt_agent:
				for form in forms:
					form_suggestions = await self.gpt_agent.rag_pipeline.get_field_suggestions(
						form, self.gpt_agent.ollama_client
					)
					if form_suggestions:
						suggestions[form.element_id] = form_suggestions[0]
			
			return {
				"page_info": page_info,
				"is_linkedin": is_linkedin,
				"forms_detected": len(forms),
				"ai_suggestions": suggestions,
				"automation_ready": is_linkedin and len(forms) > 0
			}
			
		except Exception as e:
			logging.error(f"Error processing current page: {e}")
			return {"error": str(e)}
	
	async def auto_fill_current_forms(self) -> Dict[str, Any]:
		"""Auto-fill forms on the current page"""
		if not self.is_initialized:
			return {"error": "Integration not initialized"}
		
		try:
			forms = await self.browser_api.detect_forms()
			filled_count = 0
			
			for form in forms:
				suggestions = await self.gpt_agent.rag_pipeline.get_field_suggestions(
					form, self.gpt_agent.ollama_client
				)
				
				if suggestions and suggestions[0]:
					success = await self.browser_api.fill_form_field(
						form.element_id, suggestions[0]
					)
					if success:
						filled_count += 1
			
			return {
				"success": True,
				"forms_processed": len(forms),
				"fields_filled": filled_count
			}
			
		except Exception as e:
			logging.error(f"Error auto-filling forms: {e}")
			return {"error": str(e)}
	
	async def get_integration_status(self) -> Dict[str, Any]:
		"""Get status of all integration components"""
		return {
			"initialized": self.is_initialized,
			"browser_api_connected": self.browser_api.is_connected,
			"gpt_agent_active": self.gpt_agent.is_active if self.gpt_agent else False,
			"linkedin_automation_active": self.linkedin_automation.is_active if self.linkedin_automation else False,
			"components": {
				"browser_api": bool(self.browser_api),
				"gpt_agent": bool(self.gpt_agent),
				"linkedin_automation": bool(self.linkedin_automation)
			}
		}
	
	async def shutdown(self):
		"""Shutdown all components gracefully"""
		logging.info("Shutting down BrowserOS integration...")
		
		if self.linkedin_automation:
			self.linkedin_automation.stop_automation()
		
		if self.gpt_agent:
			await self.gpt_agent.stop()
		
		self.is_initialized = False
		logging.info("BrowserOS integration shutdown complete")


# Example usage and main entry point
async def main():
	"""Main entry point for BrowserOS integration"""
	
	# Setup logging
	logging.basicConfig(
		level=logging.INFO,
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
		handlers=[
			logging.FileHandler('browseros_integration.log'),
			logging.StreamHandler(sys.stdout)
		]
	)
	
	# Configuration
	config = {
		"auto_suggest": True,
		"voice_activation": True,
		"privacy_mode": True,
		"linkedin_automation": True,
		"daily_application_limit": 25,  # Conservative limit
		"respect_rate_limits": True
	}
	
	# Initialize integration
	integration = BrowserOSIntegration()
	
	try:
		if await integration.initialize(config):
			logging.info("BrowserOS integration started successfully")
			
			# Start LinkedIn automation if enabled
			if config.get("linkedin_automation"):
				await integration.start_linkedin_automation()
			
			# Keep running until interrupted
			while integration.is_initialized:
				# Process current page periodically
				status = await integration.process_current_page()
				if status.get("automation_ready"):
					logging.info("Automation opportunity detected")
				
				await asyncio.sleep(5)  # Check every 5 seconds
				
		else:
			logging.error("Failed to initialize BrowserOS integration")
			
	except KeyboardInterrupt:
		logging.info("Received interrupt signal")
	except Exception as e:
		logging.error(f"Unexpected error: {e}")
	finally:
		await integration.shutdown()


if __name__ == "__main__":
	asyncio.run(main())