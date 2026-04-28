from django.shortcuts import render
from core.services.github_service import GitHubService

def home(request):
    if request.method == "POST":
        repo_url = request.POST.get("repo_url")

        try:
            gh = GitHubService()
            data = gh.get_all_data(repo_url)

            return render(request, "index.html", data)

        except Exception as e:
            return render(request, "index.html", {"error": str(e)})

    return render(request, "index.html")