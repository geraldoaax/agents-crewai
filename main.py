import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
serper_api_key = os.getenv("SERPER_API_KEY")


# You can choose to use a local model through Ollama for example. See https://docs.crewai.com/how-to/LLM-Connections/ for more information.

# os.environ["OPENAI_API_BASE"] = 'http://localhost:11434/v1'
# os.environ["OPENAI_MODEL_NAME"] ='openhermes'  # Adjust based on available model
# os.environ["OPENAI_API_KEY"] ='sk-111111111111111111111111111111111111111111111111'

search_tool = SerperDevTool()

# Define your agents with roles and goals
researcher = Agent(
  role='Analista de Pesquisa Sênior',
  goal='Descubra desenvolvimentos de ponta em IA e ciência de dados',
  backstory="""Você trabalha em um think tank líder em tecnologia.
  Sua experiência reside na identificação de tendências emergentes.
  Você tem talento para dissecar dados complexos e apresentar insights acionáveis.""",
  verbose=True,
  allow_delegation=False,
  tools=[search_tool]
  # You can pass an optional llm attribute specifying what model you wanna use.
  # It can be a local model through Ollama / LM Studio or a remote
  # model like OpenAI, Mistral, Antrophic or others (https://docs.crewai.com/how-to/LLM-Connections/)
  #
  # import os
  # os.environ['OPENAI_MODEL_NAME'] = 'gpt-3.5-turbo'
  #
  # OR
  #
  # from langchain_openai import ChatOpenAI
  # llm=ChatOpenAI(model_name="gpt-3.5", temperature=0.7)
)
writer = Agent(
  role='Estrategista de conteúdo técnico',
  goal='Crie conteúdo atraente sobre os avanços tecnológicos',
  backstory="""Você é um renomado estrategista de conteúdo, conhecido por seus artigos perspicazes e envolventes.
  Você transforma conceitos complexos em narrativas convincentes.""",
  verbose=True,
  allow_delegation=True
)

# Create tasks for your agents
task1 = Task(
  description="""Conduza uma análise abrangente dos últimos avanços em IA em 2024.
  Identifique as principais tendências, tecnologias inovadoras e possíveis impactos no setor.""",
  expected_output="Relatório detalhado com pelo menos 500 palavras",
  agent=researcher
)

task2 = Task(
  description="""Usando os insights fornecidos, desenvolva um blog envolvente
  postagem que destaca os avanços mais significativos da IA.
  Sua postagem deve ser informativa, mas acessível, atendendo a um público que entende de tecnologia.
  Faça com que pareça legal, evite palavras complexas para que não pareça IA.""",
  expected_output="Postagem completa no blog com pelo menos 4 parágrafos",
  agent=writer
)

# Instantiate your crew with a sequential process
crew = Crew(
  agents=[researcher, writer],
  tasks=[task1, task2],
  verbose=2, # You can set it to 1 or 2 to different logging levels
)

# Get your crew to work!
result = crew.kickoff()

print("######################")
print(result)