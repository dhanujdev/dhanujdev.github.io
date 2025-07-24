'use client'

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { ArrowDown, Download, Github, Play } from 'lucide-react'
import { motion } from 'framer-motion'
import { AnimatedIntro } from './animated-intro'

export function HeroSection() {
	const [showIntro, setShowIntro] = useState(true)

	useEffect(() => {
		// Check if intro was already shown in this session
		const introShown = sessionStorage.getItem('introShown')
		if (introShown) {
			setShowIntro(false)
		}
	}, [])

	const handleIntroComplete = () => {
		setShowIntro(false)
		sessionStorage.setItem('introShown', 'true')
	}

	const playIntroAgain = () => {
		setShowIntro(true)
		sessionStorage.removeItem('introShown')
	}

	return (
		<>
			{showIntro && <AnimatedIntro onComplete={handleIntroComplete} />}
			<section className="min-h-screen flex items-center justify-center bg-gradient-to-br from-background via-background to-muted/20">
			<div className="container mx-auto container-padding text-center">
				<motion.div
					initial={{ opacity: 0, y: 20 }}
					animate={{ opacity: 1, y: 0 }}
					transition={{ duration: 0.5 }}
					className="max-w-4xl mx-auto"
				>
					<motion.h1
						initial={{ opacity: 0, y: 20 }}
						animate={{ opacity: 1, y: 0 }}
						transition={{ duration: 0.5, delay: 0.1 }}
						className="text-4xl md:text-6xl lg:text-7xl font-bold mb-6"
					>
						Hi, I'm{' '}
						<span className="gradient-text">Dhanuj Gumpella</span>
					</motion.h1>
					
					<motion.p
						initial={{ opacity: 0, y: 20 }}
						animate={{ opacity: 1, y: 0 }}
						transition={{ duration: 0.5, delay: 0.2 }}
						className="text-xl md:text-2xl text-muted-foreground mb-8 leading-relaxed"
					>
						Software Engineer AI specializing in production-scale
						<br />
						AI systems, RAG architectures, and cloud infrastructure
					</motion.p>
					
					<motion.div
						initial={{ opacity: 0, y: 20 }}
						animate={{ opacity: 1, y: 0 }}
						transition={{ duration: 0.5, delay: 0.3 }}
						className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12"
					>
						<Button size="lg" className="w-full sm:w-auto">
							<Download className="mr-2 h-4 w-4" />
							Download CV
						</Button>
						<Button variant="outline" size="lg" className="w-full sm:w-auto" asChild>
							<a href="https://github.com/dhanujdev" target="_blank" rel="noopener noreferrer">
								<Github className="mr-2 h-4 w-4" />
								View GitHub
							</a>
						</Button>
						<Button variant="secondary" size="lg" className="w-full sm:w-auto" onClick={playIntroAgain}>
							<Play className="mr-2 h-4 w-4" />
							Replay Intro
						</Button>
					</motion.div>
					
					<motion.div
						initial={{ opacity: 0 }}
						animate={{ opacity: 1 }}
						transition={{ duration: 0.5, delay: 0.5 }}
						className="flex justify-center"
					>
						<motion.div
							animate={{ y: [0, 10, 0] }}
							transition={{ duration: 2, repeat: Infinity }}
						>
							<ArrowDown className="h-6 w-6 text-muted-foreground" />
						</motion.div>
					</motion.div>
				</motion.div>
			</div>
			</section>
		</>
	)
}