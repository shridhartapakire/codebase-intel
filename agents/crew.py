from crewai import Crew, Process

from agents.repo_analyzer_agent import (
    create_repo_analyzer_agent,
    create_analyzer_task,
)

from agents.insight_generator_agent import (
    create_insight_generator_agent,
    create_insight_task,
)


def run_analysis_crew(repo_url: str):

    # CREATE AGENTS
    analyzer_agent = create_repo_analyzer_agent()

    insight_agent = create_insight_generator_agent()


    # CREATE TASKS
    analyzer_task = create_analyzer_task(
        analyzer_agent,
        repo_url
    )

    insight_task = create_insight_task(
        insight_agent,
        analyzer_task
    )


    # CREATE CREW
    crew = Crew(
        agents=[
            analyzer_agent,
            insight_agent
        ],

        tasks=[
            analyzer_task,
            insight_task
        ],

        process=Process.sequential,

        verbose=True,
    )


    # RUN CREW
    print(f"\n🚀 Starting CrewAI analysis for: {repo_url}\n")

    result = crew.kickoff()


    # RETURN RESULTS
    return {
        "analyzer_output": str(analyzer_task.output),

        "insights_output": str(insight_task.output),

        "final_summary": str(result),

        "status": "completed",
    }