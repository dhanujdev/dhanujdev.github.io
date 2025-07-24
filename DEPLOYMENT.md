# Deployment Guide

## 🚀 Deploy to Vercel (Recommended)

Vercel is the easiest way to deploy your Next.js portfolio.

### Option 1: Deploy via Vercel Dashboard

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial portfolio setup"
   git branch -M main
   git remote add origin https://github.com/yourusername/portfolio.git
   git push -u origin main
   ```

2. **Connect to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Sign up/login with your GitHub account
   - Click "New Project"
   - Import your portfolio repository
   - Click "Deploy"

3. **Custom Domain (Optional)**
   - Go to your project settings in Vercel
   - Add your custom domain
   - Update DNS settings as instructed

### Option 2: Deploy via Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Deploy**
   ```bash
   vercel
   ```

3. **Follow the prompts**
   - Link to existing project or create new
   - Set up project settings
   - Deploy

## 🌐 Deploy to Netlify

1. **Build the project**
   ```bash
   npm run build
   ```

2. **Deploy via Netlify CLI**
   ```bash
   npm install -g netlify-cli
   netlify deploy --prod --dir=out
   ```

3. **Or drag & drop**
   - Go to [netlify.com](https://netlify.com)
   - Drag the \`out/\` folder to the deploy area

## 📱 Deploy to GitHub Pages

1. **Update next.config.js** (if using custom domain)
   ```javascript
   const nextConfig = {
     output: 'export',
     trailingSlash: true,
     images: {
       unoptimized: true
     },
     basePath: '/your-repo-name', // Only if using username.github.io/repo-name
     assetPrefix: '/your-repo-name/', // Only if using username.github.io/repo-name
   }
   ```

2. **Build and deploy**
   ```bash
   npm run build
   
   # Push the out/ directory to gh-pages branch
   git add out/
   git commit -m "Deploy to GitHub Pages"
   git subtree push --prefix out origin gh-pages
   ```

3. **Enable GitHub Pages**
   - Go to repository Settings
   - Scroll to Pages section
   - Set source to "Deploy from a branch"
   - Select "gh-pages" branch

## 🔧 Environment Variables

If you're using any API keys or environment variables:

1. **Create .env.local** (for local development)
   ```env
   NEXT_PUBLIC_GITHUB_USERNAME=yourusername
   NEXT_PUBLIC_EMAIL=your.email@example.com
   ```

2. **Add to Vercel**
   - Go to project settings
   - Add environment variables
   - Redeploy

## 📈 Performance Tips

1. **Optimize images**: Use Next.js Image component for better performance
2. **Enable compression**: Vercel handles this automatically
3. **Use CDN**: Vercel provides global CDN out of the box
4. **Monitor**: Use Vercel Analytics or Google Analytics

## 🔍 SEO Optimization

1. **Update metadata** in \`src/app/layout.tsx\`
2. **Add structured data** for better search results
3. **Create sitemap** (optional for portfolios)
4. **Submit to Google Search Console**

## 📊 Analytics

### Google Analytics
1. Create GA4 property
2. Add tracking code to layout.tsx
3. Track page views and interactions

### Vercel Analytics
1. Enable in Vercel dashboard
2. View performance metrics
3. Monitor Core Web Vitals

## 🛠️ Troubleshooting

### Common Issues

**Build fails with TypeScript errors:**
```bash
npm run build
# Fix any TypeScript errors shown
```

**Images not loading:**
- Ensure \`unoptimized: true\` in next.config.js for static export
- Use absolute paths for images

**Routing issues:**
- Enable \`trailingSlash: true\` for static hosting
- Check basePath configuration for subdirectory hosting

**API calls failing:**
- GitHub API has rate limits for unauthenticated requests
- Consider adding GitHub token for higher limits

---

**Need help?** Check the [Next.js deployment docs](https://nextjs.org/docs/deployment) or create an issue in the repository.