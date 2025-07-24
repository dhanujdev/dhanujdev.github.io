import { Github, Linkedin, Mail, Twitter } from 'lucide-react'
import { Button } from '@/components/ui/button'

export function Footer() {
	const socialLinks = [
		{ icon: Github, href: 'https://github.com/dhanujdev', label: 'GitHub' },
		{ icon: Linkedin, href: 'https://linkedin.com/in/dhanuj-gumpella', label: 'LinkedIn' },
		{ icon: Mail, href: 'mailto:dhanujsportfolio@gmail.com', label: 'Email' },
	]

	return (
		<footer className="bg-background border-t">
			<div className="container mx-auto container-padding py-8">
				<div className="flex flex-col md:flex-row justify-between items-center">
					<div className="text-center md:text-left mb-4 md:mb-0">
						<p className="text-muted-foreground">
							© 2024 Dhanuj Gumpella. All rights reserved.
						</p>
					</div>
					
					<div className="flex space-x-4">
						{socialLinks.map((link) => (
							<Button
								key={link.label}
								variant="ghost"
								size="icon"
								asChild
							>
								<a href={link.href} target="_blank" rel="noopener noreferrer">
									<link.icon className="h-5 w-5" />
									<span className="sr-only">{link.label}</span>
								</a>
							</Button>
						))}
					</div>
				</div>
				
				<div className="mt-8 pt-8 border-t text-center">
					<p className="text-sm text-muted-foreground">
						Built with Next.js, TypeScript, and Tailwind CSS
					</p>
				</div>
			</div>
		</footer>
	)
}