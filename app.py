from flask import Flask, request, jsonify
from langchain.llms import OpenLLM
from langflow import load_flow_from_json
import requests

app = Flask(__name__)

# Initialize OpenLLM
llm_openllm = OpenLLM(model_name="llama", model_id='meta-llama/Llama-2-7b-hf')

# Load LangFlow chain
langflow_chain = load_flow_from_json("path_to_langflow.json")

@app.route('/')
def home():
    return jsonify({"message": "Welcome to our API!"}), 200

@app.route('/openllm', methods=['POST'])
def openllm():
    try:
        data = request.get_json()
        result = llm_openllm(data["query"])
        return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/langflow', methods=['POST'])
def langflow():
    try:
        data = request.get_json()
        result = langflow_chain(data["text"])
        return jsonify({"result": result}), 200 
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/flowise', methods=['POST'])
def flowise():
    try:
        data = request.get_json()
        response = requests.post('http://0.0.0.0:3010/flowise_endpoint', json=data)

        # Check if request to the Flowise service was successful
        if response.status_code == 200:
            result = response.json()
            return jsonify(result), 200
        else:
            return jsonify({"error": "Flowise service unavailable"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
