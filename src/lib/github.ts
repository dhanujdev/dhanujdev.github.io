// GitHub API integration for fetching repositories and user data

export interface GitHubRepo {
	id: number
	name: string
	full_name: string
	description: string | null
	html_url: string
	language: string | null
	stargazers_count: number
	forks_count: number
	topics: string[]
	created_at: string
	updated_at: string
	homepage: string | null
}

export interface GitHubUser {
	login: string
	name: string | null
	bio: string | null
	location: string | null
	blog: string | null
	twitter_username: string | null
	public_repos: number
	followers: number
	following: number
	avatar_url: string
}

const GITHUB_API_BASE = 'https://api.github.com'

export async function fetchGitHubUser(username: string): Promise<GitHubUser | null> {
	try {
		const response = await fetch(`${GITHUB_API_BASE}/users/${username}`)
		if (!response.ok) return null
		return await response.json()
	} catch (error) {
		console.error('Error fetching GitHub user:', error)
		return null
	}
}

export async function fetchGitHubRepos(
	username: string,
	options: {
		sort?: 'created' | 'updated' | 'pushed' | 'full_name'
		direction?: 'asc' | 'desc'
		per_page?: number
		type?: 'all' | 'owner' | 'member'
	} = {}
): Promise<GitHubRepo[]> {
	try {
		const params = new URLSearchParams({
			sort: options.sort || 'updated',
			direction: options.direction || 'desc',
			per_page: (options.per_page || 6).toString(),
			type: options.type || 'owner'
		})

		const response = await fetch(`${GITHUB_API_BASE}/users/${username}/repos?${params}`)
		if (!response.ok) return []
		
		const repos: GitHubRepo[] = await response.json()
		return repos.filter(repo => !repo.name.includes('.github.io') && repo.name !== username)
	} catch (error) {
		console.error('Error fetching GitHub repos:', error)
		return []
	}
}

export async function fetchPinnedRepos(username: string): Promise<GitHubRepo[]> {
	// Note: GitHub doesn't provide a public API for pinned repos
	// This function could be extended to use GraphQL API with authentication
	// For now, we'll fetch recent public repos as a fallback
	return fetchGitHubRepos(username, { per_page: 6 })
}

export function getLanguageColor(language: string | null): string {
	const colors: Record<string, string> = {
		JavaScript: '#f1e05a',
		TypeScript: '#2b7489',
		Python: '#3572A5',
		Java: '#b07219',
		'C++': '#f34b7d',
		C: '#555555',
		'C#': '#239120',
		PHP: '#4F5D95',
		Ruby: '#701516',
		Go: '#00ADD8',
		Rust: '#dea584',
		Swift: '#ffac45',
		Kotlin: '#F18E33',
		Dart: '#00B4AB',
		HTML: '#e34c26',
		CSS: '#1572B6',
		Vue: '#2c3e50',
		React: '#61DAFB',
		Angular: '#DD0031',
		Svelte: '#ff3e00',
	}
	
	return colors[language || ''] || '#8b949e'
}