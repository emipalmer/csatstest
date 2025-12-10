#!/usr/bin/env python3
"""
Query the Educational Molecular Biology Model
Explain interesting structures and concepts
"""

import json
from collections import defaultdict

def load_data():
    """Load all framework data"""
    with open('educational_framework/concept_map.json', 'r') as f:
        concept_map = json.load(f)
    
    with open('educational_framework/extracted_concepts.json', 'r') as f:
        concepts_data = json.load(f)
    
    with open('educational_framework/concept_hierarchy.json', 'r') as f:
        concept_hierarchy = json.load(f)
    
    return concept_map, concepts_data, concept_hierarchy

def find_common_structures(concepts_data, min_frequency=5):
    """Find the most commonly appearing molecular structures"""
    structure_types = defaultdict(list)
    
    # Handle both list and dict formats
    items = concepts_data if isinstance(concepts_data, list) else concepts_data.items()
    
    if isinstance(concepts_data, list):
        for data in items:
            pdb_id = data.get('pdb_id', 'unknown')
            if 'experimental_method' in data:
                method = data['experimental_method']
                structure_types[method].append({
                    'pdb_id': pdb_id,
                    'concepts': data.get('concepts', []),
                    'complexity': data.get('complexity_level', 'unknown'),
                    'resolution': data.get('resolution', None)
                })
    else:
        for pdb_id, data in items:
            if 'experimental_method' in data:
                method = data['experimental_method']
                structure_types[method].append({
                    'pdb_id': pdb_id,
                    'concepts': data.get('concepts', []),
                    'complexity': data.get('complexity_level', 'unknown'),
                    'resolution': data.get('resolution', None)
                })
    
    return structure_types

def explain_concept(concept_name, concept_map, concepts_data):
    """Explain a specific concept with examples"""
    if concept_name not in concept_map:
        return None
    
    concept_info = concept_map[concept_name]
    
    explanation = {
        'name': concept_name,
        'frequency': concept_info['frequency'],
        'teaching_examples': concept_info['examples'][:5],  # Top 5 examples
        'description': get_description(concept_name),
        'real_world_applications': get_applications(concept_name)
    }
    
    return explanation

def get_description(concept):
    """Provide educational descriptions for key concepts"""
    descriptions = {
        'protein quaternary structure': 
            'How multiple protein chains work together. Like a team where each player has a role.',
        'structure-function relationship': 
            'The shape of a molecule determines what it can do. Like a key fitting a lock.',
        'enzyme catalysis': 
            'Proteins that speed up chemical reactions in your body. Like biological workers building things.',
        'protein-ligand interaction': 
            'When molecules bind to proteins. Like a lock and key fitting together.',
        'gene expression': 
            'DNA → RNA → Protein. How your genes become working molecules in your cells.',
        'experimental method': 
            'How scientists figure out the 3D shape of proteins (X-ray, Cryo-EM, NMR).',
        'mutation effects': 
            'When one amino acid changes, it can break the protein or change how it works.',
        'protein fold': 
            'The 3D shape a protein takes - like origami at the molecular level.',
        'binding site': 
            'The special pocket where other molecules fit into a protein.',
        'active site': 
            'The part of an enzyme where the chemical reaction happens.'
    }
    
    return descriptions.get(concept.lower(), 
                          f"A key concept in molecular biology: {concept}")

def get_applications(concept):
    """Real-world applications of molecular concepts"""
    applications = {
        'enzyme catalysis': ['Drug design', 'Industrial catalysts', 'Fermentation', 'Food processing'],
        'protein-ligand interaction': ['Drug binding', 'Hormone signaling', 'Immune response', 'Diagnostic tests'],
        'mutation effects': ['Cancer research', 'Genetic diseases', 'Evolution', 'Personalized medicine'],
        'gene expression': ['Gene therapy', 'Synthetic biology', 'Biotechnology', 'Medical treatments'],
        'structure-function relationship': ['Drug design', 'Protein engineering', 'Evolution', 'Disease understanding'],
    }
    
    return applications.get(concept.lower(), [])

def main():
    print("\n" + "="*80)
    print("QUERY THE MOLECULAR BIOLOGY EDUCATIONAL MODEL")
    print("="*80)
    
    # Load data
    concept_map, concepts_data, concept_hierarchy = load_data()
    
    print(f"\n✓ Loaded data from {len(concepts_data)} protein structures")
    print(f"✓ Found {len(concept_map)} key molecular biology concepts")
    
    # Find most common structures
    print("\n" + "-"*80)
    print("MOST COMMON MOLECULAR STRUCTURES IN YOUR DATA:")
    print("-"*80)
    
    structure_types = find_common_structures(concepts_data)
    for method, structures in sorted(structure_types.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"\n📊 {method}")
        print(f"   Count: {len(structures)} protein structures")
        print(f"   Examples: {', '.join([s['pdb_id'] for s in structures[:3]])}")
    
    # Explain top concepts
    print("\n" + "-"*80)
    print("TOP MOLECULAR BIOLOGY CONCEPTS TO TEACH:")
    print("-"*80)
    
    top_concepts = sorted(concept_map.items(), 
                         key=lambda x: x[1]['frequency'], 
                         reverse=True)[:5]
    
    for idx, (concept_name, info) in enumerate(top_concepts, 1):
        print(f"\n{idx}. {concept_name.upper()}")
        print(f"   Appears in: {info['frequency']} structures")
        
        explanation = explain_concept(concept_name, concept_map, concepts_data)
        if explanation:
            print(f"   Definition: {explanation['description']}")
            print(f"   Real-world uses: {', '.join(explanation['real_world_applications'][:3])}")
            print(f"   PDB Examples: {', '.join(explanation['teaching_examples'][:3])}")
    
    # Interactive query
    print("\n" + "-"*80)
    print("INTERACTIVE CONCEPT EXPLORER")
    print("-"*80)
    
    while True:
        user_input = input("\n💭 Ask about a concept (or 'quit' to exit): ").strip().lower()
        
        if user_input == 'quit':
            print("\n✓ Thank you for exploring molecular biology!")
            break
        
        # Find matching concepts
        matches = [c for c in concept_map.keys() if user_input in c.lower()]
        
        if matches:
            for concept in matches[:3]:  # Show top 3 matches
                explanation = explain_concept(concept, concept_map, concepts_data)
                print(f"\n📚 {concept.upper()}")
                print(f"   Definition: {explanation['description']}")
                print(f"   Frequency: Found in {explanation['frequency']} structures")
                print(f"   Applications: {', '.join(explanation['real_world_applications'])}")
                print(f"   Example PDB IDs: {', '.join(explanation['teaching_examples'][:3])}")
        else:
            print(f"❌ No concept found matching '{user_input}'")
            print(f"   Try one of these: {', '.join([c for c in list(concept_map.keys())[:5]])}")

if __name__ == '__main__':
    main()
