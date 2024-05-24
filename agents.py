from crewai import Agent

def get_agents():
    # Agentes executivos especializados nas tarefas de criação de conteúdo para redes sociais
    content_agents = {
        'calendar_agent': Agent(
            role='Especialista em Calendário de Conteúdo',
            goal='Criar um calendário detalhado de postagens para o LinkedIn',
            backstory="Experiente em planejamento de mídia e estratégias de conteúdo, com foco em maximizar engajamento.",
            max_iter=15,
            memory=True,
            verbose=True,
            cache=True,
            allow_delegation=True,
        ),
        'text_content_agent': Agent(
            role='Criador de Textos',
            goal='Escrever textos engajadores para os conteúdos planejados',
            backstory="Escritor criativo com habilidades em captar a essência da mensagem e adaptá-la para o público-alvo.",
            max_iter=15,
            memory=True,
            verbose=True,
            cache=True,
            allow_delegation=True,
        ),
        'image_creator_agent': Agent(
            role='Designer Gráfico',
            goal='Criar imagens e visuais para acompanhar os textos dos posts',
            backstory="Designer gráfico com forte senso estético, especializado em criar visuais impactantes para redes sociais.",
            max_iter=15,
            memory=True,            
            verbose=True,
            cache=True,
            allow_delegation=True,
        ),
        'video_scriptwriter_agent': Agent(
            role='Roteirista de Vídeos',
            goal='Elaborar roteiros para vídeos que serão publicados no YouTube',
            backstory="Roteirista experiente, especializado em conteúdo educativo e promocional para plataformas de vídeo.",
            max_iter=15,
            verbose=True,
            memory=True,
            cache=True,
            allow_delegation=True,
        )
    }

    return content_agents
