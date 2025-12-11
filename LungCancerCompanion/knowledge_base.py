import os

class KnowledgeBase:
    def __init__(self):
        self.documents = []
        self.load_documents()
        
    def load_documents(self):
        """Load all knowledge base documents"""
        kb_dir = 'knowledge_base'
        if not os.path.exists(kb_dir):
            os.makedirs(kb_dir)
        
        # Check if directory is empty or has no .txt files
        txt_files = [f for f in os.listdir(kb_dir) if f.endswith('.txt')] if os.path.exists(kb_dir) else []
        
        if not txt_files:
            # Create initial documents if none exist
            self._create_initial_documents(kb_dir)
            txt_files = [f for f in os.listdir(kb_dir) if f.endswith('.txt')]
        
        # Load all .txt files
        for filename in txt_files:
            filepath = os.path.join(kb_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content.strip():  # Only add non-empty files
                        self.documents.append({
                            'content': content,
                            'source': filename
                        })
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    
    def _create_initial_documents(self, kb_dir):
        """Create initial knowledge base documents"""
        docs = {
            'symptoms.txt': """SYMPTOMS AND EARLY DETECTION OF LUNG CANCER

Common Symptoms:
- Persistent cough that doesn't go away or gets worse
- Coughing up blood or rust-colored sputum
- Chest pain that worsens with deep breathing, coughing, or laughing
- Hoarseness
- Unexplained weight loss and loss of appetite
- Shortness of breath
- Feeling tired or weak
- Infections such as bronchitis and pneumonia that don't go away or keep coming back
- Wheezing

Early Detection:
Early-stage lung cancer often has no symptoms, which is why screening is important for high-risk individuals. 
Low-dose computed tomography (LDCT) scans are recommended for people aged 50-80 who have a 20 pack-year smoking 
history and currently smoke or have quit within the past 15 years.

Risk Factors:
- Smoking (cigarettes, cigars, pipes) - the leading cause
- Secondhand smoke exposure
- Exposure to radon gas
- Exposure to asbestos and other carcinogens
- Family history of lung cancer
- Previous radiation therapy to the chest
- Air pollution

Remember: Early detection significantly improves treatment outcomes. If you experience any persistent symptoms, 
consult a healthcare provider promptly.""",

            'treatment.txt': """TREATMENT OPTIONS FOR LUNG CANCER

Treatment approaches depend on the type of lung cancer, stage, overall health, and personal preferences. 
Treatment is typically managed by a multidisciplinary team including oncologists, pulmonologists, and surgeons.

Main Treatment Types:

1. Surgery:
   - Lobectomy: Removal of an entire lobe of the lung
   - Pneumonectomy: Removal of an entire lung
   - Wedge resection: Removal of a small section of lung
   - Used primarily for early-stage non-small cell lung cancer

2. Chemotherapy:
   - Uses drugs to kill cancer cells or stop them from growing
   - Can be given before surgery (neoadjuvant), after surgery (adjuvant), or as primary treatment
   - Administered in cycles with rest periods

3. Radiation Therapy:
   - Uses high-energy rays to kill cancer cells
   - Can be external beam or internal (brachytherapy)
   - Often used in combination with other treatments

4. Targeted Therapy:
   - Uses drugs that target specific genetic mutations in cancer cells
   - Requires genetic testing of the tumor
   - Examples include EGFR inhibitors, ALK inhibitors, ROS1 inhibitors

5. Immunotherapy:
   - Helps the immune system recognize and attack cancer cells
   - Checkpoint inhibitors (PD-1/PD-L1 inhibitors) are common
   - Can be used alone or with chemotherapy

6. Combination Therapy:
   - Many patients receive multiple treatments in sequence or combination

Side Effects:
All treatments have potential side effects. It's important to discuss these with your healthcare team 
and report any symptoms promptly. Palliative care can help manage symptoms and improve quality of life.

Clinical Trials:
Participation in clinical trials may provide access to new treatments. Discuss options with your healthcare team.

Important: Treatment decisions should be made in consultation with qualified medical professionals who 
can assess your specific situation.""",

            'research.txt': """LATEST RESEARCH UPDATES IN LUNG CANCER

Recent Advances (2023-2024):

1. Precision Medicine and Genetic Testing:
   - Growing use of comprehensive genomic profiling to identify targetable mutations
   - Development of new targeted therapies for specific genetic alterations
   - Liquid biopsies (blood tests) for easier mutation detection and monitoring

2. Immunotherapy Advances:
   - New combination immunotherapy approaches showing promise
   - Research into biomarkers to predict immunotherapy response
   - Development of next-generation checkpoint inhibitors

3. Early Detection:
   - Refinement of low-dose CT screening protocols
   - Research into blood-based biomarkers for early detection
   - AI-assisted imaging analysis for earlier diagnosis

4. Treatment Combinations:
   - Studies showing benefits of combining targeted therapy with immunotherapy
   - Neoadjuvant immunotherapy before surgery showing improved outcomes
   - Better sequencing of treatments for optimal results

5. Small Cell Lung Cancer:
   - New treatments for this aggressive form of lung cancer
   - Immunotherapy combinations showing promise

6. Survivorship and Quality of Life:
   - Improved understanding of long-term side effects
   - Better supportive care approaches
   - Rehabilitation and recovery programs

7. Prevention:
   - Smoking cessation programs and support
   - Research into chemoprevention strategies
   - Public health initiatives for early detection

Staying Updated:
- Follow reputable medical organizations (ACS, NCI, NCCN)
- Consult with your healthcare team about relevant research
- Consider participation in clinical trials when appropriate

Note: Research moves quickly. Always consult with healthcare professionals for the most current 
treatment recommendations based on your specific situation.""",

            'support.txt': """SUPPORT RESOURCES FOR LUNG CANCER PATIENTS AND FAMILIES

Emotional and Psychological Support:

1. Support Groups:
   - In-person and online support groups for patients and caregivers
   - Peer support can provide understanding and shared experiences
   - Many hospitals and cancer centers offer support groups

2. Counseling and Therapy:
   - Individual or family counseling
   - Specialized oncology social workers
   - Grief and bereavement counseling

3. Patient Advocacy Organizations:
   - American Lung Association
   - American Cancer Society
   - Lung Cancer Foundation of America
   - GO2 Foundation for Lung Cancer
   - LUNGevity Foundation

Practical Support:

1. Financial Assistance:
   - Help with medical bills and treatment costs
   - Prescription assistance programs
   - Transportation to appointments
   - Many organizations offer financial aid

2. Practical Help:
   - Meal delivery services
   - Home health care services
   - Childcare assistance
   - Household task help

3. Information Resources:
   - Educational materials and brochures
   - Online resources and databases
   - Hotlines staffed by trained professionals

For Caregivers:
- Respite care services
- Caregiver support groups
- Educational resources
- Self-care importance

Palliative and Hospice Care:
- Palliative care focuses on quality of life and symptom management
- Can be provided alongside curative treatment
- Hospice care for end-of-life support

Legal and Advance Planning:
- Advance directives and living wills
- Power of attorney documents
- Insurance navigation help

Remember: You don't have to face lung cancer alone. Reach out to your healthcare team, 
social workers, and support organizations for help. Asking for support is a sign of strength.""",

            'emergency.txt': """EMERGENCY RESOURCES AND WHEN TO SEEK IMMEDIATE CARE

Medical Emergencies - Call 911 or go to the emergency room immediately if you experience:

1. Severe Breathing Problems:
   - Sudden shortness of breath
   - Difficulty breathing or gasping for air
   - Severe chest pain or pressure
   - Feeling like you're suffocating

2. Severe Bleeding:
   - Coughing up large amounts of blood
   - Vomiting blood
   - Uncontrolled bleeding

3. Neurological Symptoms:
   - Sudden severe headache
   - Confusion or disorientation
   - Weakness or numbness on one side of the body
   - Seizures
   - Vision changes

4. Cardiac Symptoms:
   - Chest pain that doesn't go away
   - Irregular heartbeat
   - Dizziness or fainting

5. Severe Treatment Side Effects:
   - High fever (over 101.5°F or 38.6°C)
   - Severe allergic reactions
   - Uncontrolled nausea or vomiting
   - Severe pain

6. Other Serious Symptoms:
   - Extreme weakness or inability to get out of bed
   - Severe dehydration
   - Signs of infection (fever, chills, rapid heartbeat)

When to Contact Your Healthcare Team (Non-Emergency):

- New or worsening symptoms
- Questions about medications
- Concerns about side effects
- Scheduling issues
- Emotional support needs
- Questions about treatment plan

Important Numbers:
- Emergency: 911
- National Suicide Prevention Lifeline: 988 (US)
- Poison Control: 1-800-222-1222

Always err on the side of caution. If you're unsure whether something is an emergency, 
it's better to seek immediate medical attention. Trust your instincts about your health."""
        }
        
        for filename, content in docs.items():
            filepath = os.path.join(kb_dir, filename)
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Created knowledge base file: {filename}")
            except Exception as e:
                print(f"Error creating {filename}: {e}")
    
    def get_relevant_context(self, query: str, top_k: int = 3) -> str:
        """Get relevant context from knowledge base using improved keyword matching"""
        query_lower = query.lower()
        scored_docs = []
        
        # Define keyword groups for better matching
        topic_keywords = {
            'symptoms.txt': ['symptom', 'sign', 'feel', 'experience', 'cough', 'pain', 'breath', 'weight', 'hoarse', 'wheezing'],
            'treatment.txt': ['treat', 'therapy', 'medicine', 'drug', 'surgery', 'chemotherapy', 'radiation', 'immunotherapy', 'targeted', 'clinical trial'],
            'research.txt': ['research', 'study', 'latest', 'new', 'advance', 'update', 'trial', 'development', 'breakthrough'],
            'support.txt': ['support', 'help', 'resource', 'group', 'counseling', 'assistance', 'organization', 'caregiver'],
            'emergency.txt': ['emergency', 'urgent', '911', 'immediate', 'severe', 'bleeding', 'difficulty breathing', 'chest pain']
        }
        
        for doc in self.documents:
            content_lower = doc['content'].lower()
            score = 0
            filename = doc['source']
            
            # Check for keyword matches (remove common words)
            keywords = [w for w in query_lower.split() if len(w) > 2 and w not in ['the', 'are', 'what', 'how', 'tell', 'me', 'about', 'can', 'you']]
            
            # Boost score if query keywords match topic-specific keywords
            if filename in topic_keywords:
                for keyword in keywords:
                    if keyword in topic_keywords[filename]:
                        score += 10  # Boost for topic-specific matches
                    if keyword in content_lower:
                        score += content_lower.count(keyword)
            else:
                # General matching
                for keyword in keywords:
                    if keyword in content_lower:
                        score += content_lower.count(keyword)
            
            if score > 0:
                scored_docs.append((score, doc))
        
        # Sort by score and get top_k
        scored_docs.sort(reverse=True, key=lambda x: x[0])
        top_docs = scored_docs[:top_k]
        
        # Combine contexts
        contexts = []
        for score, doc in top_docs:
            # Include full content (not truncated) for better responses
            contexts.append(f"Source: {doc['source']}\n{doc['content']}")
        
        if not contexts:
            # If no matches, return general information from all documents
            contexts = [doc['content'] for doc in self.documents[:2]]
        
        return "\n\n---\n\n".join(contexts)

