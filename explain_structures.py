#!/usr/bin/env python3
"""
Explain Interesting Molecular Structures in the Educational Model
Query common structures and molecular concepts
"""

import json

def load_data():
    """Load all framework data"""
    with open('educational_framework/concept_map.json', 'r') as f:
        concept_map = json.load(f)
    
    with open('educational_framework/extracted_concepts.json', 'r') as f:
        concepts_data = json.load(f)
    
    return concept_map, concepts_data

def explain_common_structures():
    """Explain the most interesting and common molecular structures"""
    
    concept_map, concepts_data = load_data()
    
    print("\n" + "="*80)
    print("INTERESTING MOLECULAR STRUCTURES IN YOUR DATASET")
    print("="*80)
    
    # Get the most common concepts
    most_common = concept_map.get('most_common_concepts', [])
    
    print(f"\n✓ Analyzed {len(concepts_data)} protein structures")
    print(f"✓ Found {concept_map.get('total_concepts', 0)} key molecular biology concepts")
    
    print("\n" + "-"*80)
    print("THE 5 MOST COMMON MOLECULAR STRUCTURES & CONCEPTS:")
    print("-"*80)
    
    descriptions = {
        'Protein Quaternary Structure': {
            'description': 'Multiple protein chains working together as a team. Like a business with different departments.',
            'example': 'Hemoglobin (4 chains carry oxygen), Antibodies (2 heavy + 2 light chains)',
            'why_important': 'Many important proteins are multi-subunit complexes - they do more together than alone.',
            'teaching': 'Show students how changing one subunit can affect the whole protein complex.'
        },
        'Structure-Function Relationship': {
            'description': 'The shape determines what a molecule can do. Like a key fitting into a lock.',
            'example': 'Insulin - hormone shape lets it bind to cell receptors. Hemoglobin - shape lets it pick up oxygen.',
            'why_important': 'This is THE fundamental principle of molecular biology.',
            'teaching': 'Ask: "What would happen if we twisted that amino acid chain?"'
        },
        'Cryo-EM': {
            'description': 'Cryo-Electron Microscopy - freezing proteins in ice and shooting electrons to see their shape.',
            'example': 'Won 2017 Nobel Prize. Used to find COVID-19 vaccine structure.',
            'why_important': 'Can see proteins that are too flexible to crystallize (80% of proteins!).',
            'teaching': 'Show the journey: fuzzy EM images → 3D structure. Like CSI with molecules.'
        },
        'Gene Expression': {
            'description': 'How DNA → RNA → Protein. The flow of genetic information.',
            'example': 'Your insulin gene becomes insulin protein. Your hemoglobin genes become hemoglobin.',
            'why_important': 'Connects genetics to real protein molecules in your cells.',
            'teaching': 'Use examples like lactose intolerance, eye color, height - all from gene expression.'
        },
        'Nucleic Acid-Protein Interactions': {
            'description': 'Proteins binding to DNA/RNA to control what happens in cells.',
            'example': 'Transcription factors bind DNA to turn genes on/off. Ribosome binds mRNA to make proteins.',
            'why_important': 'This is how cells control which genes get expressed.',
            'teaching': 'Explain genetic regulation and why identical twins with different diets can look different.'
        },
        'X-ray Crystallography': {
            'description': 'Shining X-rays on protein crystals to figure out 3D structure.',
            'example': '315 of your 1,061 structures used this method. Won multiple Nobel Prizes.',
            'why_important': 'First major method to "see" proteins at atomic resolution.',
            'teaching': 'Show X-ray diffraction patterns and how computers rebuild the 3D structure.'
        },
        'Data Quality & Resolution': {
            'description': 'How clearly we can see the protein atoms. Better resolution = more detail.',
            'example': 'Best structures show atomic positions. Worst structures are fuzzy models.',
            'why_important': 'Resolution affects what teaching questions you can ask (can you see side chains?).',
            'teaching': 'Compare high-resolution vs low-resolution structures. Which is more useful?'
        },
    }
    
    for idx, (concept_name, frequency) in enumerate(most_common[:7], 1):
        if isinstance(concept_name, list):
            concept_name = concept_name[0]
            frequency = concept_name[1] if len(concept_name) > 1 else frequency
        
        print(f"\n{idx}. {concept_name.upper()}")
        print(f"   Appears in: {frequency} structures")
        
        if concept_name in descriptions:
            info = descriptions[concept_name]
            print(f"   What it is: {info['description']}")
            print(f"   Real example: {info['example']}")
            print(f"   Why teach it: {info['why_important']}")
            print(f"   How to teach: {info['teaching']}")
    
    # Find some interesting specific structures
    print("\n" + "-"*80)
    print("SOME INTERESTING SPECIFIC STRUCTURES TO SHOW STUDENTS:")
    print("-"*80)
    
    interesting_pdbs = {
        '1A8O': 'Hemoglobin - carries oxygen in blood',
        '1CLL': 'Insulin - controls blood sugar',
        '1JIW': 'Cryo-EM ribosome structure',
        '4HHB': 'Hemoglobin with bound oxygen',
        '2HHB': 'Hemoglobin in deoxygenated state (compare to 4HHB)',
    }
    
    for pdb_id, description in interesting_pdbs.items():
        # Check if we have this structure
        has_struct = any(s.get('pdb_id') == pdb_id for s in concepts_data)
        status = "✓ In your data" if has_struct else "✗ Not in your data"
        print(f"\n  {pdb_id}: {description} [{status}]")
    
    print("\n" + "-"*80)
    print("HOW TO USE THIS WITH STUDENTS:")
    print("-"*80)
    print("""
1. Start with a "hook" concept like Hemoglobin
   - Normal hemoglobin vs Sickle cell hemoglobin
   - Show: This ONE amino acid change destroys health
   - Ask: "How could we fix this at the molecular level?"

2. Teach Structure-Function Relationship
   - Use your 1,061 structures as examples
   - For each structure ask: "What does this shape do?"
   - Why does the shape matter?

3. Show the Science Methods
   - Cryo-EM won the Nobel Prize recently!
   - X-ray Crystallography won Nobel Prizes in 1915, 1962, 2009
   - How do scientists even see proteins?

4. Connect to Gene Expression
   - DNA sequence → mRNA → Protein structure
   - One wrong codon = one wrong amino acid
   - Can completely break the protein (like sickle cell)

5. Use Real PDB Data
   - Go to www.rcsb.org
   - Search for "insulin" or "hemoglobin" or structure ID
   - Let students rotate, zoom, color-code by atom type
   - This is REAL DATA that scientists discovered!
    """)

if __name__ == '__main__':
    explain_common_structures()
