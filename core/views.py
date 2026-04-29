from django.shortcuts import render
from core.services.github_service import GitHubService
from core.services.ai_service import AIService

def home(request):
    if request.method == "POST":
        repo_url = request.POST.get("repo_url")

        try:
            gh = GitHubService()
            ai = AIService()

            data = gh.get_all_data(repo_url)

            summary = ai.summarize_repo(data)

            data["summary"] = summary

            return render(request, "index.html", data)

        except Exception as e:
            return render(request, "index.html", {"error": str(e)})

    return render(request, "index.html")