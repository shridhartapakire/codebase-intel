from django.shortcuts import render
from core.services.github_service import GitHubService

def home(request):
    if request.method == "POST":
        repo_url = request.POST.get("repo_url")

        try:
            parts = repo_url.rstrip("/").split("/")
            owner = parts[-2]
            repo = parts[-1]

            gh = GitHubService()

            repo_data = gh.get_repo_info(owner, repo)
            issues = gh.get_issues(owner, repo)
            prs = gh.get_pull_requests(owner, repo)
            contributors = gh.get_contributors(owner, repo)
            commits = gh.get_commits(owner, repo)

            return render(request, "index.html", {
                "data": repo_data,
                "issues": issues,
                "prs": prs,
                "contributors": contributors,
                "commits": commits
            })

        except Exception as e:
            return render(request, "index.html", {
                "error": str(e)
            })

    return render(request, "index.html")