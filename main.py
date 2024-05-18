from flask import Flask, request, jsonify
import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
serper_api_key = os.getenv("SERPER_API_KEY")


# You can choose to use a local model through Ollama for example. See https://docs.crewai.com/how-to/LLM-Connections/ for more information.

# os.environ["OPENAI_API_BASE"] = 'http://localhost:11434/v1'
# os.environ["OPENAI_MODEL_NAME"] ='openhermes'  # Adjust based on available model
# os.environ["OPENAI_API_KEY"] ='sk-111111111111111111111111111111111111111111111111'

search_tool = SerperDevTool()

# Define your agents with roles and goals
# researcher = Agent(
#   role='Analista de Pesquisa Sênior',
#   goal='Descubra desenvolvimentos de ponta em IA e ciência de dados',
#   backstory="""Você trabalha em um think tank líder em tecnologia.
#   Sua experiência reside na identificação de tendências emergentes.
#   Você tem talento para dissecar dados complexos e apresentar insights acionáveis.""",
#   verbose=True,
#   allow_delegation=False,
#   tools=[search_tool]
#   # You can pass an optional llm attribute specifying what model you wanna use.
#   # It can be a local model through Ollama / LM Studio or a remote
#   # model like OpenAI, Mistral, Antrophic or others (https://docs.crewai.com/how-to/LLM-Connections/)
#   #
#   # import os
#   # os.environ['OPENAI_MODEL_NAME'] = 'gpt-3.5-turbo'
#   #
#   # OR
#   #
#   # from langchain_openai import ChatOpenAI
#   # llm=ChatOpenAI(model_name="gpt-3.5", temperature=0.7)
# )
# writer = Agent(
#   role='Estrategista de conteúdo técnico',
#   goal='Crie conteúdo atraente sobre os avanços tecnológicos',
#   backstory="""Você é um renomado estrategista de conteúdo, conhecido por seus artigos perspicazes e envolventes.
#   Você transforma conceitos complexos em narrativas convincentes.""",
#   verbose=True,
#   allow_delegation=True
# )

# Definição dos Agentes Executivos
executive_agents = {
    'content_strategy_exec': Agent(
        role='Executivo de Estratégia de Conteúdo',
        goal='Coordenar a criação de estratégias de conteúdo',
        backstory="Líder estratégico com experiência em grandes campanhas. Enfatiza inovação e autenticidade.",
        verbose=True
    ),
    'data_analysis_exec': Agent(
        role='Executivo de Análise de Dados',
        goal='Analisar dados de marketing para identificar tendências',
        backstory="Analista sênior focado em métricas e conversões. Utiliza dados para impulsionar decisões.",
        verbose=True
    ),
    'customer_engagement_exec': Agent(
        role='Executivo de Engajamento do Cliente',
        goal='Maximizar o engajamento através de canais digitais',
        backstory="Especialista em engajamento e retenção de clientes com foco em mídias sociais e e-mail marketing.",
        verbose=True
    )
}

# Definição dos Sub-Agentes
sub_agents = {
    'content_creator': Agent(
        role='Criador de Conteúdo',
        goal='Produzir conteúdo criativo e envolvente',
        backstory="Jovem criativo apaixonado por contar histórias e criar conteúdo visualmente atraente.",
        verbose=True
    ),
    'seo_analyst': Agent(
        role='Analista de SEO',
        goal='Otimizar conteúdo para motores de busca',
        backstory="Especialista em SEO com profundo conhecimento de algoritmos de busca e otimização on-page.",
        verbose=True
    ),
    'ppc_specialist': Agent(
        role='Especialista em Publicidade PPC',
        goal='Gerenciar campanhas PPC para maximizar o ROI',
        backstory="Publicitário com experiência em plataformas de anúncios pagos e análise de performance de campanhas.",
        verbose=True
    )
}

# Combina todos os agentes em um dicionário para fácil acesso
all_agents = {**executive_agents, **sub_agents}

@app.route('/execute-tasks', methods=['POST'])
def execute_tasks():
    data = request.json
    tasks_data = data.get('tasks', [])

    if not tasks_data:
        print("Nenhuma tarefa foi fornecida")
        return jsonify({"error": "No tasks provided"}), 400

    tasks = []
    for task_info in tasks_data:
        agent_key = task_info.get('agent')
        agent = all_agents.get(agent_key)
        if not agent:
            print(f"Agente não encontrado: {agent_key}")
            return jsonify({"error": f"Agent key '{agent_key}' not found."}), 404

        description = task_info.get('description', 'No description provided.')
        expected_output = task_info.get('expected_output', 'No output specified.')
        task = Task(description=description, expected_output=expected_output, agent=agent)
        tasks.append(task)
        print(f"Tarefa adicionada para o agente {agent_key}: {description}")

    crew = Crew(agents=list(all_agents.values()), tasks=tasks, verbose=2)

    print("Iniciando a execução das tarefas...")
    result = crew.kickoff()

    print("Tarefas executadas, retornando resultados...")
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)