'use client'

import { useState, useEffect } from 'react'
import { motion, useAnimation } from 'framer-motion'
import { Button } from '@/components/ui/button'
import { Volume2, VolumeX, Play } from 'lucide-react'
import { useTypingSound } from '@/hooks/useTypingSound'

interface AnimatedIntroProps {
	onComplete?: () => void
}

export function AnimatedIntro({ onComplete }: AnimatedIntroProps) {
	const [currentSection, setCurrentSection] = useState(0)
	const [displayText, setDisplayText] = useState('')
	const [isTyping, setIsTyping] = useState(false)
	const [showSkip, setShowSkip] = useState(false)
	const [audioEnabled, setAudioEnabled] = useState(false)
	const [showIntro, setShowIntro] = useState(true)
	const controls = useAnimation()
	const { playTypingSound, playBellSound } = useTypingSound()

	const resumeData = [
		{
			title: "DHANUJ GUMPELLA",
			content: "Brooklyn, NY | +1 551-253-8297 | dhanujsportfolio@gmail.com",
			delay: 100
		},
		{
			title: "SOFTWARE ENGINEER AI",
			content: "Specializing in production-scale AI systems, RAG architectures, and cloud infrastructure",
			delay: 80
		},
		{
			title: "EXPERIENCE",
			content: `NYC Department of Social Services - Software Engineer AI (Jan 2023 - Present)
• Led Azure ML infrastructure modernization serving 8M+ NYC residents
• Architected production RAG pipeline reducing policy lookup time by 60%
• Automated ML model lifecycle achieving 99.9% uptime
• Built secure document processing pipelines with 75% time reduction`,
			delay: 60
		},
		{
			title: "KEY PROJECTS",
			content: `AI Resume Tailoring SaaS Platform
• Built production RAG system with 95% ATS match scores
• Chrome extension with AI-powered DOM analysis

YouTube Content Automation Pipeline  
• LangChain-based agentic pipeline with FastAPI
• Automated video processing with AI voice generation`,
			delay: 50
		},
		{
			title: "TECHNICAL EXPERTISE",
			content: `AI/ML: LangChain, LangGraph, RAG, Vector Databases, PyTorch, TensorFlow
Cloud: Azure ML, AWS Bedrock, Docker, Kubernetes, CI/CD
Programming: Python, TypeScript, Java, FastAPI, React, Next.js`,
			delay: 40
		}
	]

	const typeText = async (text: string, delay: number) => {
		setIsTyping(true)
		for (let i = 0; i <= text.length; i++) {
			setDisplayText(text.slice(0, i))
			
			// Play typing sound for each character (but not on spaces)
			if (audioEnabled && text[i] && text[i] !== ' ' && text[i] !== '\n') {
				playTypingSound()
			}
			
			await new Promise(resolve => setTimeout(resolve, delay))
		}
		setIsTyping(false)
		
		// Play bell sound when section is complete
		if (audioEnabled) {
			playBellSound()
		}
	}

	useEffect(() => {
		const runAnimation = async () => {
			setShowSkip(true)
			
			for (let i = 0; i < resumeData.length; i++) {
				setCurrentSection(i)
				const section = resumeData[i]
				
				// Type title
				await typeText(section.title, 100)
				await new Promise(resolve => setTimeout(resolve, 300))
				
				// Type content
				await typeText(section.title + '\n\n' + section.content, section.delay)
				await new Promise(resolve => setTimeout(resolve, 800))
			}
			
			// Final animation
			await typeText('Welcome to my portfolio...', 80)
			await new Promise(resolve => setTimeout(resolve, 1500))
			
			setShowIntro(false)
			onComplete?.()  // Call the completion callback
		}

		if (showIntro) {
			runAnimation()
		}
	}, [showIntro])

	const skipIntro = () => {
		setShowIntro(false)
		onComplete?.()
	}

	const toggleAudio = () => {
		setAudioEnabled(!audioEnabled)
	}

	if (!showIntro) {
		return null
	}

	return (
		<motion.div
			initial={{ opacity: 0 }}
			animate={{ opacity: 1 }}
			exit={{ opacity: 0 }}
			className="fixed inset-0 z-50 bg-black text-green-400 font-mono overflow-hidden"
		>
			{/* Terminal Background Pattern */}
			<div className="absolute inset-0 opacity-10">
				<div className="grid grid-cols-12 gap-1 h-full w-full">
					{Array.from({ length: 1000 }).map((_, i) => (
						<div key={i} className="bg-green-400 opacity-5 animate-pulse" />
					))}
				</div>
			</div>

			{/* Controls */}
			<div className="absolute top-4 right-4 flex gap-2 z-10">
				<Button
					variant="ghost"
					size="icon"
					onClick={toggleAudio}
					className="text-green-400 hover:bg-green-400/20"
				>
					{audioEnabled ? <Volume2 className="h-4 w-4" /> : <VolumeX className="h-4 w-4" />}
				</Button>
				{showSkip && (
					<Button
						variant="ghost"
						onClick={skipIntro}
						className="text-green-400 hover:bg-green-400/20"
					>
						Skip Intro
					</Button>
				)}
			</div>

			{/* Terminal Header */}
			<div className="border-b border-green-400/30 p-4">
				<div className="flex items-center gap-2">
					<div className="w-3 h-3 rounded-full bg-red-500"></div>
					<div className="w-3 h-3 rounded-full bg-yellow-500"></div>
					<div className="w-3 h-3 rounded-full bg-green-500"></div>
					<span className="ml-4 text-green-400/70">terminal — Resume Display</span>
				</div>
			</div>

			{/* Main Content */}
			<div className="p-8 h-full overflow-auto">
				<div className="max-w-4xl mx-auto">
					{/* Prompt */}
					<div className="mb-4">
						<span className="text-green-300">user@portfolio:~$ </span>
						<span className="text-white">cat dhanuj_resume.txt</span>
					</div>

					{/* Resume Content */}
					<motion.div
						className="whitespace-pre-wrap text-sm leading-relaxed"
						initial={{ opacity: 0 }}
						animate={{ opacity: 1 }}
					>
						{displayText}
						{isTyping && (
							<motion.span
								animate={{ opacity: [1, 0] }}
								transition={{ duration: 0.5, repeat: Infinity }}
								className="inline-block w-2 h-5 bg-green-400 ml-1"
							/>
						)}
					</motion.div>

					{/* Progress Indicator */}
					<div className="fixed bottom-8 left-1/2 transform -translate-x-1/2">
						<div className="flex items-center gap-2 bg-black/50 backdrop-blur-sm px-4 py-2 rounded-full border border-green-400/30">
							<div className="flex gap-1">
								{resumeData.map((_, index) => (
									<div
										key={index}
										className={`w-2 h-2 rounded-full transition-colors duration-300 ${
											index <= currentSection ? 'bg-green-400' : 'bg-green-400/30'
										}`}
									/>
								))}
							</div>
							<span className="text-green-400 text-xs ml-2">
								{currentSection + 1} / {resumeData.length}
							</span>
						</div>
					</div>
				</div>
			</div>

		</motion.div>
	)
}