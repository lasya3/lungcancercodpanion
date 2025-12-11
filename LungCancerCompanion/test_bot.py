"""
Test script to check what the chatbot retrieves for different questions
Run this while your Flask server is running, or import the knowledge base directly
"""

import requests
import json

# Option 1: Test via API (if Flask server is running)
def test_via_api(question):
    """Test a question via the API"""
    try:
        response = requests.post('http://localhost:5000/api/debug', 
                               json={'message': question},
                               timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"\n{'='*60}")
            print(f"QUESTION: {question}")
            print(f"{'='*60}")
            print(f"Matched Documents:")
            for doc in data['matched_documents']:
                print(f"  - {doc['source']} (score: {doc['score']})")
            print(f"\nContext Preview:")
            print(data['context_preview'][:300])
            print(f"\nFull Context Length: {data['context_length']} chars")
            return data
        else:
            print(f"Error: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        print("ERROR: Flask server is not running!")
        print("Start it with: python app.py")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Option 2: Test directly with knowledge base
def test_direct(question):
    """Test directly with knowledge base (no Flask needed)"""
    from knowledge_base import KnowledgeBase
    kb = KnowledgeBase()
    
    print(f"\n{'='*60}")
    print(f"QUESTION: {question}")
    print(f"{'='*60}")
    
    context = kb.get_relevant_context(question)
    
    # Check which documents matched
    query_lower = question.lower()
    matched = []
    for doc in kb.documents:
        score = 0
        keywords = [w for w in query_lower.split() if len(w) > 2]
        for keyword in keywords:
            if keyword in doc['content'].lower():
                score += doc['content'].lower().count(keyword)
        if score > 0:
            matched.append((score, doc['source']))
    
    matched.sort(reverse=True)
    print("Matched Documents:")
    for score, source in matched:
        print(f"  - {source} (score: {score})")
    
    print(f"\nContext Length: {len(context)} chars")
    print(f"\nContext Preview (first 500 chars):")
    print(context[:500])
    return context

if __name__ == '__main__':
    print("Testing LumoCare Chatbot Knowledge Base Retrieval")
    print("=" * 60)
    
    # Test questions
    test_questions = [
        "What are the symptoms of lung cancer?",
        "Tell me about treatment options",
        "What is the latest research?",
        "Find support groups",
        "What are emergency symptoms?"
    ]
    
    print("\nChoose testing method:")
    print("1. Test via API (requires Flask server running)")
    print("2. Test directly (no Flask needed)")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == '1':
        print("\nTesting via API...")
        for q in test_questions:
            test_via_api(q)
            input("\nPress Enter to continue to next question...")
    else:
        print("\nTesting directly...")
        for q in test_questions:
            test_direct(q)
            input("\nPress Enter to continue to next question...")
    
    print("\n" + "="*60)
    print("Testing complete!")

