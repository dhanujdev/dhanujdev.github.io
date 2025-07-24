'use client'

import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { ExternalLink, Github, Star, GitFork } from 'lucide-react'
import { motion } from 'framer-motion'
import { useEffect, useState } from 'react'
import { fetchGitHubRepos, type GitHubRepo, getLanguageColor } from '@/lib/github'

export function ProjectsSection() {
	const [githubRepos, setGithubRepos] = useState<GitHubRepo[]>([])
	const [loading, setLoading] = useState(true)

	// Replace 'yourusername' with your actual GitHub username
	const GITHUB_USERNAME = 'dhanujdev'

	useEffect(() => {
		async function loadRepos() {
			const repos = await fetchGitHubRepos(GITHUB_USERNAME, { per_page: 6 })
			setGithubRepos(repos)
			setLoading(false)
		}
		loadRepos()
	}, [])

	// Actual projects from resume
	const projects = [
		{
			title: 'AI Resume Tailoring SaaS Platform',
			description: 'Built production SaaS platform implementing RAG to store and index user professional data in Supabase vector database, enabling context-aware resume generation that achieves 95% ATS match scores with Chrome extension integration.',
			tech: ['RAG', 'Supabase', 'Vector Database', 'Chrome Extension', 'AI/ML', 'DOM Analysis'],
			github: 'https://github.com/dhanujdev/AI-Powered-Resume-Tailor',
			demo: null,
			image: '/api/placeholder/600/400'
		},
		{
			title: 'YouTube Content Automation Pipeline',
			description: 'Engineered an end-to-end LangChain-based agentic pipeline using FastAPI to automate YouTube content creation: scanned Google Drive for raw recipe clips, merged videos with background music using FFmpeg, generated metadata, AI Voice Over in local language via Gemini.',
			tech: ['LangChain', 'FastAPI', 'FFmpeg', 'Gemini', 'YouTube Data API', 'OAuth2', 'Google Drive API'],
			github: 'https://github.com/dhanujdev/ytcookhouse',
			demo: null,
			image: '/api/placeholder/600/400'
		},
		{
			title: 'Financial Enterprise Code Documentation Generator',
			description: 'Automated Documentation Pipeline – Co-developed enterprise tool analyzing multi-module Java codebases to generate UML diagrams, API documentation, and security reports with PII/PCI detection, deployed to Fortune 500 clients via Docker.',
			tech: ['Java', 'UML', 'Docker', 'SSL/TLS', 'PII/PCI Detection', 'API Documentation'],
			github: 'https://github.com/dhanujdev/codedocgen-gemini',
			demo: null,
			image: '/api/placeholder/600/400'
		},
		{
			title: 'DeepSeek-R1 Edge AI Research',
			description: 'Fine-tuned 70B parameter model for edge deployment using quantization techniques and 3D Printed Robot Chassis for real-world AI applications.',
			tech: ['Fine-tuning', 'Model Quantization', 'Edge AI', '3D Printing', '70B Parameters'],
			github: null,
			demo: null,
			image: '/api/placeholder/600/400'
		},
		{
			title: 'Go Offer E-commerce Platform',
			description: 'Engineered ML-driven product categorization system using Azure Computer Vision and Gemini Flash APIs to automatically classify and tag 1,500+ jewelry products, achieving 95% accuracy and reducing manual cataloging time by 80%.',
			tech: ['Azure Computer Vision', 'Gemini Flash API', 'Next.js', 'Node.js', 'PostgreSQL', 'ML Classification'],
			github: null,
			demo: 'https://jatin-jewellers-v2.vercel.app/gallery',
			image: '/api/placeholder/600/400'
		}
	]

	return (
		<section id="projects" className="py-20">
			<div className="container mx-auto container-padding">
				<motion.div
					initial={{ opacity: 0, y: 20 }}
					whileInView={{ opacity: 1, y: 0 }}
					transition={{ duration: 0.5 }}
					viewport={{ once: true }}
					className="max-w-6xl mx-auto"
				>
					<h2 className="text-3xl md:text-4xl font-bold text-center mb-12">
						Featured <span className="gradient-text">Projects</span>
					</h2>
					
					<div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
						{loading ? (
							// Loading skeleton
							Array.from({ length: 6 }).map((_, index) => (
								<Card key={index} className="h-full">
									<CardHeader>
										<div className="aspect-video bg-muted rounded-lg mb-4 animate-pulse" />
										<div className="h-6 bg-muted rounded animate-pulse mb-2" />
										<div className="h-4 bg-muted rounded animate-pulse" />
									</CardHeader>
									<CardContent>
										<div className="flex gap-2">
											<div className="h-6 w-16 bg-muted rounded animate-pulse" />
											<div className="h-6 w-20 bg-muted rounded animate-pulse" />
										</div>
									</CardContent>
								</Card>
							))
						) : githubRepos.length > 0 ? (
							// Display GitHub repos
							githubRepos.map((repo, index) => (
								<motion.div
									key={repo.id}
									initial={{ opacity: 0, y: 20 }}
									whileInView={{ opacity: 1, y: 0 }}
									transition={{ duration: 0.5, delay: index * 0.1 }}
									viewport={{ once: true }}
								>
									<Card className="h-full hover:shadow-lg transition-shadow duration-300">
										<CardHeader>
											<CardTitle className="text-xl flex items-center justify-between">
												{repo.name}
												<div className="flex items-center gap-2 text-sm text-muted-foreground">
													{repo.stargazers_count > 0 && (
														<div className="flex items-center gap-1">
															<Star className="h-4 w-4" />
															{repo.stargazers_count}
														</div>
													)}
													{repo.forks_count > 0 && (
														<div className="flex items-center gap-1">
															<GitFork className="h-4 w-4" />
															{repo.forks_count}
														</div>
													)}
												</div>
											</CardTitle>
											<CardDescription className="text-sm min-h-[3rem]">
												{repo.description || 'No description available'}
											</CardDescription>
										</CardHeader>
										
										<CardContent>
											<div className="flex flex-wrap gap-2">
												{repo.language && (
													<Badge variant="secondary" className="text-xs">
														<div 
															className="w-2 h-2 rounded-full mr-1" 
															style={{ backgroundColor: getLanguageColor(repo.language) }}
														/>
														{repo.language}
													</Badge>
												)}
												{repo.topics.slice(0, 3).map((topic) => (
													<Badge key={topic} variant="outline" className="text-xs">
														{topic}
													</Badge>
												))}
											</div>
										</CardContent>
										
										<CardFooter className="flex gap-2">
											<Button variant="outline" size="sm" asChild>
												<a href={repo.html_url} target="_blank" rel="noopener noreferrer">
													<Github className="mr-2 h-4 w-4" />
													Code
												</a>
											</Button>
											{repo.homepage && (
												<Button size="sm" asChild>
													<a href={repo.homepage} target="_blank" rel="noopener noreferrer">
														<ExternalLink className="mr-2 h-4 w-4" />
														Demo
													</a>
												</Button>
											)}
										</CardFooter>
									</Card>
								</motion.div>
							))
						) : (
							// Fallback to static projects
							projects.map((project, index) => (
								<motion.div
									key={project.title}
									initial={{ opacity: 0, y: 20 }}
									whileInView={{ opacity: 1, y: 0 }}
									transition={{ duration: 0.5, delay: index * 0.1 }}
									viewport={{ once: true }}
								>
									<Card className="h-full hover:shadow-lg transition-shadow duration-300">
										<CardHeader>
											<div className="aspect-video bg-muted rounded-lg mb-4 flex items-center justify-center">
												<span className="text-muted-foreground">Project Image</span>
											</div>
											<CardTitle className="text-xl">{project.title}</CardTitle>
											<CardDescription className="text-sm">
												{project.description}
											</CardDescription>
										</CardHeader>
										
										<CardContent>
											<div className="flex flex-wrap gap-2">
												{project.tech.map((tech) => (
													<Badge key={tech} variant="outline" className="text-xs">
														{tech}
													</Badge>
												))}
											</div>
										</CardContent>
										
										<CardFooter className="flex gap-2">
											{project.github && (
												<Button variant="outline" size="sm" asChild>
													<a href={project.github} target="_blank" rel="noopener noreferrer">
														<Github className="mr-2 h-4 w-4" />
														Code
													</a>
												</Button>
											)}
											{project.demo && (
												<Button size="sm" asChild>
													<a href={project.demo} target="_blank" rel="noopener noreferrer">
														<ExternalLink className="mr-2 h-4 w-4" />
														Demo
													</a>
												</Button>
											)}
										</CardFooter>
									</Card>
								</motion.div>
							))
						)}
					</div>
				</motion.div>
			</div>
		</section>
	)
}