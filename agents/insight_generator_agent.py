import os
from crewai import LLM
import json

from crewai import Agent, Task
from crewai.tools import tool

llm = LLM(
    model="openai/gpt-oss-20b:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    max_tokens=1000,
    temperature=0.3
)

# TOOL
@tool("Analyze Repository Patterns")
def analyze_patterns(repo_summary: str) -> str:
    """
    Analyze repository summary and detect patterns,
    risks, warnings, and positive signals.
    """

    patterns = {
        "input_received": True,
        "summary_length": len(repo_summary),

        "instruction": (
            "Analyze repository for:\n"
            "- contributor imbalance\n"
            "- stale development\n"
            "- high issue backlog\n"
            "- maintenance risks\n"
            "- positive community signals\n"
        )
    }

    return json.dumps(patterns)


# AGENT
def create_insight_generator_agent():

    return Agent(
        role="Software Project Intelligence Analyst",

        goal="""
        Analyze repository metrics and generate
        actionable engineering insights.
        """,

        backstory="""
        You are an experienced engineering manager
        who specializes in identifying repository risks,
        unhealthy engineering patterns,
        and project sustainability concerns.
        """,

        tools=[analyze_patterns],

        llm=llm,

        verbose=True,
        allow_delegation=False,
        max_iter=2,
    )


# TASK
def create_insight_task(agent, analyzer_task):

    return Task(
        description="""
        Analyze the repository report generated earlier.

        Identify:
        - risks
        - warnings
        - positive signals
        - engineering concerns
        - actionable recommendations

        Use actual repository numbers when possible.
        """,

        expected_output="""
        Structured repository insight report with:
        - RED FLAGS
        - WARNINGS
        - POSITIVE SIGNALS
        - RECOMMENDATIONS
        """,

        agent=agent,

        context=[analyzer_task]
    )