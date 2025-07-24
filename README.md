# Dhanuj Gumpella - Portfolio Website

A responsive, modern portfolio website showcasing my experience as a Software Engineer AI, built with Next.js 14, TypeScript, and Tailwind CSS. Features dark/light theme toggle, GitHub integration, and comprehensive project showcase.

## ✨ Features

- **Responsive Design** - Works perfectly on desktop, tablet, and mobile
- **Dark/Light Theme** - Toggle between themes with smooth transitions  
- **Smooth Animations** - Framer Motion powered animations and transitions
- **GitHub Integration** - Automatically fetches and displays repositories from dhanujdev
- **Modern UI Components** - Built with Radix UI and shadcn/ui
- **TypeScript** - Full type safety throughout the application
- **Real Project Showcase** - Features actual projects including AI/ML systems, RAG architectures, and enterprise tools
- **Professional Sections** - Complete experience, certifications, and technical expertise
- **SEO Optimized** - Meta tags and structured data for better search visibility
- **Fast Performance** - Optimized with Next.js 14 and static export

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. Clone the repository:
\`\`\`bash
git clone <your-repo-url>
cd Portfolio
\`\`\`

2. Install dependencies:
\`\`\`bash
npm install
# or
yarn install
\`\`\`

3. Start the development server:
\`\`\`bash
npm run dev
# or
yarn dev
\`\`\`

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## 🛠️ Customization

### Personal Information

Update the following files with your information:

- \`src/app/layout.tsx\` - Meta title and description
- \`src/components/sections/hero-section.tsx\` - Name and introduction
- \`src/components/sections/about-section.tsx\` - About text and skills
- \`src/components/sections/projects-section.tsx\` - Your projects
- \`src/components/sections/experience-section.tsx\` - Work experience and education
- \`src/components/sections/contact-section.tsx\` - Contact information
- \`src/components/layout/footer.tsx\` - Social media links

### Styling

The project uses Tailwind CSS with a custom design system. Colors and spacing can be customized in:

- \`tailwind.config.js\` - Tailwind configuration
- \`src/app/globals.css\` - CSS variables and custom styles

### Adding New Sections

1. Create a new component in \`src/components/sections/\`
2. Import and add it to \`src/app/page.tsx\`
3. Add navigation link in \`src/components/layout/header.tsx\`

## 📦 Build and Deploy

### Build for Production

\`\`\`bash
npm run build
\`\`\`

The project is configured for static export, generating files in the \`out/\` directory.

### Deploy to Vercel

1. Push your code to GitHub
2. Connect your repository to [Vercel](https://vercel.com)
3. Deploy with zero configuration

### Deploy to Netlify

1. Build the project: \`npm run build\`
2. Upload the \`out/\` directory to [Netlify](https://netlify.com)

### Deploy to GitHub Pages

1. Update \`next.config.js\` with your repository name
2. Build and push the \`out/\` directory to the \`gh-pages\` branch

## 🧰 Tech Stack

- **Framework:** Next.js 14
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **UI Components:** Radix UI + shadcn/ui
- **Animations:** Framer Motion
- **Theme:** next-themes
- **Icons:** Lucide React

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](../../issues).

## 📞 Support

If you have any questions or need help customizing the portfolio, feel free to reach out!

---

Built with ❤️ using Next.js and TypeScript