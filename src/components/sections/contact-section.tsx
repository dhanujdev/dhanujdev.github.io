'use client'

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Mail, MessageSquare, Phone, MapPin } from 'lucide-react'
import { motion } from 'framer-motion'

export function ContactSection() {
	const contactInfo = [
		{
			icon: Mail,
			title: 'Email',
			description: 'dhanujsportfolio@gmail.com',
			href: 'mailto:dhanujsportfolio@gmail.com'
		},
		{
			icon: Phone,
			title: 'Phone',
			description: '+1 (551) 253-8297',
			href: 'tel:+15512538297'
		},
		{
			icon: MapPin,
			title: 'Location',
			description: 'Brooklyn, NY',
			href: null
		}
	]

	return (
		<section id="contact" className="py-20">
			<div className="container mx-auto container-padding">
				<motion.div
					initial={{ opacity: 0, y: 20 }}
					whileInView={{ opacity: 1, y: 0 }}
					transition={{ duration: 0.5 }}
					viewport={{ once: true }}
					className="max-w-4xl mx-auto"
				>
					<h2 className="text-3xl md:text-4xl font-bold text-center mb-12">
						Get In <span className="gradient-text">Touch</span>
					</h2>
					
					<div className="grid md:grid-cols-2 gap-12">
						<motion.div
							initial={{ opacity: 0, x: -20 }}
							whileInView={{ opacity: 1, x: 0 }}
							transition={{ duration: 0.5, delay: 0.1 }}
							viewport={{ once: true }}
						>
							<div className="space-y-6">
								<div>
									<h3 className="text-2xl font-semibold mb-4">Let's work together</h3>
									<p className="text-lg text-muted-foreground leading-relaxed">
										I'm always interested in hearing about new opportunities and exciting projects. 
										Whether you have a question or just want to say hi, I'll try my best to get back to you!
									</p>
								</div>
								
								<div className="space-y-4">
									{contactInfo.map((info, index) => (
										<motion.div
											key={info.title}
											initial={{ opacity: 0, y: 10 }}
											whileInView={{ opacity: 1, y: 0 }}
											transition={{ duration: 0.3, delay: 0.2 + index * 0.1 }}
											viewport={{ once: true }}
											className="flex items-center space-x-4"
										>
											<div className="flex-shrink-0">
												<div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
													<info.icon className="h-6 w-6 text-primary" />
												</div>
											</div>
											<div>
												<h4 className="font-medium">{info.title}</h4>
												{info.href ? (
													<a 
														href={info.href}
														className="text-muted-foreground hover:text-primary transition-colors"
													>
														{info.description}
													</a>
												) : (
													<p className="text-muted-foreground">{info.description}</p>
												)}
											</div>
										</motion.div>
									))}
								</div>
							</div>
						</motion.div>
						
						<motion.div
							initial={{ opacity: 0, x: 20 }}
							whileInView={{ opacity: 1, x: 0 }}
							transition={{ duration: 0.5, delay: 0.2 }}
							viewport={{ once: true }}
						>
							<Card>
								<CardHeader>
									<CardTitle className="flex items-center gap-2">
										<MessageSquare className="h-5 w-5" />
										Send a Message
									</CardTitle>
									<CardDescription>
										Fill out the form below and I'll get back to you as soon as possible.
									</CardDescription>
								</CardHeader>
								<CardContent>
									<form className="space-y-4">
										<div>
											<label htmlFor="name" className="block text-sm font-medium mb-2">
												Name
											</label>
											<input
												type="text"
												id="name"
												name="name"
												className="w-full px-3 py-2 border border-input rounded-md bg-background focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent"
												placeholder="Your name"
											/>
										</div>
										<div>
											<label htmlFor="email" className="block text-sm font-medium mb-2">
												Email
											</label>
											<input
												type="email"
												id="email"
												name="email"
												className="w-full px-3 py-2 border border-input rounded-md bg-background focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent"
												placeholder="your.email@example.com"
											/>
										</div>
										<div>
											<label htmlFor="message" className="block text-sm font-medium mb-2">
												Message
											</label>
											<textarea
												id="message"
												name="message"
												rows={4}
												className="w-full px-3 py-2 border border-input rounded-md bg-background focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent resize-none"
												placeholder="Your message..."
											/>
										</div>
										<Button type="submit" className="w-full">
											Send Message
										</Button>
									</form>
								</CardContent>
							</Card>
						</motion.div>
					</div>
				</motion.div>
			</div>
		</section>
	)
}