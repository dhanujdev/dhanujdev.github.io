'use client'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Award, Calendar } from 'lucide-react'
import { motion } from 'framer-motion'

export function CertificationsSection() {
	const certifications = [
		{
			title: 'Microsoft AI & ML Engineering Professional Certification',
			issuer: 'Microsoft',
			status: 'Ongoing',
			description: 'Comprehensive certification covering Azure AI services, machine learning operations, and AI solution architecture.',
			skills: ['Azure AI', 'MLOps', 'AI Architecture', 'Cognitive Services']
		},
		{
			title: 'Meta Full Stack Developer Professional Certification',
			issuer: 'Meta',
			status: 'Completed',
			description: 'Full-stack web development certification covering modern frameworks, databases, and deployment strategies.',
			skills: ['React', 'Node.js', 'Database Design', 'API Development']
		},
		{
			title: 'IBM RAG and Agentic AI Professional Certification',
			issuer: 'IBM',
			status: 'Completed',
			description: 'Advanced certification in Retrieval-Augmented Generation and agentic AI systems for enterprise applications.',
			skills: ['RAG Architecture', 'Vector Databases', 'LangChain', 'Agentic AI']
		}
	]

	return (
		<section id="certifications" className="py-20">
			<div className="container mx-auto container-padding">
				<motion.div
					initial={{ opacity: 0, y: 20 }}
					whileInView={{ opacity: 1, y: 0 }}
					transition={{ duration: 0.5 }}
					viewport={{ once: true }}
					className="max-w-4xl mx-auto"
				>
					<h2 className="text-3xl md:text-4xl font-bold text-center mb-12">
						Certifications & <span className="gradient-text">Credentials</span>
					</h2>
					
					<div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
						{certifications.map((cert, index) => (
							<motion.div
								key={cert.title}
								initial={{ opacity: 0, y: 20 }}
								whileInView={{ opacity: 1, y: 0 }}
								transition={{ duration: 0.5, delay: index * 0.1 }}
								viewport={{ once: true }}
							>
								<Card className="h-full hover:shadow-lg transition-shadow duration-300">
									<CardHeader>
										<div className="flex items-center gap-2 mb-2">
											<Award className="h-5 w-5 text-primary" />
											<Badge variant={cert.status === 'Ongoing' ? 'secondary' : 'default'}>
												{cert.status}
											</Badge>
										</div>
										<CardTitle className="text-lg leading-tight">
											{cert.title}
										</CardTitle>
										<CardDescription className="text-primary font-medium">
											{cert.issuer}
										</CardDescription>
									</CardHeader>
									
									<CardContent>
										<p className="text-sm text-muted-foreground mb-4">
											{cert.description}
										</p>
										<div className="flex flex-wrap gap-2">
											{cert.skills.map((skill) => (
												<Badge key={skill} variant="outline" className="text-xs">
													{skill}
												</Badge>
											))}
										</div>
									</CardContent>
								</Card>
							</motion.div>
						))}
					</div>
				</motion.div>
			</div>
		</section>
	)
}