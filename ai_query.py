#!/usr/bin/env python3
"""
AI-Enhanced Molecular Biology Educational Query System
Integrates LLMs for intelligent explanations and natural language queries
"""

import json
import sys
import argparse
import os
from collections import defaultdict
import requests

class AIBackend:
    """Base class for AI backends"""
    
    def generate_explanation(self, prompt, max_tokens=500):
        raise NotImplementedError
    
    def is_available(self):
        raise NotImplementedError

class OpenAIBackend(AIBackend):
    """OpenAI GPT backend"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.base_url = "https://api.openai.com/v1/chat/completions"
    
    def is_available(self):
        return self.api_key is not None
    
    def generate_explanation(self, prompt, max_tokens=500):
        if not self.is_available():
            return "❌ OpenAI API key not found. Set OPENAI_API_KEY environment variable."
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [
                {'role': 'system', 'content': 'You are an expert molecular biology teacher. Explain concepts clearly for students.'},
                {'role': 'user', 'content': prompt}
            ],
            'max_tokens': max_tokens,
            'temperature': 0.7
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"❌ OpenAI API error: {response.status_code}"
        except Exception as e:
            return f"❌ Error calling OpenAI API: {str(e)}"

class OllamaBackend(AIBackend):
    """Local Ollama backend"""
    
    def __init__(self, model_name="llama3.2:1b", base_url="http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
    
    def is_available(self):
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def generate_explanation(self, prompt, max_tokens=500):
        if not self.is_available():
            return "❌ Ollama not available. Install with: curl -fsSL https://ollama.ai/install.sh | sh"
        
        data = {
            'model': self.model_name,
            'prompt': f"You are an expert molecular biology teacher. {prompt}",
            'stream': False
        }
        
        try:
            response = requests.post(f"{self.base_url}/api/generate", json=data, timeout=30)
            if response.status_code == 200:
                result = response.json()
                return result.get('response', 'No response generated')
            else:
                return f"❌ Ollama API error: {response.status_code}"
        except Exception as e:
            return f"❌ Error calling Ollama API: {str(e)}"

class MockAIBackend(AIBackend):
    """Mock AI backend for testing without API calls"""
    
    def is_available(self):
        return True
    
    def generate_explanation(self, prompt, max_tokens=500):
        # Generate a reasonable response based on keywords in the prompt
        responses = {
            'protein structure': "Protein structure refers to the three-dimensional arrangement of atoms in proteins. Think of it like molecular architecture - the shape determines the function!",
            'enzyme': "Enzymes are protein catalysts that speed up chemical reactions in living organisms. They work like molecular machines with specific shapes that fit their substrates.",
            'cryo-em': "Cryo-electron microscopy (Cryo-EM) is a technique that allows scientists to see protein structures by freezing them in ice and using electron beams.",
            'gene expression': "Gene expression is the process by which information from genes is used to synthesize functional gene products, usually proteins.",
            'x-ray crystallography': "X-ray crystallography uses X-ray diffraction patterns from protein crystals to determine atomic-level structures."
        }
        
        prompt_lower = prompt.lower()
        for key, response in responses.items():
            if key in prompt_lower:
                return f"🤖 [Mock AI Response]\n\n{response}\n\nThis is a simplified explanation. For more detail, enable a real AI backend (OpenAI or Ollama)."
        
        return "🤖 [Mock AI Response]\n\nI can explain molecular biology concepts! Try asking about proteins, enzymes, or experimental methods."

class AIEnhancedQuery:
    """Main AI-enhanced query system"""
    
    def __init__(self):
        self.ai_backends = [
            OpenAIBackend(),
            OllamaBackend(),
            MockAIBackend()  # Always available fallback
        ]
        self.active_backend = None
        self._select_backend()
        self.concept_map = None
        self.concepts_data = None
        self.lesson_templates = None
    
    def _select_backend(self):
        """Select the first available AI backend"""
        for backend in self.ai_backends:
            if backend.is_available():
                self.active_backend = backend
                print(f"🤖 Using AI backend: {backend.__class__.__name__}")
                break
    
    def load_educational_data(self):
        """Load all educational framework data files"""
        try:
            with open('educational_framework/concept_map.json', 'r') as f:
                self.concept_map = json.load(f)
            
            with open('educational_framework/extracted_concepts.json', 'r') as f:
                self.concepts_data = json.load(f)
            
            with open('educational_framework/lesson_templates.json', 'r') as f:
                self.lesson_templates = json.load(f)
            
            return True
        except FileNotFoundError as e:
            print(f"❌ Error: Could not find educational framework files: {e}")
            return False
    
    def natural_language_query(self, question):
        """Process natural language questions about molecular biology"""
        # Create context from the data
        context = f"""
        You have access to a molecular biology educational database with:
        - {len(self.concepts_data)} protein structures
        - {self.concept_map.get('total_concepts', 0)} unique concepts
        - Experimental methods: X-ray crystallography, Cryo-EM
        - Complexity levels: Basic to Advanced
        
        Key concepts include: Protein Quaternary Structure, Structure-Function Relationship, 
        Gene Expression, Enzyme Function, Nucleic Acid-Protein Interactions
        
        Question: {question}
        
        Please provide a clear, educational explanation suitable for students learning molecular biology.
        If the question is about a specific protein or structure, explain its biological significance.
        """
        
        return self.active_backend.generate_explanation(context)
    
    def explain_concept_with_ai(self, concept_name, student_level="general"):
        """Generate AI explanation for a concept using real data"""
        # Find relevant structures for this concept
        relevant_structures = []
        all_concepts = self.concept_map.get('most_common_concepts', [])
        
        concept_frequency = 0
        for concept_entry in all_concepts:
            if isinstance(concept_entry, list) and len(concept_entry) >= 2:
                name, freq = concept_entry[0], concept_entry[1]
                if concept_name.lower() in name.lower():
                    concept_frequency = freq
                    break
        
        # Get examples from detailed data
        examples = []
        for struct in self.concepts_data[:5]:  # Check first 5 for examples
            if any(concept_name.lower() in c.lower() for c in struct.get('concepts', [])):
                examples.append({
                    'pdb_id': struct['pdb_id'],
                    'title': struct.get('title', ''),
                    'complexity': struct.get('complexity_level', '')
                })
        
        prompt = f"""
        Explain the molecular biology concept "{concept_name}" for {student_level} level students.
        
        Context from real scientific data:
        - This concept appears in {concept_frequency} protein structures in our database
        - Example structures: {', '.join([ex['pdb_id'] for ex in examples[:3]])}
        - Real protein examples: {'; '.join([ex['title'][:50] + '...' for ex in examples[:2]])}
        
        Please provide:
        1. A clear definition
        2. Why this concept is important in biology
        3. Real-world examples and applications
        4. How students can visualize or understand this concept
        
        Keep the explanation engaging and appropriate for {student_level} students.
        """
        
        return self.active_backend.generate_explanation(prompt)
    
    def generate_lesson_ideas(self, topic, grade_level="high school"):
        """Generate AI-powered lesson plan ideas"""
        prompt = f"""
        Create a lesson plan for teaching "{topic}" to {grade_level} students.
        
        Available resources:
        - 1,061 real protein structures from research databases
        - 3D visualization tools (RCSB PDB website)
        - Educational concepts mapped to real scientific data
        
        Please suggest:
        1. Learning objectives
        2. Engaging opening activity (5-10 minutes)
        3. Main lesson activities using real protein structures
        4. Assessment ideas
        5. Real-world connections
        
        Make it practical and engaging for {grade_level} students.
        """
        
        return self.active_backend.generate_explanation(prompt, max_tokens=800)
    
    def search_and_explain(self, query):
        """Enhanced search that includes AI explanations"""
        # First do the regular search
        query_lower = query.lower()
        
        # Check if it's a PDB ID
        if len(query) == 4 and query.isalnum():
            return self._explain_pdb_structure(query.upper())
        
        # Search concepts
        matching_concepts = []
        all_concepts = self.concept_map.get('most_common_concepts', [])
        
        for concept_entry in all_concepts:
            if isinstance(concept_entry, list) and len(concept_entry) >= 2:
                concept_name, frequency = concept_entry[0], concept_entry[1]
                if query_lower in concept_name.lower():
                    matching_concepts.append((concept_name, frequency))
        
        if matching_concepts:
            result = f"\n🔍 Found {len(matching_concepts)} concept(s) matching '{query}':\n"
            result += "-" * 80 + "\n"
            
            for concept_name, frequency in matching_concepts[:3]:  # Top 3 matches
                result += f"\n📊 {concept_name}\n"
                result += f"   Frequency: {frequency} structures\n\n"
                
                # Add AI explanation
                ai_explanation = self.explain_concept_with_ai(concept_name)
                result += f"🤖 AI Explanation:\n{ai_explanation}\n"
                result += "\n" + "=" * 80 + "\n"
            
            return result
        else:
            # Try natural language query
            return self.natural_language_query(query)
    
    def _explain_pdb_structure(self, pdb_id):
        """Explain a specific PDB structure with AI enhancement"""
        for struct in self.concepts_data:
            if struct.get('pdb_id') == pdb_id:
                basic_info = f"""
🧬 PDB ID: {pdb_id}
Title: {struct.get('title', 'N/A')}
Complexity: {struct.get('complexity_level', 'N/A')}
Concepts: {', '.join(struct.get('concepts', []))}
"""
                
                # Generate AI explanation
                prompt = f"""
                Explain this protein structure for students:
                
                PDB ID: {pdb_id}
                Title: {struct.get('title', '')}
                Biological concepts: {', '.join(struct.get('concepts', []))}
                Complexity level: {struct.get('complexity_level', '')}
                
                Please explain:
                1. What this protein does in living organisms
                2. Why its structure is important
                3. What students can learn from studying it
                4. How they can explore it further
                
                Make it educational and engaging.
                """
                
                ai_explanation = self.active_backend.generate_explanation(prompt)
                
                return basic_info + f"\n🤖 AI Explanation:\n{ai_explanation}"
        
        return f"❌ PDB ID {pdb_id} not found in dataset"

def main():
    parser = argparse.ArgumentParser(
        description='AI-Enhanced Molecular Biology Educational Query System',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('query', nargs='?', help='Natural language question or search term')
    parser.add_argument('--concept', '-c', help='Explain a concept with AI')
    parser.add_argument('--lesson', '-l', help='Generate lesson plan for topic')
    parser.add_argument('--pdb', '-p', help='Explain specific PDB structure')
    parser.add_argument('--ask', '-a', help='Ask any question about molecular biology')
    parser.add_argument('--level', default='high school', help='Student level (elementary, middle school, high school, college)')
    
    args = parser.parse_args()
    
    # Show help if no arguments
    if len(sys.argv) == 1:
        print("""
🤖 AI-ENHANCED MOLECULAR BIOLOGY QUERY SYSTEM
============================================

EXAMPLES:
  python3 ai_query.py "How do proteins fold?"
  python3 ai_query.py --concept "enzyme catalysis" --level college
  python3 ai_query.py --lesson "protein structure" --level "high school"
  python3 ai_query.py --pdb 1A02
  python3 ai_query.py --ask "What is the difference between X-ray and Cryo-EM?"

FEATURES:
  🧠 Natural language queries
  📚 AI-generated concept explanations  
  📝 Custom lesson plan generation
  🔬 Enhanced PDB structure explanations
  🎓 Adaptive responses for different student levels
        """)
        return
    
    # Initialize AI system
    print("🚀 Starting AI-Enhanced Query System...")
    ai_query = AIEnhancedQuery()
    
    if not ai_query.load_educational_data():
        print("❌ Could not load educational data")
        return
    
    # Process queries
    if args.query:
        print(ai_query.search_and_explain(args.query))
    elif args.concept:
        print(f"\n🧠 AI Explanation of '{args.concept}' for {args.level} students:")
        print("=" * 80)
        print(ai_query.explain_concept_with_ai(args.concept, args.level))
    elif args.lesson:
        print(f"\n📝 AI Lesson Plan for '{args.lesson}' ({args.level}):")
        print("=" * 80)
        print(ai_query.generate_lesson_ideas(args.lesson, args.level))
    elif args.pdb:
        print(ai_query._explain_pdb_structure(args.pdb.upper()))
    elif args.ask:
        print(f"\n💭 AI Answer:")
        print("=" * 80)
        print(ai_query.natural_language_query(args.ask))

if __name__ == '__main__':
    main()