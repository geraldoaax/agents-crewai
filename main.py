from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Endpoint da API Llama local
LLAMA_ENDPOINT = 'http://localhost:11434/api/generate'

@app.route('/execute-tasks', methods=['POST'])
def execute_tasks():
    data = request.json
    tasks_data = data.get('tasks', [])

    if not tasks_data:
        return jsonify({"error": "No tasks provided"}), 400

    results = []
    for task in tasks_data:
        agent_details = task['agent_details']
        # Solicitar explicitamente que a resposta seja em português
        enriched_prompt = (
            "Por favor, responda em português.\n"
            f"Função: {agent_details['role']}\n"
            f"Objetivo: {agent_details['goal']}\n"
            f"Histórico: {agent_details['backstory']}\n"
            f"Descrição da Tarefa: {task['description']}"
        )

        payload = {
            "model": "llama3",
            "prompt": enriched_prompt,
            "stream": False
        }
        response = requests.post(LLAMA_ENDPOINT, json=payload)
        if response.status_code == 200:
            results.append({
                "task": task['description'],
                "result": response.json().get('response')
            })
        else:
            results.append({
                "task": task['description'],
                "result": "Error processing task with Llama 3",
                "debug": response.text
            })

    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
