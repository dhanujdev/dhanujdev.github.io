'use client'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { CalendarDays, MapPin } from 'lucide-react'
import { motion } from 'framer-motion'

export function ExperienceSection() {
	const experiences = [
		{
			title: 'Software Engineer AI',
			company: 'NYC Department of Social Services',
			location: 'New York City, NY',
			duration: 'Jan 2023 - Present',
			description: 'Modernizing citizen-services platforms serving 8M+ NYC residents through AI-powered automation. Led Azure ML infrastructure modernization across mission-critical systems, achieving 99.9% uptime while processing 100K+ daily requests through intelligent document workflows.',
			tech: ['Azure ML', 'Azure AI Search', 'GPT-4', 'Databricks', 'AKS', 'Python', 'PowerShell', 'NLP', 'RAG']
		},
		{
			title: 'Software Engineer',
			company: 'Go Offer Hyperlocal Pvt Ltd',
			location: 'India',
			duration: 'Jul 2018 - Jul 2021',
			description: 'AI-powered e-commerce platform development for SMB retail digital transformation. Engineered ML-driven product categorization system using Azure Computer Vision and Gemini Flash APIs to automatically classify and tag 1,500+ jewelry products, achieving 95% accuracy.',
			tech: ['Azure Computer Vision', 'Gemini Flash API', 'Next.js', 'React', 'Node.js', 'Python', 'PostgreSQL', 'ML']
		}
	]

	const education = [
		{
			title: 'Master of Science, Computer Science',
			institution: 'University of North Texas',
			location: 'Texas',
			duration: 'Dec 2022',
			description: 'Advanced coursework in AI/ML, algorithms, and distributed systems. Focused on machine learning applications and software engineering best practices.',
			achievements: ['AI/ML Specialization', 'Graduate Research', 'Advanced Algorithms']
		}
	]

	return (
		<section id="experience" className="py-20 bg-muted/30">
			<div className="container mx-auto container-padding">
				<motion.div
					initial={{ opacity: 0, y: 20 }}
					whileInView={{ opacity: 1, y: 0 }}
					transition={{ duration: 0.5 }}
					viewport={{ once: true }}
					className="max-w-4xl mx-auto"
				>
					<h2 className="text-3xl md:text-4xl font-bold text-center mb-12">
						Experience & <span className="gradient-text">Education</span>
					</h2>
					
					{/* Experience */}
					<div className="mb-16">
						<h3 className="text-2xl font-semibold mb-8 text-primary">Work Experience</h3>
						<div className="space-y-6">
							{experiences.map((exp, index) => (
								<motion.div
									key={exp.title + exp.company}
									initial={{ opacity: 0, x: -20 }}
									whileInView={{ opacity: 1, x: 0 }}
									transition={{ duration: 0.5, delay: index * 0.1 }}
									viewport={{ once: true }}
								>
									<Card>
										<CardHeader>
											<CardTitle className="text-xl">{exp.title}</CardTitle>
											<CardDescription className="text-lg font-medium text-primary">
												{exp.company}
											</CardDescription>
											<div className="flex flex-col sm:flex-row sm:items-center gap-2 text-sm text-muted-foreground">
												<div className="flex items-center gap-1">
													<MapPin className="h-4 w-4" />
													{exp.location}
												</div>
												<div className="flex items-center gap-1">
													<CalendarDays className="h-4 w-4" />
													{exp.duration}
												</div>
											</div>
										</CardHeader>
										<CardContent>
											<p className="text-muted-foreground mb-4">{exp.description}</p>
											<div className="flex flex-wrap gap-2">
												{exp.tech.map((tech) => (
													<Badge key={tech} variant="secondary">
														{tech}
													</Badge>
												))}
											</div>
										</CardContent>
									</Card>
								</motion.div>
							))}
						</div>
					</div>
					
					{/* Education */}
					<div>
						<h3 className="text-2xl font-semibold mb-8 text-primary">Education</h3>
						<div className="space-y-6">
							{education.map((edu, index) => (
								<motion.div
									key={edu.title + edu.institution}
									initial={{ opacity: 0, x: -20 }}
									whileInView={{ opacity: 1, x: 0 }}
									transition={{ duration: 0.5, delay: index * 0.1 }}
									viewport={{ once: true }}
								>
									<Card>
										<CardHeader>
											<CardTitle className="text-xl">{edu.title}</CardTitle>
											<CardDescription className="text-lg font-medium text-primary">
												{edu.institution}
											</CardDescription>
											<div className="flex flex-col sm:flex-row sm:items-center gap-2 text-sm text-muted-foreground">
												<div className="flex items-center gap-1">
													<MapPin className="h-4 w-4" />
													{edu.location}
												</div>
												<div className="flex items-center gap-1">
													<CalendarDays className="h-4 w-4" />
													{edu.duration}
												</div>
											</div>
										</CardHeader>
										<CardContent>
											<p className="text-muted-foreground mb-4">{edu.description}</p>
											<div className="space-y-1">
												{edu.achievements.map((achievement) => (
													<Badge key={achievement} variant="outline">
														{achievement}
													</Badge>
												))}
											</div>
										</CardContent>
									</Card>
								</motion.div>
							))}
						</div>
					</div>
				</motion.div>
			</div>
		</section>
	)
}