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
	const [error, setError] = useState<string | null>(null)
	const [showGithubRepos, setShowGithubRepos] = useState(false)

	// Replace 'yourusername' with your actual GitHub username
	const GITHUB_USERNAME = 'dhanujdev'

	useEffect(() => {
		async function loadRepos() {
			try {
				setError(null)
				const repos = await fetchGitHubRepos(GITHUB_USERNAME, { per_page: 6 })
				if (repos.length > 0) {
					setGithubRepos(repos)
					setShowGithubRepos(true)
				}
			} catch (err) {
				setError('Unable to load GitHub repositories')
				console.warn('GitHub API error:', err)
			}
			setLoading(false)
		}
		loadRepos()
	}, [])

	// Featured projects with enhanced descriptions and outcomes
	const featuredProjects = [
		{
			title: 'AI Resume Tailoring SaaS Platform',
			description: 'Production SaaS platform implementing RAG architecture to store and index user professional data in Supabase vector database. Enables context-aware resume generation with 95% ATS match scores.',
			longDescription: 'Built a comprehensive system that reduces job application time from 30 minutes to 2 minutes per application through AI-powered DOM analysis and Chrome extension integration.',
			outcome: '95% ATS match scores, 93% time reduction',
			tech: ['RAG', 'Supabase', 'Vector Database', 'Chrome Extension', 'AI/ML', 'DOM Analysis'],
			github: 'https://github.com/dhanujdev/AI-Powered-Resume-Tailor',
			demo: null,
			category: 'AI/ML',
			featured: true
		},
		{
			title: 'YouTube Content Automation Pipeline',
			description: 'End-to-end LangChain-based agentic pipeline using FastAPI to automate YouTube content creation with AI voice generation and video processing.',
			longDescription: 'Automated entire YouTube workflow: scans Google Drive for raw clips, merges with background music using FFmpeg, generates metadata, creates AI voiceovers in local languages via Gemini API.',
			outcome: 'Full automation of video content pipeline',
			tech: ['LangChain', 'FastAPI', 'FFmpeg', 'Gemini', 'YouTube Data API', 'OAuth2', 'Google Drive API'],
			github: 'https://github.com/dhanujdev/ytcookhouse',
			demo: null,
			category: 'AI/ML',
			featured: true
		},
		{
			title: 'Enterprise Code Documentation Generator',
			description: 'Automated documentation pipeline for Fortune 500 clients analyzing multi-module Java codebases to generate UML diagrams, API docs, and security reports.',
			longDescription: 'Co-developed enterprise tool with PII/PCI detection capabilities, handling 100K+ lines of code per analysis. Deployed via Docker with SSL/TLS security for enterprise clients.',
			outcome: 'Deployed to Fortune 500 clients, 100K+ LOC analysis',
			tech: ['Java', 'UML', 'Docker', 'SSL/TLS', 'PII/PCI Detection', 'API Documentation'],
			github: 'https://github.com/dhanujdev/codedocgen-gemini',
			demo: null,
			category: 'Enterprise',
			featured: true
		},
		{
			title: 'NYC Citizen Services AI Platform',
			description: 'Production AI system serving 8M+ NYC residents through intelligent document workflows and RAG-powered policy lookup.',
			longDescription: 'Led Azure ML infrastructure modernization achieving 99.9% uptime while processing 100K+ daily requests. Built production RAG pipeline reducing policy lookup time by 60%.',
			outcome: '8M+ users served, 60% time reduction, 99.9% uptime',
			tech: ['Azure ML', 'RAG', 'GPT-4', 'Databricks', 'AKS', 'Production Scale'],
			github: null,
			demo: null,
			category: 'Government',
			featured: true
		},
		{
			title: 'E-commerce ML Product Categorization',
			description: 'ML-driven product categorization system using Azure Computer Vision and Gemini Flash APIs for automated jewelry product classification.',
			longDescription: 'Built scalable system that automatically classifies and tags 1,500+ jewelry products with 95% accuracy, reducing manual cataloging time by 80% for retail clients.',
			outcome: '95% accuracy, 80% time reduction, 1,500+ products',
			tech: ['Azure Computer Vision', 'Gemini Flash API', 'Next.js', 'Node.js', 'PostgreSQL', 'ML Classification'],
			github: null,
			demo: 'https://jatin-jewellers-v2.vercel.app/gallery',
			category: 'E-commerce',
			featured: true
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

					{/* Show loading or error states */}
					{loading && (
						<div className="text-center mb-8">
							<p className="text-muted-foreground">Loading GitHub repositories...</p>
						</div>
					)}
					
					{error && (
						<div className="text-center mb-8">
							<p className="text-muted-foreground text-sm">{error} - Showing featured projects</p>
						</div>
					)}

					{/* GitHub Repositories Section */}
					{showGithubRepos && githubRepos.length > 0 && (
						<div className="mb-16">
							<h3 className="text-2xl font-semibold text-center mb-8 text-primary">
								Latest from GitHub
							</h3>
							<div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
								{githubRepos.slice(0, 3).map((repo, index) => (
									<motion.div
										key={repo.id}
										initial={{ opacity: 0, y: 20 }}
										whileInView={{ opacity: 1, y: 0 }}
										transition={{ duration: 0.5, delay: index * 0.1 }}
										viewport={{ once: true }}
									>
										<Card className="h-full hover:shadow-lg transition-all duration-300 hover:-translate-y-1">
											<CardHeader>
												<CardTitle className="text-lg flex items-center justify-between">
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
												<CardDescription className="text-sm">
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
								))}
							</div>
						</div>
					)}

					{/* Featured Projects Section */}
					<div>
						<h3 className="text-2xl font-semibold text-center mb-8 text-primary">
							Key Projects & Achievements
						</h3>
						<div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
							{featuredProjects.map((project, index) => (
								<motion.div
									key={project.title}
									initial={{ opacity: 0, y: 20 }}
									whileInView={{ opacity: 1, y: 0 }}
									transition={{ duration: 0.5, delay: index * 0.1 }}
									viewport={{ once: true }}
								>
									<Card className="h-full hover:shadow-lg transition-all duration-300 hover:-translate-y-1 border-l-4 border-l-primary/50">
										<CardHeader>
											<div className="flex items-center justify-between mb-2">
												<Badge variant="secondary" className="text-xs">
													{project.category}
												</Badge>
												{project.featured && (
													<Badge variant="default" className="text-xs">
														Featured
													</Badge>
												)}
											</div>
											<CardTitle className="text-xl mb-2">{project.title}</CardTitle>
											<CardDescription className="text-sm mb-3">
												{project.description}
											</CardDescription>
											{project.outcome && (
												<div className="bg-muted/50 rounded-lg px-3 py-2 mb-3">
													<p className="text-xs font-medium text-primary">
														✨ Key Results: {project.outcome}
													</p>
												</div>
											)}
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
							))}
						</div>
					</div>
				</motion.div>
			</div>
		</section>
	)
}