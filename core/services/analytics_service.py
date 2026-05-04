class AnalyticsService:

    def calculate_health_score(self, data):
        score = 0

        stars = data["repo"]["stars"]
        issues = data["issues"]["open"]
        prs = data["prs"]["open"]
        contributors = len(data["contributors"])
        commits = len(data["commits"])

        # ⭐ Stars (popularity)
        if stars > 50000:
            score += 30
        elif stars > 10000:
            score += 20
        elif stars > 1000:
            score += 10

        # 🐞 Issues (lower is better)
        if issues < 50:
            score += 20
        elif issues < 200:
            score += 10

        # 🔀 PRs (activity)
        if prs > 20:
            score += 15
        elif prs > 5:
            score += 8

        # 👥 Contributors
        if contributors > 10:
            score += 15
        elif contributors > 3:
            score += 8

        # 📦 Commits (recent activity)
        if commits > 5:
            score += 20
        elif commits > 2:
            score += 10

        return min(score, 100)

    def get_health_label(self, score):
        if score >= 80:
            return "Excellent"
        elif score >= 60:
            return "Good"
        elif score >= 40:
            return "Average"
        else:
            return "Poor"