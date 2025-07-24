'use client'

import { HeroSection } from '@/components/sections/hero-section'
import { AboutSection } from '@/components/sections/about-section'
import { ProjectsSection } from '@/components/sections/projects-section'
import { ExperienceSection } from '@/components/sections/experience-section'
import { CertificationsSection } from '@/components/sections/certifications-section'
import { ContactSection } from '@/components/sections/contact-section'
import { Header } from '@/components/layout/header'
import { Footer } from '@/components/layout/footer'

export default function Home() {
	return (
		<div className="min-h-screen bg-background">
			<Header />
			<main>
				<HeroSection />
				<AboutSection />
				<ProjectsSection />
				<ExperienceSection />
				<CertificationsSection />
				<ContactSection />
			</main>
			<Footer />
		</div>
	)
}