from django.shortcuts import render
from core.services.github_service import GitHubService
from core.services.ai_service import AIService

def home(request):
    if request.method == "POST":
        repo_url = request.POST.get("repo_url")

        try:
            from core.models import RepositoryAnalysis
            
            gh = GitHubService()
            ai = AIService()

            data = gh.get_all_data(repo_url)

            summary = ai.summarize_repo(data)
            rating = ai.rate_repo(data)
            suggestions = ai.get_suggestions(data)

            data["summary"] = summary
            data["rating"] = rating
            data["suggestions"] = suggestions

            # 🔥 SAVE TO DATABASE
            RepositoryAnalysis.objects.update_or_create(
                repo_url=repo_url,
                defaults={
                    "name": data["repo"]["name"],
                    "stars": data["repo"]["stars"],
                    "language": data["repo"]["language"],
                    "issues": data["issues"]["open"],
                    "summary": summary,
                    "rating": rating,
                }
            )

            return render(request, "index.html", data)

        except Exception as e:
            return render(request, "index.html", {"error": str(e)})

    return render(request, "index.html")