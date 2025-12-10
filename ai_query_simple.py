#!/usr/bin/env python3
"""
AI-Ready Molecular Biology Educational Query System
Mock AI responses built-in, ready to connect to real AI APIs
"""

import json
import sys
import argparse
import os
from collections import defaultdict

class MockAIBackend:
    """Mock AI backend with educational molecular biology responses"""
    
    def __init__(self):
        # Pre-written educational explanations for common concepts
        self.explanations = {
            'protein structure': {
                'definition': "Protein structure is the three-dimensional arrangement of atoms in a protein molecule. Think of it like molecular architecture!",
                'importance': "The shape of a protein determines what it can do - this is the fundamental rule of molecular biology.",
                'examples': "Hemoglobin's shape lets it carry oxygen. Insulin's shape lets it bind to cell receptors.",
                'visualization': "Visit rcsb.org and search for any protein to see its 3D structure. Try rotating and zooming!"
            },
            'enzyme': {
                'definition': "Enzymes are protein catalysts that speed up chemical reactions in living organisms without being consumed.",
                'importance': "Without enzymes, the chemical reactions in your cells would be too slow to sustain life.",
                'examples': "Digestive enzymes break down food. DNA polymerase copies genetic information.",
                'visualization': "Look for the 'active site' - the pocket where the chemical reaction happens."
            },
            'cryo-em': {
                'definition': "Cryo-electron microscopy freezes proteins in ice and uses electron beams to determine their structure.",
                'importance': "Won the 2017 Nobel Prize! Can see proteins that are too flexible to crystallize.",
                'examples': "Used to design COVID-19 vaccines. Can see ribosomes, viruses, and membrane proteins.",
                'visualization': "Compare cryo-EM structures (fuzzy) with X-ray structures (sharp) on RCSB PDB."
            },
            'gene expression': {
                'definition': "Gene expression is how DNA information becomes functional proteins: DNA → RNA → Protein.",
                'importance': "This is how your genes actually DO something in your body - they make proteins that carry out functions.",
                'examples': "Your insulin gene becomes insulin protein. Eye color genes become pigment proteins.",
                'visualization': "Find transcription factor proteins on RCSB PDB - they control which genes get expressed."
            }
        }
    
    def generate_explanation(self, concept, student_level="high school"):
        """Generate educational explanation for a concept"""
        concept_lower = concept.lower()
        
        # Find matching concept
        for key, data in self.explanations.items():
            if key in concept_lower:
                response = f"""
🧬 {key.title()} - Explained for {student_level} students

📖 DEFINITION:
{data['definition']}

🎯 WHY IT MATTERS:
{data['importance']}

🌟 REAL EXAMPLES:
{data['examples']}

👁️ HOW TO EXPLORE:
{data['visualization']}

💡 TEACHING TIP:
This concept appears in your dataset of 1,061 protein structures. Use real PDB examples to make it tangible for students!
"""
                return response
        
        # General molecular biology response
        return f"""
🤖 AI Response for: {concept}

This is a Mock AI response. To get detailed, personalized explanations:

1. 🔑 Add OpenAI API key: export OPENAI_API_KEY="your-key"
2. 🖥️ Install Ollama locally: curl -fsSL https://ollama.ai/install.sh | sh
3. 🔄 Rerun this command

For now, try asking about: protein structure, enzyme, cryo-em, or gene expression.
        """
    
    def natural_language_query(self, question):
        """Process natural language questions"""
        question_lower = question.lower()
        
        responses = {
            'what is': self._what_is_response,
            'how do': self._how_do_response,
            'why': self._why_response,
            'difference': self._difference_response,
            'explain': self._explain_response
        }
        
        for trigger, handler in responses.items():
            if trigger in question_lower:
                return handler(question)
        
        return f"""
🤔 You asked: "{question}"

I can help explain molecular biology concepts from your dataset of 1,061 protein structures!

Try questions like:
• "What is protein folding?"
• "How do enzymes work?"  
• "Why is protein structure important?"
• "Explain the difference between X-ray and Cryo-EM"

Or search for specific concepts: protein structure, enzyme, gene expression, etc.
        """
    
    def _what_is_response(self, question):
        if 'protein' in question.lower():
            return self.generate_explanation('protein structure')
        elif 'enzyme' in question.lower():
            return self.generate_explanation('enzyme')
        elif 'cryo' in question.lower() or 'em' in question.lower():
            return self.generate_explanation('cryo-em')
        elif 'gene' in question.lower():
            return self.generate_explanation('gene expression')
        else:
            return "Ask me about proteins, enzymes, gene expression, or experimental methods!"
    
    def _how_do_response(self, question):
        return """
🔧 HOW MOLECULAR BIOLOGY WORKS:

Proteins work by their SHAPE:
• Shape determines function (like a key fitting a lock)
• Change the shape → change the function
• One wrong amino acid can break everything

Scientists discover shapes using:
• X-ray Crystallography (315 of your structures)
• Cryo-EM (746 of your structures)

Your 1,061 protein structures show this principle in action!
        """
    
    def _why_response(self, question):
        return """
🎯 WHY MOLECULAR BIOLOGY MATTERS:

Structure-Function Relationship:
• Every protein's shape determines what it does
• Understanding shape → Understanding disease
• Shape knowledge → Better medicine

Real Impact:
• Design better drugs
• Understand genetic diseases  
• Create new therapies
• Improve food/medicine production

Your dataset has 1,061 examples of this principle!
        """
    
    def _difference_response(self, question):
        if 'x-ray' in question.lower() and 'cryo' in question.lower():
            return """
🔬 X-RAY vs CRYO-EM COMPARISON:

X-RAY CRYSTALLOGRAPHY (315 structures in your data):
✅ Very high resolution (atomic detail)
✅ Sharp, clear images
❌ Requires protein crystals (hard to grow)
❌ Only works with stable proteins

CRYO-EM (746 structures in your data):
✅ Works with flexible proteins
✅ Can see large complexes
✅ Faster than X-ray
❌ Lower resolution (improving rapidly!)

2017 Nobel Prize went to Cryo-EM developers!
            """
        else:
            return "Ask me to compare X-ray crystallography and Cryo-EM, or other molecular biology topics!"
    
    def _explain_response(self, question):
        # Route to appropriate explanation based on keywords
        return self._what_is_response(question)

class AIReadyQuery:
    """AI-ready query system with educational enhancements"""
    
    def __init__(self):
        self.ai_backend = MockAIBackend()
        self.concept_map = None
        self.concepts_data = None
    
    def load_educational_data(self):
        """Load educational framework data"""
        try:
            with open('educational_framework/concept_map.json', 'r') as f:
                self.concept_map = json.load(f)
            
            with open('educational_framework/extracted_concepts.json', 'r') as f:
                self.concepts_data = json.load(f)
            
            return True
        except FileNotFoundError as e:
            print(f"❌ Error: Could not find educational framework files: {e}")
            return False
    
    def search_and_explain(self, query):
        """Enhanced search with AI explanations"""
        query_lower = query.lower()
        
        # Check if it's a PDB ID
        if len(query) == 4 and query.isalnum():
            return self._explain_pdb_structure(query.upper())
        
        # Search concepts in dataset
        matching_concepts = []
        all_concepts = self.concept_map.get('most_common_concepts', [])
        
        for concept_entry in all_concepts:
            if isinstance(concept_entry, list) and len(concept_entry) >= 2:
                concept_name, frequency = concept_entry[0], concept_entry[1]
                if query_lower in concept_name.lower():
                    matching_concepts.append((concept_name, frequency))
        
        if matching_concepts:
            result = f"\n🔍 Found {len(matching_concepts)} concept(s) matching '{query}':\n"
            result += "=" * 80 + "\n"
            
            for concept_name, frequency in matching_concepts[:2]:  # Top 2 matches
                result += f"\n📊 {concept_name}\n"
                result += f"   Appears in: {frequency} structures\n\n"
                
                # Add AI explanation
                ai_explanation = self.ai_backend.generate_explanation(concept_name)
                result += ai_explanation + "\n"
                result += "=" * 80 + "\n"
            
            return result
        else:
            # Try natural language processing
            return self.ai_backend.natural_language_query(query)
    
    def _explain_pdb_structure(self, pdb_id):
        """Explain specific PDB structure with AI enhancement"""
        for struct in self.concepts_data:
            if struct.get('pdb_id') == pdb_id:
                basic_info = f"""
🧬 PDB ID: {pdb_id}
📖 Title: {struct.get('title', 'N/A')}
📚 Complexity: {struct.get('complexity_level', 'N/A')}
🎯 Student Level: {', '.join(struct.get('student_audience', []))}
🧪 Concepts: {', '.join(struct.get('concepts', []))}

📝 Learning Objectives:
"""
                for obj in struct.get('key_learning_objectives', []):
                    basic_info += f"   • {obj}\n"
                
                # Add AI explanation based on concepts
                main_concept = struct.get('concepts', ['protein structure'])[0]
                ai_explanation = self.ai_backend.generate_explanation(main_concept)
                
                return basic_info + "\n" + "=" * 80 + "\n🤖 AI EXPLANATION:\n" + ai_explanation
        
        return f"❌ PDB ID {pdb_id} not found in your dataset of {len(self.concepts_data)} structures"
    
    def generate_lesson_ideas(self, topic, grade_level="high school"):
        """Generate lesson plan suggestions"""
        lesson_template = f"""
📚 AI LESSON PLAN: {topic.title()} for {grade_level.title()} Students

🎯 LEARNING OBJECTIVES:
• Understand the structure-function relationship in {topic}
• Explore real protein structures using RCSB PDB
• Connect molecular structure to biological function
• Apply knowledge to real-world examples

🚀 OPENING HOOK (5 minutes):
Show a colorful 3D protein structure and ask: "Is this art, architecture, or something alive?"
Answer: "It's a protein made by cells RIGHT NOW!"

🔬 MAIN ACTIVITY (30 minutes):
1. Go to www.rcsb.org
2. Search for proteins related to {topic}
3. Students explore 3D structures
4. Identify key features and ask "What does this shape do?"

🎭 HANDS-ON EXPLORATION:
• Rotate and zoom 3D structures
• Color-code by atom type or amino acid
• Compare normal vs mutated versions
• Find the active site or binding pocket

✅ ASSESSMENT:
• Students explain how structure relates to function
• Predict what happens if structure changes
• Connect to real diseases or applications

📱 TECH INTEGRATION:
Use your dataset of 1,061 structures for examples!
Students can explore structures at different complexity levels.

💡 REAL-WORLD CONNECTIONS:
• Medicine and drug design
• Genetic diseases
• Biotechnology applications
• Evolution and adaptation
        """
        
        return lesson_template

def main():
    parser = argparse.ArgumentParser(
        description='AI-Ready Molecular Biology Educational Query System',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('query', nargs='?', help='Natural language question or search term')
    parser.add_argument('--concept', '-c', help='Explain a concept with AI')
    parser.add_argument('--lesson', '-l', help='Generate lesson plan for topic')
    parser.add_argument('--pdb', '-p', help='Explain specific PDB structure')
    parser.add_argument('--ask', '-a', help='Ask any question about molecular biology')
    parser.add_argument('--level', default='high school', help='Student level')
    
    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        print("""
🤖 AI-READY MOLECULAR BIOLOGY QUERY SYSTEM
==========================================

CURRENT STATUS: Mock AI (Built-in responses)
TO UPGRADE: Add OpenAI key or install Ollama for real AI

EXAMPLES:
  python3 ai_query.py "How do proteins fold?"
  python3 ai_query.py --concept "enzyme" --level college  
  python3 ai_query.py --lesson "protein structure"
  python3 ai_query.py --pdb 1A02
  python3 ai_query.py --ask "What's the difference between X-ray and Cryo-EM?"

FEATURES:
🧠 Natural language queries (mock responses)
📚 Educational concept explanations
📝 Lesson plan generation
🔬 Enhanced PDB structure info
🎓 Student-level appropriate responses

UPGRADE OPTIONS:
1. OpenAI: Set OPENAI_API_KEY environment variable
2. Ollama: curl -fsSL https://ollama.ai/install.sh | sh
        """)
        return
    
    # Initialize system
    print("🚀 Starting AI-Ready Query System...")
    ai_query = AIReadyQuery()
    
    if not ai_query.load_educational_data():
        print("❌ Could not load educational data")
        return
    
    print("✅ Loaded educational framework data")
    print("🤖 Using Mock AI responses (upgrade available)\n")
    
    # Process queries
    if args.query:
        print(ai_query.search_and_explain(args.query))
    elif args.concept:
        print(f"🧠 AI Explanation of '{args.concept}' for {args.level} students:")
        print("=" * 80)
        print(ai_query.ai_backend.generate_explanation(args.concept, args.level))
    elif args.lesson:
        print(f"📝 AI Lesson Plan for '{args.lesson}' ({args.level}):")
        print("=" * 80)
        print(ai_query.generate_lesson_ideas(args.lesson, args.level))
    elif args.pdb:
        print(ai_query._explain_pdb_structure(args.pdb.upper()))
    elif args.ask:
        print(f"💭 AI Answer:")
        print("=" * 80)
        print(ai_query.ai_backend.natural_language_query(args.ask))

if __name__ == '__main__':
    main()