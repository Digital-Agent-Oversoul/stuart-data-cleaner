import requests
import json

def test_ollama():
    try:
        # Test connection
        response = requests.get('http://localhost:11434/api/tags', timeout=3)
        print(f'Ollama status: {response.status_code}')
        
        if response.status_code == 200:
            models = response.json()
            print(f'Available models: {json.dumps(models, indent=2)}')
            
            # Check if our model is available
            model_names = [model['name'] for model in models.get('models', [])]
            target_model = "qwen2.5:7b-instruct-q4_K_M"
            
            if target_model in model_names:
                print(f'✅ Target model {target_model} is available')
            else:
                print(f'❌ Target model {target_model} not found')
                print(f'Available models: {model_names}')
        else:
            print(f'❌ Ollama connection failed: {response.status_code}')
            
    except Exception as e:
        print(f'❌ Error connecting to Ollama: {e}')

if __name__ == "__main__":
    test_ollama() 