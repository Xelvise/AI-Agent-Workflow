import os
import requests
from bs4 import BeautifulSoup
from crewai import Agent, Task, Process, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import Ollama
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import load_tools
from langchain.tools import tool
from crewai.tasks.task_output import TaskOutput
from dotenv import load_dotenv

# To Load Local models through Ollama
llm_mistral = Ollama(model="mistral")

# To load gemini
# load_dotenv()
# llm_gemini = ChatGoogleGenerativeAI(model="gemini-pro", verbose=True, temperature=0.1, google_api_key=os.getenv("GOOGLE-API-KEY"))

search_tool = DuckDuckGoSearchRun()

# Define the topic of interest
topic = input('Emter your desired topic: \n')

# Loading Human Tools
human_tools = load_tools(["human"])
    
# Creating custom tools
class ContentTools:
    @tool("Read webpage content")
    def read_content(url: str) -> str:
        """Read content from a webpage."""
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        text_content = soup.get_text()
        return text_content[:5000]

# Define the senior researcher agent
researcher = Agent(
    role='Curious Explorer',
    goal=f'Explore and delve deep to uncover groundbreaking discoveries around {topic}',
    verbose=True,
    backstory="""Driven by curiosity, you're at the forefront of innovation, eager to explore and share ideas that could change the world.""",
    allow_delegation=False,
    llm=llm_mistral,
    tools=[search_tool]
)

# Define the writer agent
writer = Agent(
    role='Enlightened scribe',
    goal=f'Craft a compelling well-explained content around {topic}',
    verbose=True,
    backstory="""With a flair for simplifying complex topics, you craft engaging educative narratives, transforming knowledge into eloquent prose.""",
    allow_delegation=True,
    llm=llm_mistral
)

# Define the Examiner agent
examiner = Agent(
    role='Examiner',
    goal='Formulate 2-3 thought-provoking test questions, as well as providing the corresponding answer to each',
    verbose=True,
    backstory="""In a bid to guage comprehension and understanding of a given text, you conduct assessment tests that ensures that learnes truly grasp the underlying concepts""",
    allow_delegation=True,
    llm=llm_mistral
)

# Define the synchronous research tasks
list_ideas = Task(
    description=f"List of 5 interesting ideas to explore for an article about {topic}.",
    expected_output="Bullet point list of 5 ideas for an article.",
    tools=[search_tool, ContentTools().read_content],  
    agent=researcher
)


# Define the writing task that waits for the outputs of the two research tasks
write_article = Task(
    description=f"Compose an insightful article on the following ideas",
    expected_output=f"A 4 paragraph article about {topic}.",
    tools=[search_tool],  
    agent=writer,
    context=[list_ideas]  # Depends on the completion of the two asynchronous tasks
)

# Define the examiner's task that waits for the output of the writer's task
assessment = Task(
    description="Generate 2-3 test questions to evaluate understanding or comprehension of the given article",
    expected_output="bullet point list of test questions, with the corresponding answers to each",
    tools=[search_tool, ContentTools().read_content],  
    agent=examiner,
    context=[write_article]
)

# Integrating the crew agents via a sequential process
crew = Crew(
    agents=[researcher, writer, examiner],
    tasks=[list_ideas, write_article, assessment],
    process=Process.sequential,
    verbose=2
)

# Kick off the crew's work
result = crew.kickoff()
print('######################')
print(result)