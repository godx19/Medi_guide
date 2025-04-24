from flask import Flask, request, jsonify
import json
import re
from datetime import datetime

app = Flask(__name__)

# Knowledge base for the chatbot
knowledge_base = {
    'symptoms': {
        'keywords': ['symptom', 'sick', 'pain', 'fever', 'headache', 'cough'],
        'response': "I can help you check your symptoms. Please visit our Symptom Checker page for detailed analysis."
    },
    'medicines': {
        'keywords': ['medicine', 'drug', 'medication', 'pill', 'tablet'],
        'response': "You can find detailed information about medicines on our Medicines page. Would you like me to help you search for a specific medicine?"
    },
    'contact': {
        'keywords': ['contact', 'help', 'support', 'email', 'phone'],
        'response': "You can reach us through the contact form on this page, or call us at +91 9823000010 during business hours."
    },
    'general': {
        'keywords': ['hello', 'hi', 'hey', 'thanks', 'thank you'],
        'response': "Hello! I'm MediBot, your health assistant. How can I help you today?"
    }
}

def process_message(message):
    message = message.lower()
    
    # Check for matches in knowledge base
    for category, data in knowledge_base.items():
        for keyword in data['keywords']:
            if keyword in message:
                return data['response']
    
    # If no specific match, provide a general response
    return "I'm here to help! You can ask me about symptoms, medicines, or how to contact us. What would you like to know?"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        response = process_message(message)
        
        # Log the interaction
        log_interaction(message, response)
        
        return jsonify({'response': response})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def log_interaction(message, response):
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = {
            'timestamp': timestamp,
            'message': message,
            'response': response
        }
        
        # Append to log file
        with open('chat_logs.json', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
            
    except Exception as e:
        print(f"Error logging interaction: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True, port=5000) 