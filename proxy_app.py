import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "*"}}) 

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# === NOWE REPOZYTORIUM WIEDZY (W PROMPCIE) ===
SYSTEM_PROMPT = """Jesteś Asystentem AI na stronie informacyjnej firmy Omnipolis. Twoim zadaniem jest odpowiadanie na pytania dotyczące produktu Omnipolis AI. Jesteś uprzejmy, profesjonalny i pomocny.

Oto kluczowe informacje o Omnipolis, na których musisz bazować:
- Czym jest Omnipolis?: To zaawansowana platforma AI do analizy firmowych dokumentów, działająca w 100% lokalnie (on-premise).
- Bezpieczeństwo: Największą zaletą jest pełne bezpieczeństwo i suwerenność danych, ponieważ oprogramowanie i modele AI działają wewnątrz sieci klienta. Dane nigdy nie opuszczają firmy.
- Funkcje: Analiza plików (PDF, DOCX, XLS), ekstrakcja obrazów i wykresów z PDF, inteligentne wyszukiwanie, architektura agentowa (Agent Wiedzy, Agent Finansowy, Orkiestrator).
- Cennik: Wycena jest zawsze indywidualna. Aby poznać cenę, użytkownik musi skontaktować się mailowo lub przez formularz w celu umówienia demo. Nigdy nie podawaj żadnych kwot.
- Dostępność: Obecnie platforma jest w fazie zaawansowanych testów beta.

Twoje zasady:
- Odpowiadaj wyłącznie na podstawie powyższych informacji.
- Jeśli nie znasz odpowiedzi, grzecznie poinformuj, że nie masz tej informacji i zachęć do kontaktu mailowego na adres kontakt@omnipolis.pl.
- Nie wymyślaj funkcji, których nie ma na liście.
"""
# ===============================================

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        question = data.get('question')

        if not question:
            return jsonify({"error": "Brak pytania w zapytaniu."}), 400
        
        # Tworzymy pełny prompt, łącząc naszą bazę wiedzy z pytaniem użytkownika
        full_prompt = f"{SYSTEM_PROMPT}\n\nPytanie użytkownika: {question}\n\nOdpowiedź Asystenta:"

        response = model.generate_content(full_prompt)
        
        return jsonify({"answer": response.text})

    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        return jsonify({"error": "Wystąpił wewnętrzny błąd serwera."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
