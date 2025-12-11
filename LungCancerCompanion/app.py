from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv
from knowledge_base import KnowledgeBase

load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)

# Hugging Face API settings (free to use, no API key required for public models)
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
# Alternative free models you can use:
# - "google/flan-t5-xxl" (good for instruction following)
# - "microsoft/DialoGPT-large" (for conversational AI)
# - "HuggingFaceH4/zephyr-7b-beta" (good instruction following)

# Optional: Add your Hugging Face token for higher rate limits (free account available)
HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACE_API_TOKEN', None)
# Set USE_LOCAL_RESPONSES_ONLY=true in .env to avoid external API calls and always use the smart fallback
USE_LOCAL_RESPONSES_ONLY = os.getenv('USE_LOCAL_RESPONSES_ONLY', 'false').lower() == 'true'

# Initialize knowledge base
kb = KnowledgeBase()

def generate_smart_response(user_message, context):
    """Generate a smart response from knowledge base when API is unavailable"""
    user_lower = user_message.lower()
    
    # Extract content from all context sections
    context_sections = context.split('\n\n---\n\n')
    all_content = []
    
    for section in context_sections:
        lines = section.split('\n')
        cleaned_section = []
        skip_next = False
        for i, line in enumerate(lines):
            line = line.strip()
            if line.startswith('Source:'):
                skip_next = True
                continue
            if skip_next and not line:
                skip_next = False
                continue
            if line and not skip_next:
                cleaned_section.append(line)
        if cleaned_section:
            all_content.extend(cleaned_section)
    
    # If no content extracted, try a simpler approach
    if not all_content:
        # Try extracting directly from context
        lines = context.split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith('Source:') and '---' not in line:
                all_content.append(line)
    
    # Combine all content
    content_text = '\n'.join(all_content) if all_content else context
    
    # Clean up extra whitespace
    import re
    content_text = re.sub(r'\n\s*\n\s*\n+', '\n\n', content_text)
    content_text = content_text.strip()
    
    # Create a conversational response
    response_parts = []
    
    # Add relevant information based on query
    if any(word in user_lower for word in ['symptom', 'sign', 'feel', 'experience']):
        intro = "Here's information about lung cancer symptoms:\n\n"
    elif any(word in user_lower for word in ['treat', 'therapy', 'medicine', 'drug']):
        intro = "Here's information about lung cancer treatment options:\n\n"
    elif any(word in user_lower for word in ['research', 'study', 'latest', 'new']):
        intro = "Here's information about the latest lung cancer research:\n\n"
    elif any(word in user_lower for word in ['support', 'help', 'resource', 'group']):
        intro = "Here's information about support resources:\n\n"
    elif any(word in user_lower for word in ['emergency', 'urgent', '911', 'immediate']):
        intro = "Here's important information about emergency situations:\n\n"
    elif any(word in user_lower for word in ['hello', 'hi', 'help', 'what can you']):
        intro = "Hello! I'm LumoCare, your lung cancer companion. I'm here to help educate you about lung cancer.\n\n"
    else:
        intro = "Based on your question, here's relevant information:\n\n"
    
    response_parts.append(intro.rstrip())
    
    # Extract and format the main content (limit to 1500 chars for readability)
    if content_text and len(content_text) > 10:
        # Find a good breaking point (prefer sentence end)
        content_preview = content_text[:1500]
        last_period = content_preview.rfind('.')
        last_newline = content_preview.rfind('\n')
        
        # Prefer breaking at sentence end, but at least at paragraph
        if last_period > 300:
            content_preview = content_preview[:last_period + 1]
        elif last_newline > 300:
            content_preview = content_preview[:last_newline].strip()
        
        response_parts.append(content_preview)
        
        if len(content_text) > 1500:
            response_parts.append("\n\n(For more detailed information, please consult with healthcare professionals.)")
    else:
        # Fallback if still no content
        response_parts.append("I'm here to help answer your questions about lung cancer. Could you please rephrase your question or try asking about symptoms, treatments, research, or support resources?")
    
    # Add disclaimer at the end
    response_parts.append("\n\n⚠️ Important: This is general educational information only. Always consult with qualified healthcare providers for personal medical decisions.")
    
    return '\n'.join(response_parts)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get relevant context from RAG
        context = kb.get_relevant_context(user_message)

        if USE_LOCAL_RESPONSES_ONLY:
            assistant_message = generate_smart_response(user_message, context)
            return jsonify({
                'response': assistant_message,
                'status': 'success'
            })

        # Debug logging (remove in production or make it optional)
        print(f"\n[DEBUG] Query: {user_message}")
        print(f"[DEBUG] Context length: {len(context)} chars")
        print(f"[DEBUG] Context sources: {context.split('Source:')[1:2] if 'Source:' in context else 'None'}")
        
        # Create prompt with context and medical disclaimer
        prompt = f"""<s>[INST] You are LumoCare, an intelligent and compassionate lung cancer companion chatbot. 
Your role is to provide educational information about lung cancer, including symptoms, early detection, treatment options, 
research updates, and support resources.

IMPORTANT DISCLAIMERS:
- This chatbot provides general information only and is NOT a substitute for professional medical advice.
- Always encourage users to consult healthcare providers for personal medical decisions.
- Never provide specific diagnoses or treatment recommendations for individuals.
- If a user describes serious symptoms or an emergency, direct them to seek immediate medical attention.

Use the following context from the knowledge base to provide accurate, up-to-date information:

{context}

Be warm, empathetic, and educational in your responses. Use clear, accessible language.

User question: {user_message}

Provide a helpful response: [/INST]"""
        
        # Call Hugging Face Inference API (free)
        headers = {}
        if HUGGINGFACE_TOKEN:
            headers["Authorization"] = f"Bearer {HUGGINGFACE_TOKEN}"
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 500,
                "temperature": 0.7,
                "return_full_text": False
            }
        }
        
        try:
            response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                # Handle different response formats
                if isinstance(result, list) and len(result) > 0:
                    if 'generated_text' in result[0]:
                        assistant_message = result[0]['generated_text']
                    elif 'text' in result[0]:
                        assistant_message = result[0]['text']
                    else:
                        assistant_message = str(result[0])
                elif isinstance(result, dict):
                    if 'generated_text' in result:
                        assistant_message = result['generated_text']
                    elif 'text' in result:
                        assistant_message = result['text']
                    else:
                        assistant_message = str(result)
                else:
                    assistant_message = str(result)
                
                # Clean up the response (remove any remaining prompt artifacts)
                assistant_message = assistant_message.strip()
                if assistant_message.startswith('[/INST]'):
                    assistant_message = assistant_message.replace('[/INST]', '').strip()
                if not assistant_message or len(assistant_message) < 20:
                    # Response too short, use fallback
                    raise ValueError("Response too short")
            else:
                # API error, use fallback
                raise requests.exceptions.RequestException(f"API returned status {response.status_code}")
        except (requests.exceptions.RequestException, ValueError, KeyError) as e:
            # Use smart fallback when API fails
            print(f"Using fallback response due to: {e}")
            assistant_message = generate_smart_response(user_message, context)
        
        return jsonify({
            'response': assistant_message,
            'status': 'success'
        })
        
    except requests.exceptions.RequestException:
        # Network/API errors - use smart fallback
        context = kb.get_relevant_context(user_message)
        assistant_message = generate_smart_response(user_message, context)
        return jsonify({
            'response': assistant_message,
            'status': 'success'
        })
    except Exception as e:
        # Other errors - still try to provide helpful response
        try:
            context = kb.get_relevant_context(user_message)
            assistant_message = generate_smart_response(user_message, context)
            return jsonify({
                'response': assistant_message,
                'status': 'success'
            })
        except:
            return jsonify({'error': 'An error occurred. Please try again.'}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

@app.route('/api/debug', methods=['POST'])
def debug():
    """Debug endpoint to see what context is being retrieved for a query"""
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get relevant context
        context = kb.get_relevant_context(user_message)
        
        # Get matching documents with scores
        query_lower = user_message.lower()
        matched_docs = []
        for doc in kb.documents:
            content_lower = doc['content'].lower()
            score = 0
            keywords = query_lower.split()
            for keyword in keywords:
                if keyword in content_lower:
                    score += content_lower.count(keyword)
            if score > 0:
                matched_docs.append({
                    'source': doc['source'],
                    'score': score,
                    'preview': doc['content'][:200] + '...'
                })
        
        matched_docs.sort(key=lambda x: x['score'], reverse=True)
        
        return jsonify({
            'query': user_message,
            'context_length': len(context),
            'matched_documents': matched_docs,
            'context_preview': context[:500] + '...' if len(context) > 500 else context,
            'full_context': context
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

