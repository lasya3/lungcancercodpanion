# LumoCare: Lung Cancer Companion Chatbot

An intelligent educational chatbot that provides information about lung cancer using Large Language Models (LLMs) and Retrieval Augmented Generation (RAG).

## Features

- 🤖 **AI-Powered Chatbot**: Uses Hugging Face's free Mistral-7B-Instruct model for natural language understanding and generation
- 💰 **Completely Free**: No API costs - uses Hugging Face's free Inference API
- 📚 **RAG System**: Retrieval Augmented Generation with a knowledge base on lung cancer topics
- 🎨 **Modern UI**: Clean, accessible interface with quick topic buttons
- 📖 **Educational Content**: Covers symptoms, treatments, research, support resources, and emergencies
- ⚠️ **Medical Disclaimers**: Includes appropriate warnings about not being a substitute for professional medical advice

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **AI**: Hugging Face Mistral-7B-Instruct (Free Inference API)
- **RAG**: Keyword-based retrieval system with knowledge base documents

## Setup Instructions

### 1. Clone or Download the Project

Navigate to the project directory:
```bash
cd LungCancerCompanion
```

### 2. Install Dependencies

Create a virtual environment (recommended):
```bash
python -m venv venv
```

Activate the virtual environment:
- **Windows**: `venv\Scripts\activate`
- **Mac/Linux**: `source venv/bin/activate`

Install required packages:
```bash
pip install -r requirements.txt
```

### 3. Set Up API (Optional - Works Without It!)

This chatbot uses **Hugging Face's free Inference API** - no API key required! 

However, for higher rate limits and better performance, you can optionally:
1. Create a free account at [Hugging Face](https://huggingface.co/join)
2. Get your token from [Settings > Access Tokens](https://huggingface.co/settings/tokens)
3. Create a `.env` file and add:
   ```
   HUGGINGFACE_API_TOKEN=your_token_here
   # Set to true to skip remote API calls and rely only on the local knowledge base
   USE_LOCAL_RESPONSES_ONLY=false
   ```

**Note**: The chatbot works without any API key - Hugging Face's public API is free to use (with rate limits).
You can also set `USE_LOCAL_RESPONSES_ONLY=true` if you want to run entirely offline using the built-in knowledge base and
smart response generator.

### 4. Run the Application

Start the Flask server:
```bash
python app.py
```

The server will start on `http://localhost:5000`

### 5. Open the Chatbot

Open your web browser and navigate to:
```
http://localhost:5000/static/index.html
```

Or simply open the `static/index.html` file directly in your browser (note: the API won't work without the Flask server running).

## Project Structure

```
LungCancerCompanion/
│
├── app.py                 # Flask backend with API endpoints
├── knowledge_base.py      # RAG system and knowledge base manager
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create from .env.example)
├── .env.example          # Example environment file
├── README.md             # This file
│
├── knowledge_base/       # Knowledge base documents (auto-created)
│   ├── symptoms.txt
│   ├── treatment.txt
│   ├── research.txt
│   ├── support.txt
│   └── emergency.txt
│
└── static/               # Frontend files
    ├── index.html        # Main HTML file
    ├── styles.css        # Styling
    └── script.js         # JavaScript for chat functionality
```

## How It Works

1. **User Input**: User types a question or clicks a topic button
2. **RAG Retrieval**: The system searches the knowledge base for relevant information
3. **Context Enhancement**: Relevant context is retrieved and formatted
4. **LLM Generation**: OpenAI GPT-3.5-turbo generates a response using the context
5. **Response Display**: The response is shown to the user in the chat interface

## Knowledge Base Topics

- **Symptoms & Early Detection**: Common symptoms, risk factors, screening recommendations
- **Treatment Options**: Surgery, chemotherapy, radiation, targeted therapy, immunotherapy
- **Latest Research**: Recent advances in lung cancer research and treatment
- **Support Resources**: Emotional support, practical help, advocacy organizations
- **Emergency Resources**: When to seek immediate medical attention

## Testing and Debugging

### Debug Endpoint

You can test what context is being retrieved for any question using the debug endpoint:

```bash
curl -X POST http://localhost:5000/api/debug -H "Content-Type: application/json" -d "{\"message\": \"What are the symptoms?\"}"
```

Or use the test script:
```bash
python test_bot.py
```

This will show you:
- Which knowledge base documents match your query
- The relevance scores
- The context being used for the response

### Console Debugging

When running the Flask server, check the console output - it will show:
- The query being processed
- Context length
- Which sources are being used

## API Endpoints

- `GET /api/health` - Health check endpoint
- `POST /api/chat` - Send a chat message and receive a response
  - Request body: `{ "message": "user question here" }`
  - Response: `{ "response": "bot response", "status": "success" }`

## Customization

### Adding More Knowledge

Edit or add files in the `knowledge_base/` directory. The system will automatically load all `.txt` files.

### Changing the LLM Model

Edit `app.py` and change the `HUGGINGFACE_API_URL` to use a different free model:
```python
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-xxl"
# Other free models available:
# - "microsoft/DialoGPT-large"
# - "HuggingFaceH4/zephyr-7b-beta"
```

To run completely offline (no external API calls), set `USE_LOCAL_RESPONSES_ONLY=true` in your `.env` file. The app will
then rely solely on the knowledge base and its smart fallback response generator.

### Improving RAG

You can enhance the RAG system in `knowledge_base.py` by:
- Using embeddings (OpenAI embeddings or sentence-transformers)
- Implementing vector similarity search
- Adding semantic search capabilities

## Important Notes

⚠️ **Medical Disclaimer**: This chatbot provides educational information only and is NOT a substitute for professional medical advice. Always consult healthcare providers for personal medical decisions.

✅ **Free to Use**: The chatbot uses Hugging Face's free Inference API. No costs involved! 
   (Optional: Add a free Hugging Face token for higher rate limits)

## Future Enhancements

- Vector database integration (e.g., Pinecone, Weaviate) for better RAG
- User conversation history
- Multi-language support
- Enhanced UI features
- Local LLM option for cost savings

## License

This project is created for educational purposes.

## Support

For issues or questions, please refer to the code comments or consult your AI class instructor.

