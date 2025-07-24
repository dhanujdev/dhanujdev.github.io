#!/usr/bin/env python3
"""
User Context Setup Script for Local GPT Agent
=============================================

This script helps users set up their personal context for intelligent form filling.
It creates a secure, local profile that the AI agent uses to fill forms intelligently.

Privacy Note: All data is stored locally and never sent to external servers.
"""

import json
import getpass
from pathlib import Path
from typing import Dict, List, Any
import logging
from datetime import datetime

from local_gpt_agent import UserContext, RAGPipeline


class UserContextSetup:
	"""Interactive setup for user context"""
	
	def __init__(self):
		self.context = UserContext()
		self.setup_path = Path("./context_db")
		self.setup_path.mkdir(exist_ok=True)
	
	def run_interactive_setup(self):
		"""Run interactive setup process"""
		print("🤖 Local GPT Agent - User Context Setup")
		print("=" * 50)
		print("This setup will create your personal profile for intelligent form filling.")
		print("✅ All data stays local on your device")
		print("✅ No information is sent to external servers")
		print("✅ You can modify or delete this data anytime")
		print()
		
		# Basic Information
		print("📝 Basic Information")
		print("-" * 20)
		self._setup_basic_info()
		
		# Contact Information  
		print("\n📞 Contact Information")
		print("-" * 20)
		self._setup_contact_info()
		
		# Address Information
		print("\n🏠 Address Information")
		print("-" * 20)
		self._setup_address_info()
		
		# Work Experience
		print("\n💼 Work Experience")
		print("-" * 20)
		self._setup_work_experience()
		
		# Education
		print("\n🎓 Education")
		print("-" * 15)
		self._setup_education()
		
		# Skills
		print("\n🛠️ Skills")
		print("-" * 10)
		self._setup_skills()
		
		# Preferences
		print("\n⚙️ Preferences")
		print("-" * 15)
		self._setup_preferences()
		
		# Custom Responses
		print("\n💬 Custom Responses")
		print("-" * 20)
		self._setup_custom_responses()
		
		# Save and confirm
		self._save_context()
		
		print("\n✅ Setup Complete!")
		print(f"Your profile has been saved to: {self.setup_path}")
		print("\nYou can now use voice commands like:")
		print("- 'Fill this form'")
		print("- 'Auto fill my information'")
		print("- 'Save this workflow'")
	
	def _setup_basic_info(self):
		"""Setup basic personal information"""
		self.context.full_name = input("Full Name: ").strip()
		
		# Parse name components if needed
		if self.context.full_name:
			name_parts = self.context.full_name.split()
			if len(name_parts) >= 2:
				first_name = name_parts[0]
				last_name = " ".join(name_parts[1:])
				print(f"  First Name: {first_name}")
				print(f"  Last Name: {last_name}")
	
	def _setup_contact_info(self):
		"""Setup contact information"""
		self.context.email = input("Email Address: ").strip()
		self.context.phone = input("Phone Number: ").strip()
		
		# Additional contact methods
		linkedin_url = input("LinkedIn Profile URL (optional): ").strip()
		github_url = input("GitHub Profile URL (optional): ").strip()
		website = input("Personal Website (optional): ").strip()
		
		if linkedin_url or github_url or website:
			if not hasattr(self.context, 'social_profiles'):
				self.context.social_profiles = {}
			if linkedin_url:
				self.context.social_profiles['linkedin'] = linkedin_url
			if github_url:
				self.context.social_profiles['github'] = github_url
			if website:
				self.context.social_profiles['website'] = website
	
	def _setup_address_info(self):
		"""Setup address information"""
		print("Enter your address (used for shipping, billing, etc.):")
		
		street = input("Street Address: ").strip()
		city = input("City: ").strip()
		state = input("State/Province: ").strip()
		zipcode = input("ZIP/Postal Code: ").strip()
		country = input("Country (default: United States): ").strip() or "United States"
		
		self.context.address = {
			"street": street,
			"city": city,
			"state": state,
			"zipcode": zipcode,
			"country": country
		}
		
		# Additional address fields
		apt_unit = input("Apartment/Unit (optional): ").strip()
		if apt_unit:
			self.context.address["apartment"] = apt_unit
	
	def _setup_work_experience(self):
		"""Setup work experience"""
		print("Enter your work experience (most recent first):")
		print("Press Enter on empty 'Company' to finish")
		
		while True:
			print(f"\nJob #{len(self.context.work_experience) + 1}:")
			company = input("Company Name: ").strip()
			if not company:
				break
			
			position = input("Job Title/Position: ").strip()
			start_date = input("Start Date (YYYY-MM or 'Current'): ").strip()
			end_date = input("End Date (YYYY-MM or 'Current'): ").strip()
			description = input("Job Description (brief): ").strip()
			
			# Parse employment type
			emp_type = input("Employment Type (Full-time/Part-time/Contract/Internship): ").strip()
			location = input("Location (City, State): ").strip()
			
			experience = {
				"company": company,
				"position": position,
				"start_date": start_date,
				"end_date": end_date,
				"description": description,
				"employment_type": emp_type or "Full-time",
				"location": location
			}
			
			self.context.work_experience.append(experience)
			
			continue_adding = input("Add another job? (y/N): ").strip().lower()
			if continue_adding != 'y':
				break
	
	def _setup_education(self):
		"""Setup education information"""
		print("Enter your education (most recent first):")
		print("Press Enter on empty 'School' to finish")
		
		while True:
			print(f"\nEducation #{len(self.context.education) + 1}:")
			school = input("School/University Name: ").strip()
			if not school:
				break
			
			degree = input("Degree (e.g., Bachelor of Science): ").strip()
			field = input("Field of Study (e.g., Computer Science): ").strip()
			graduation_year = input("Graduation Year (YYYY): ").strip()
			gpa = input("GPA (optional): ").strip()
			
			education = {
				"school": school,
				"degree": degree,
				"field_of_study": field,
				"graduation_year": graduation_year
			}
			
			if gpa:
				education["gpa"] = gpa
			
			# Additional education details
			honors = input("Honors/Awards (optional): ").strip()
			if honors:
				education["honors"] = honors
			
			relevant_courses = input("Relevant Coursework (comma-separated, optional): ").strip()
			if relevant_courses:
				education["relevant_courses"] = [course.strip() for course in relevant_courses.split(",")]
			
			self.context.education.append(education)
			
			continue_adding = input("Add another degree? (y/N): ").strip().lower()
			if continue_adding != 'y':
				break
	
	def _setup_skills(self):
		"""Setup skills and competencies"""
		print("Enter your skills (comma-separated):")
		print("Examples: Python, JavaScript, React, Machine Learning, Project Management")
		
		skills_input = input("Skills: ").strip()
		if skills_input:
			self.context.skills = [skill.strip() for skill in skills_input.split(",")]
		
		# Categorize skills
		print("\nOptional: Categorize your skills")
		categorize = input("Would you like to categorize your skills? (y/N): ").strip().lower()
		
		if categorize == 'y':
			skill_categories = {}
			
			for skill in self.context.skills:
				print(f"\nSkill: {skill}")
				category = input("Category (Programming, Tools, Soft Skills, etc.): ").strip()
				level = input("Proficiency Level (Beginner/Intermediate/Advanced/Expert): ").strip()
				
				if category not in skill_categories:
					skill_categories[category] = []
				
				skill_categories[category].append({
					"name": skill,
					"level": level or "Intermediate"
				})
			
			if not hasattr(self.context, 'skill_categories'):
				self.context.skill_categories = skill_categories
	
	def _setup_preferences(self):
		"""Setup user preferences for form filling"""
		print("Set your preferences for form filling:")
		
		# Work preferences
		print("\nWork Preferences:")
		work_type = input("Preferred Work Type (Remote/Hybrid/On-site/Any): ").strip()
		salary_min = input("Minimum Salary Expectation (optional): ").strip()
		salary_max = input("Maximum Salary Expectation (optional): ").strip()
		willing_to_relocate = input("Willing to relocate? (yes/no): ").strip().lower()
		
		# Availability
		availability = input("Availability to start (e.g., '2 weeks notice', 'Immediately'): ").strip()
		
		# Work authorization
		work_auth = input("Work Authorization Status (e.g., 'US Citizen', 'Visa Required'): ").strip()
		
		preferences = {
			"work_type": work_type,
			"willing_to_relocate": willing_to_relocate in ['yes', 'y'],
			"availability": availability,
			"work_authorization": work_auth
		}
		
		if salary_min:
			preferences["salary_min"] = salary_min
		if salary_max:
			preferences["salary_max"] = salary_max
		
		# Additional preferences
		industries = input("Preferred Industries (comma-separated, optional): ").strip()
		if industries:
			preferences["preferred_industries"] = [ind.strip() for ind in industries.split(",")]
		
		company_size = input("Preferred Company Size (Startup/Small/Medium/Large/Any): ").strip()
		if company_size:
			preferences["company_size"] = company_size
		
		self.context.preferences = preferences
	
	def _setup_custom_responses(self):
		"""Setup custom responses for common questions"""
		print("Setup custom responses for common screening questions:")
		print("Press Enter on empty question to finish")
		
		common_questions = [
			"Why are you interested in this role?",
			"Why do you want to work for this company?",
			"What are your salary expectations?",
			"Where do you see yourself in 5 years?",
			"What is your greatest strength?",
			"What is your greatest weakness?",
			"Why are you leaving your current job?"
		]
		
		print("\nCommon questions (optional - you can add custom responses):")
		for i, question in enumerate(common_questions, 1):
			print(f"{i}. {question}")
		
		while True:
			question = input("\nEnter question (or number from above): ").strip()
			if not question:
				break
			
			# Handle numbered selection
			if question.isdigit() and 1 <= int(question) <= len(common_questions):
				question = common_questions[int(question) - 1]
			
			response = input(f"Your response to '{question}': ").strip()
			if response:
				self.context.custom_responses[question] = response
			
			continue_adding = input("Add another custom response? (y/N): ").strip().lower()
			if continue_adding != 'y':
				break
	
	def _save_context(self):
		"""Save user context to local storage"""
		print("\n💾 Saving your profile...")
		
		# Initialize RAG pipeline to save context
		rag_pipeline = RAGPipeline(context_db_path=str(self.setup_path))
		rag_pipeline.user_context = self.context
		rag_pipeline.save_user_context()
		
		# Also save as JSON for easy viewing/editing
		context_file = self.setup_path / "user_profile.json"
		with open(context_file, 'w') as f:
			# Convert context to dict for JSON serialization
			context_dict = self.context.__dict__.copy()
			json.dump(context_dict, f, indent=2, default=str)
		
		print(f"✅ Profile saved to {context_file}")
		
		# Show summary
		self._show_summary()
	
	def _show_summary(self):
		"""Show a summary of the saved context"""
		print("\n📋 Profile Summary:")
		print("-" * 20)
		print(f"Name: {self.context.full_name}")
		print(f"Email: {self.context.email}")
		print(f"Phone: {self.context.phone}")
		print(f"Location: {self.context.address.get('city', '')}, {self.context.address.get('state', '')}")
		print(f"Work Experience: {len(self.context.work_experience)} positions")
		print(f"Education: {len(self.context.education)} degrees")
		print(f"Skills: {len(self.context.skills)} skills")
		print(f"Custom Responses: {len(self.context.custom_responses)} responses")


def main():
	"""Main setup function"""
	try:
		setup = UserContextSetup()
		setup.run_interactive_setup()
		
		print("\n🎉 Setup complete! You can now:")
		print("1. Start BrowserOS")
		print("2. Load the Local GPT Agent extension")
		print("3. Use voice commands to fill forms automatically")
		print("\nFor help, run: python browser_os_integration.py --help")
		
	except KeyboardInterrupt:
		print("\n\n❌ Setup cancelled by user")
	except Exception as e:
		print(f"\n❌ Setup failed: {e}")
		logging.error(f"Setup error: {e}")


if __name__ == "__main__":
	main()