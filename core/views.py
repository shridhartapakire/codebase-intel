from django.shortcuts import render
from core.services.github_service import GitHubService

def home(request):
    if request.method == "POST":
        repo_url = request.POST.get("repo_url")

        # extract owner and repo
        parts = repo_url.rstrip("/").split("/")
        owner = parts[-2]
        repo = parts[-1]

        gh = GitHubService()
        data = gh.get_repo_info(owner, repo)

        return render(request, "index.html", {"data": data})

    return render(request, "index.html")