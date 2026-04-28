import os
import requests
from dotenv import load_dotenv

load_dotenv()


class GitHubService:

    BASE_URL = "https://api.github.com"

    def __init__(self):
        token = os.getenv("GITHUB_TOKEN")
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
        }

    def _get(self, endpoint, params=None):
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 404:
            raise ValueError("Repository not found")
        if response.status_code == 403:
            raise ValueError("Rate limit exceeded or bad token")
        if response.status_code != 200:
            raise ValueError(f"GitHub error: {response.status_code}")

        return response.json()

    def parse_repo_url(self, url):
        url = url.rstrip("/")
        parts = url.replace("https://github.com/", "").split("/")

        if len(parts) != 2:
            raise ValueError("Invalid GitHub URL")

        return parts[0], parts[1]

    def get_repo_info(self, owner, repo):
        data = self._get(f"/repos/{owner}/{repo}")

        return {
            "name": data["name"],
            "stars": data["stargazers_count"],
            "language": data.get("language", "Unknown"),
        }

    def get_issues(self, owner, repo):
        data = self._get(f"/repos/{owner}/{repo}")

        return {
            "open": data["open_issues_count"]
        }

    def get_pull_requests(self, owner, repo):
        open_prs = self._get(f"/repos/{owner}/{repo}/pulls", {"state": "open"})
        closed_prs = self._get(f"/repos/{owner}/{repo}/pulls", {"state": "closed"})

        return {
            "open": len(open_prs),
            "closed": len(closed_prs),
        }

    def get_contributors(self, owner, repo):
        data = self._get(f"/repos/{owner}/{repo}/contributors", {"per_page": 5})

        return [
            {
                "username": c["login"],
                "contributions": c["contributions"],
            }
            for c in data
        ]

    def get_commits(self, owner, repo):
        data = self._get(f"/repos/{owner}/{repo}/commits", {"per_page": 5})

        return [
            {
                "message": c["commit"]["message"].split("\n")[0],
                "author": c["commit"]["author"]["name"],
            }
            for c in data
        ]

    def get_all_data(self, repo_url):
        owner, repo = self.parse_repo_url(repo_url)

        return {
            "repo": self.get_repo_info(owner, repo),
            "issues": self.get_issues(owner, repo),
            "prs": self.get_pull_requests(owner, repo),
            "contributors": self.get_contributors(owner, repo),
            "commits": self.get_commits(owner, repo),
        }