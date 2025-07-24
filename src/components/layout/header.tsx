'use client'

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Menu, X, Moon, Sun } from 'lucide-react'
import { useTheme } from 'next-themes'

export function Header() {
	const [isMenuOpen, setIsMenuOpen] = useState(false)
	const [scrolled, setScrolled] = useState(false)
	const { theme, setTheme } = useTheme()

	useEffect(() => {
		const handleScroll = () => {
			setScrolled(window.scrollY > 50)
		}
		window.addEventListener('scroll', handleScroll)
		return () => window.removeEventListener('scroll', handleScroll)
	}, [])

	const navigation = [
		{ name: 'About', href: '#about' },
		{ name: 'Projects', href: '#projects' },
		{ name: 'Experience', href: '#experience' },
		{ name: 'Certifications', href: '#certifications' },
		{ name: 'Contact', href: '#contact' },
	]

	return (
		<header className={`fixed top-0 w-full z-50 transition-all duration-300 ${
			scrolled ? 'bg-background/80 backdrop-blur-md border-b' : 'bg-transparent'
		}`}>
			<div className="container mx-auto container-padding">
				<div className="flex items-center justify-between h-16">
					<div className="flex-shrink-0">
						<span className="text-xl font-bold gradient-text">Portfolio</span>
					</div>

					{/* Desktop Navigation */}
					<nav className="hidden md:block">
						<div className="flex items-center space-x-8">
							{navigation.map((item) => (
								<a
									key={item.name}
									href={item.href}
									className="text-foreground hover:text-primary transition-colors duration-200"
								>
									{item.name}
								</a>
							))}
						</div>
					</nav>

					<div className="flex items-center space-x-4">
						<Button
							variant="ghost"
							size="icon"
							onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
						>
							<Sun className="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
							<Moon className="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
							<span className="sr-only">Toggle theme</span>
						</Button>

						{/* Mobile menu button */}
						<Button
							variant="ghost"
							size="icon"
							className="md:hidden"
							onClick={() => setIsMenuOpen(!isMenuOpen)}
						>
							{isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
						</Button>
					</div>
				</div>

				{/* Mobile Navigation */}
				{isMenuOpen && (
					<div className="md:hidden">
						<div className="px-2 pt-2 pb-3 space-y-1 bg-background/95 backdrop-blur-md rounded-lg mt-2">
							{navigation.map((item) => (
								<a
									key={item.name}
									href={item.href}
									className="block px-3 py-2 text-foreground hover:text-primary transition-colors duration-200"
									onClick={() => setIsMenuOpen(false)}
								>
									{item.name}
								</a>
							))}
						</div>
					</div>
				)}
			</div>
		</header>
	)
}