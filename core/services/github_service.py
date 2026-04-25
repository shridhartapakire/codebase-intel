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