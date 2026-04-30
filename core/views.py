from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render
from core.services.github_service import GitHubService
from core.services.ai_service import AIService
from core.models import RepositoryAnalysis

def home(request):

    repo_url = request.GET.get("repo_url")

    if request.method == "POST" or repo_url:
        repo_url = request.POST.get("repo_url") or request.GET.get("repo_url")

        try:
            gh = GitHubService()
            ai = AIService()

            # 🔥 STEP 1: Check DB first
            existing = RepositoryAnalysis.objects.filter(repo_url=repo_url).first()

            is_fresh = False

            if existing:
                time_diff = timezone.now() - existing.updated_at
                if time_diff < timedelta(hours=1):
                    is_fresh = True

            if existing and is_fresh:
                # ✅ Load from DB (FAST)
                data = {
                    "repo": {
                        "name": existing.name,
                        "stars": existing.stars,
                        "language": existing.language,
                    },
                    "issues": {"open": existing.issues},
                    "summary": existing.summary,
                    "rating": existing.rating,
                }
                suggestions = [] 
                data["suggestions"] = suggestions

            else:
                # ❌ Not in DB → Call API
                data = gh.get_all_data(repo_url)

                summary = ai.summarize_repo(data)
                rating = ai.rate_repo(data)
                suggestions = ai.get_suggestions(data)

                data["summary"] = summary
                data["rating"] = rating
                data["suggestions"] = suggestions

                # 🔥 Save to DB
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

            analyses = RepositoryAnalysis.objects.order_by("-created_at")[:5]
            data["analyses"] = analyses

            return render(request, "index.html", data)

        except Exception as e:
            analyses = RepositoryAnalysis.objects.order_by("-created_at")[:5]

            return render(request, "index.html", {
                "error": str(e),
                "analyses": analyses
            })

    analyses = RepositoryAnalysis.objects.order_by("-created_at")[:5]
    return render(request, "index.html", {"analyses": analyses})