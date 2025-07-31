import requests

def generate_commentary(game_data):
    """Generate chess commentary using Ollama API"""
    
    # Ollama API endpoint (default local installation)
    OLLAMA_API = "http://localhost:11434/api/generate"
    
    # Prepare the prompt
    moves_str = ' '.join(str(move) for move in game_data['moves'])
    prompt = f"""Analyze this chess game and provide engaging commentary.
    Game details:
    Moves: {moves_str}
    Analysis: {game_data.get('analysis', [])}
    
    Provide a natural, engaging commentary about the key moments and strategies."""
    
    # Prepare the request
    payload = {
        "model": "llama3.2:1b",  # or your specific model
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_API, json=payload)
        response.raise_for_status()
        return response.json().get('response', 'No commentary generated')
    except requests.exceptions.RequestException as e:
        raise Exception(f"Ollama API error: {str(e)}")