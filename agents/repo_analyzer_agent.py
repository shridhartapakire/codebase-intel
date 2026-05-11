import json

from crewai import Agent, Task
from crewai.tools import tool

from core.services.github_service import GitHubService
from core.services.analytics_service import AnalyticsService


# TOOL 1
@tool("Fetch GitHub Repository Data")
def fetch_github_data(repo_url: str) -> str:
    """
    Fetch GitHub repository data using the GitHubService.
    """

    gh = GitHubService()
    data = gh.get_all_data(repo_url)

    return json.dumps(data)


# TOOL 2
@tool("Calculate Repository Health Score")
def calculate_health_score(repo_data_json: str) -> str:
    """
    Calculate repository health score using AnalyticsService.
    """

    data = json.loads(repo_data_json)

    analytics = AnalyticsService()

    score = analytics.calculate_health_score(data)
    label = analytics.get_health_label(score)

    result = {
        "health_score": score,
        "health_label": label
    }

    return json.dumps(result)


# AGENT
def create_repo_analyzer_agent():

    return Agent(
        role="GitHub Repository Analyst",

        goal="""
        Analyze GitHub repositories and provide
        structured repository insights.
        """,

        backstory="""
        You are an expert software engineer who
        specializes in evaluating GitHub repositories,
        project quality, contributor activity,
        and engineering health.
        """,

        tools=[
            fetch_github_data,
            calculate_health_score
        ],

        verbose=True,
        allow_delegation=False,
        max_iter=2,
        Smax_execution_time=120,
    )


# TASK
def create_analyzer_task(agent, repo_url):

    return Task(
        description=f"""
        Analyze the GitHub repository:
        {repo_url}

        Fetch repository data,
        calculate health score,
        and provide a short summary.
        """

        expected_output="""
        Repository summary with:
        - repo info
        - stars
        - contributors
        - health score
        - overall quality
        """,

        agent=agent
    )