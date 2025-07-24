'use client'

import { Badge } from '@/components/ui/badge'
import { Card, CardContent } from '@/components/ui/card'
import { motion } from 'framer-motion'

export function AboutSection() {
	const skills = {
		'AI & ML Engineering': ['LangChain', 'LangGraph', 'Gemini', 'OpenAI/Anthropic APIs', 'RAG Architectures', 'Vector Databases', 'Hugging Face Transformers', 'PyTorch', 'TensorFlow', 'Fine-tuning'],
		'Programming & Frameworks': ['Python', 'TypeScript/JavaScript', 'Java', 'C++', 'FastAPI', 'Next.js/React', 'Spring Boot', 'Node.js', 'Chrome Extensions'],
		'Cloud & MLOps': ['Azure ML', 'Azure AKS', 'AWS Bedrock', 'AWS SageMaker', 'Docker', 'CI/CD', 'LangSmith', 'Vercel'],
		'Data & Infrastructure': ['PostgreSQL', 'pgvector', 'Pinecone', 'Weaviate', 'Firebase/Supabase', 'OAuth2', 'JWT', 'TLS Protocols']
	}

	return (
		<section id="about" className="py-20 bg-muted/30">
			<div className="container mx-auto container-padding">
				<motion.div
					initial={{ opacity: 0, y: 20 }}
					whileInView={{ opacity: 1, y: 0 }}
					transition={{ duration: 0.5 }}
					viewport={{ once: true }}
					className="max-w-4xl mx-auto"
				>
					<h2 className="text-3xl md:text-4xl font-bold text-center mb-12">
						About <span className="gradient-text">Me</span>
					</h2>
					
					<div className="grid md:grid-cols-2 gap-12 items-center">
						<motion.div
							initial={{ opacity: 0, x: -20 }}
							whileInView={{ opacity: 1, x: 0 }}
							transition={{ duration: 0.5, delay: 0.1 }}
							viewport={{ once: true }}
						>
							<div className="space-y-6">
								<p className="text-lg text-muted-foreground leading-relaxed">
									I'm a Software Engineer AI at NYC Department of Social Services, modernizing 
									citizen-services platforms serving 8M+ NYC residents through AI-powered automation. 
									I specialize in production-scale AI systems, RAG architectures, and cloud infrastructure.
								</p>
								<p className="text-lg text-muted-foreground leading-relaxed">
									With a Master's in Computer Science from University of North Texas and extensive 
									experience in ML/AI engineering, I've led Azure ML infrastructure modernization, 
									built production RAG pipelines, and automated ML model lifecycles from development 
									to deployment.
								</p>
								<p className="text-lg text-muted-foreground leading-relaxed">
									I'm passionate about leveraging cutting-edge AI technologies to solve real-world 
									problems and create impactful solutions that improve people's lives.
								</p>
							</div>
						</motion.div>
						
						<motion.div
							initial={{ opacity: 0, x: 20 }}
							whileInView={{ opacity: 1, x: 0 }}
							transition={{ duration: 0.5, delay: 0.2 }}
							viewport={{ once: true }}
							className="space-y-6"
						>
							{Object.entries(skills).map(([category, skillList], index) => (
								<Card key={category}>
									<CardContent className="p-6">
										<h3 className="font-semibold mb-3 text-primary">{category}</h3>
										<div className="flex flex-wrap gap-2">
											{skillList.map((skill) => (
												<Badge key={skill} variant="secondary">
													{skill}
												</Badge>
											))}
										</div>
									</CardContent>
								</Card>
							))}
						</motion.div>
					</div>
				</motion.div>
			</div>
		</section>
	)
}