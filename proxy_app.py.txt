import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- Konfiguracja ---
# Wczytujemy klucz API ze zmiennej środowiskowej dla bezpieczeństwa
# LUB wklej go bezpośrednio tutaj do testów.
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyDHpYtLISiIZM0SpPIAjbZmVu9xOgVF8h8")

app = Flask(__name__)
# Włączamy CORS, aby Twoja strona www mogła "rozmawiać" z tym serwerem
CORS(app, resources={r"/chat": {"origins": "*"}}) 

# Konfigurujemy klienta Google AI
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

@app.route('/chat', methods=['POST'])
def chat():
    """
    Główny endpoint, który przyjmuje pytanie i zwraca odpowiedź od AI.
    """
    try:
        # Odczytujemy pytanie z zapytania
        data = request.json
        question = data.get('question')

        if not question:
            return jsonify({"error": "Brak pytania w zapytaniu."}), 400

        # Wysyłamy pytanie do Google AI
        response = model.generate_content(question)
        
        # Zwracamy samą treść odpowiedzi do Twojej strony www
        return jsonify({"answer": response.text})

    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        return jsonify({"error": "Wystąpił wewnętrzny błąd serwera."}), 500

if __name__ == '__main__':
    # Uruchamiamy serwer na porcie 5000 (można zmienić)
    app.run(host='0.0.0.0', port=5000)