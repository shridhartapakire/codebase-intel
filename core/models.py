from django.db import models

class RepositoryAnalysis(models.Model):
    repo_url = models.URLField(unique=True)
    name = models.CharField(max_length=255)
    stars = models.IntegerField(default=0)
    language = models.CharField(max_length=100, blank=True, null=True)
    issues = models.IntegerField(default=0)

    summary = models.TextField(blank=True, null=True)
    rating = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name