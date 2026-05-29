import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool

load_dotenv()

gemini_llm = LLM(
    model="gemini/gemini-2.5-flash",
    temperature=0.3,
    api_key=os.environ.get("GOOGLE_API_KEY"),
    max_retries=5,
    timeout=120
)

academic_search_tool = SerperDevTool(
    search_url="https://google.serper.dev/scholar",
    n_results=2
)

scout = Agent(
    role="Literature Scout",
    goal="Discover and summarize top-tier academic papers and recent research trends relevant to the given topic.",
    backstory="You are an expert bibliographer with an unparalleled ability to navigate academic databases and extract core methodologies and contributions from complex papers.",
    tools=[academic_search_tool],
    llm=gemini_llm,
    max_iter=3,  
    max_rpm=10,
    verbose=True
)

critic = Agent(
    role="Methodology Critic",
    goal="Identify structural limitations, flawed assumptions, and critical gaps (Research Gaps) within the gathered literature.",
    backstory="You are a notoriously rigorous peer reviewer for top-tier journals (often called 'Reviewer 2'). You analyze methodologies with deep skepticism to find hidden weaknesses.",
    llm=gemini_llm,
    max_iter=3,  
    max_rpm=10,
    verbose=True
)

validator = Agent(
    role="Hypothesis Validator",
    goal="Logically prove how the user's proposed new idea addresses and overcomes the discovered research gaps.",
    backstory="You are a brilliant research strategist who excels at transforming raw ideas into novel, bulletproof academic hypotheses that possess high academic value.",
    llm=gemini_llm,
    max_iter=3,
    max_rpm=10,
    verbose=True
)

writer = Agent(
    role="Academic Ghostwriter",
    goal="Draft a formal, publication-ready Abstract and Introduction section based on the synthesized research analysis.",
    backstory="You are a master of academic writing. You perfectly understand the tone, style, and vocabulary required for top-tier publication venues such as IEEE, ACM, or Nature.",
    llm=gemini_llm,
    max_iter=3,
    max_rpm=10,
    verbose=True
)

pi = Agent(
    role="Principal Investigator",
    goal="Critically review, refine, and polish the final draft to ensure absolute logical coherence and high academic integrity.",
    backstory="You are a distinguished university professor who has guided hundreds of Ph.D. students. You evaluate research proposals with a strict eye for flawless flow and impact.",
    llm=gemini_llm,
    max_iter=3,  
    max_rpm=10,
    verbose=True
)

task_planning = Task(
    description="Formulate a comprehensive search plan, sub-keywords, and milestones to systematically analyze the research topic: '{research_topic}'.",
    expected_output="A structured search blueprint and taxonomy tree for the literature review. Bullet points only.",
    agent=scout
)

task_scouting = Task(
    description="Use the Academic Search Tool to discover the most influential and recent papers regarding '{research_topic}'. Summarize their core methodologies.",
    expected_output="A bullet-point summary of max 3 papers. Do not write introductory or concluding remarks.",
    agent=scout
)

task_criticism = Task(
    description="Analyze the literature summary provided by the Scout. Deduce the fundamental limitations and research gaps step-by-step. Explain WHY these limitations exist.",
    expected_output="A rigorous critique detailing specific research gaps and methodological bottlenecks. Bullet points only.",
    agent=critic
)

task_validation = Task(
    description="Map the user's new idea: '[{new_idea}]' against the research gaps identified by the Critic. Demonstrate logically how this new idea bridges those gaps and establishes academic novelty.",
    expected_output="A logical validation framework proving the novelty and feasibility of the new idea. Bullet points only.",
    agent=validator
)

task_writing = Task(
    description="Synthesize all previous findings to write a formal, sophisticated academic draft containing an Abstract and an Introduction section for a research proposal.",
    expected_output="A well-formatted, high-quality academic draft (Abstract & Introduction) written in a formal scholarly tone.",
    agent=writer
)

task_pi_review = Task(
    description="Review the drafted Abstract and Introduction with the strict eye of a Principal Investigator. Identify any logical leaps, weak arguments, or stylistic flaws. Correct and polish them yourself to produce the ultimate final research proposal.",
    expected_output="A polished, publication-grade final research proposal in Markdown format.",
    agent=pi,
    output_file="final_research_proposal.md" 
)

scholar_crew = Crew(
    agents=[scout, critic, validator, writer, pi],
    tasks=[task_planning, task_scouting, task_criticism, task_validation, task_writing, task_pi_review],
    process=Process.sequential,
    memory=False,
    verbose=True
)

inputs = {
    'research_topic': 'RAG Hallucination',
    'new_idea': 'Dynamic token budget'
}

if __name__ == "__main__":
    print("## [ScholarStream AI] Initializing Autonomous Research Pipeline... ##")
    scholar_crew.kickoff(inputs=inputs)
    print("\n## [System Success] Execution Completed! ##")
    print("The final academic proposal has been successfully saved to 'final_research_proposal.md'.")