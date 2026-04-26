import requests

class GitHubService:

    BASE_URL = "https://api.github.com"

    def get_repo_info(self, owner, repo):
        url = f"{self.BASE_URL}/repos/{owner}/{repo}"
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception("Failed to fetch repo")

        data = response.json()

        return {
            "name": data["name"],
            "stars": data["stargazers_count"],
            "language": data["language"],
        }

    def get_issues(self, owner, repo):
        url = f"{self.BASE_URL}/repos/{owner}/{repo}"
        response = requests.get(url)

        data = response.json()

        return {
            "open": data["open_issues_count"],
            "note": "Includes pull requests also"
    }

    def get_pull_requests(self, owner, repo):
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/pulls"

        open_prs = requests.get(url, params={"state": "open"})
        closed_prs = requests.get(url, params={"state": "closed"})

        return {
            "open": len(open_prs.json()),
            "closed": len(closed_prs.json())
        }
    
    def get_contributors(self, owner, repo):
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/contributors"

        response = requests.get(url, params={"per_page": 5})
        data = response.json()

        return [
            {
                "username": user["login"],
                "contributions": user["contributions"]
            }
            for user in data
        ]
    
    def get_commits(self, owner, repo):
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/commits"

        response = requests.get(url, params={"per_page": 5})
        data = response.json()

        return [
            {
                "message": commit["commit"]["message"].split("\n")[0],
                "author": commit["commit"]["author"]["name"]
            }
            for commit in data
        ]