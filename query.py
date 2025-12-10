#!/usr/bin/env python3
"""
Molecular Biology Educational Model Query System
Easy command-line interface to search and explore your 1,061 protein structures
"""

import json
import sys
import argparse
from collections import defaultdict

def load_educational_data():
    """Load all educational framework data files"""
    try:
        with open('educational_framework/concept_map.json', 'r') as f:
            concept_map = json.load(f)
        
        with open('educational_framework/extracted_concepts.json', 'r') as f:
            concepts_data = json.load(f)
        
        with open('educational_framework/lesson_templates.json', 'r') as f:
            lesson_templates = json.load(f)
        
        return concept_map, concepts_data, lesson_templates
    except FileNotFoundError as e:
        print(f"❌ Error: Could not find educational framework files: {e}")
        print("💡 Make sure you're in the project directory and have run build_educational_model.py")
        sys.exit(1)

def search_by_concept(query, concept_map, concepts_data):
    """Search for structures containing a specific concept"""
    query_lower = query.lower()
    
    # Get concept frequencies from the map
    all_concepts = concept_map.get('most_common_concepts', [])
    matching_concepts = []
    
    for concept_entry in all_concepts:
        if isinstance(concept_entry, list) and len(concept_entry) >= 2:
            concept_name, frequency = concept_entry[0], concept_entry[1]
        else:
            continue
        
        if query_lower in concept_name.lower():
            matching_concepts.append((concept_name, frequency))
    
    if not matching_concepts:
        print(f"❌ No concepts found matching '{query}'")
        return
    
    print(f"\n🔍 Found {len(matching_concepts)} concept(s) matching '{query}':")
    print("-" * 80)
    
    for concept_name, frequency in matching_concepts:
        print(f"\n📊 {concept_name}")
        print(f"   Frequency: {frequency} structures")
        
        # Find examples from the detailed data
        examples = []
        for struct in concepts_data[:10]:  # Check first 10 for examples
            if concept_name in struct.get('concepts', []):
                examples.append(struct['pdb_id'])
                if len(examples) >= 3:
                    break
        
        if examples:
            print(f"   Examples: {', '.join(examples)}")

def search_by_pdb_id(pdb_id, concepts_data):
    """Look up a specific PDB ID"""
    pdb_id = pdb_id.upper()
    
    for struct in concepts_data:
        if struct.get('pdb_id') == pdb_id:
            print(f"\n🧬 PDB ID: {pdb_id}")
            print("-" * 80)
            print(f"Title: {struct.get('title', 'N/A')}")
            print(f"Complexity: {struct.get('complexity_level', 'N/A')}")
            print(f"Student Audience: {', '.join(struct.get('student_audience', []))}")
            print(f"Concepts:")
            for concept in struct.get('concepts', []):
                print(f"  • {concept}")
            print(f"Learning Objectives:")
            for objective in struct.get('key_learning_objectives', []):
                print(f"  • {objective}")
            return
    
    print(f"❌ PDB ID {pdb_id} not found in your dataset of {len(concepts_data)} structures")

def filter_by_method(method, concepts_data):
    """Filter structures by experimental method"""
    method_lower = method.lower()
    matching_structures = []
    
    for struct in concepts_data:
        struct_concepts = struct.get('concepts', [])
        for concept in struct_concepts:
            if method_lower in concept.lower():
                matching_structures.append(struct)
                break
    
    if not matching_structures:
        print(f"❌ No structures found using method '{method}'")
        return
    
    print(f"\n🔬 Found {len(matching_structures)} structures using '{method}':")
    print("-" * 80)
    
    for i, struct in enumerate(matching_structures[:10]):  # Show first 10
        print(f"{i+1}. {struct['pdb_id']}: {struct.get('title', '')[:60]}...")
        print(f"   Complexity: {struct.get('complexity_level')}")
    
    if len(matching_structures) > 10:
        print(f"   ... and {len(matching_structures) - 10} more")

def filter_by_complexity(level, concepts_data):
    """Filter structures by complexity level"""
    level_lower = level.lower()
    matching_structures = [s for s in concepts_data if level_lower in s.get('complexity_level', '').lower()]
    
    if not matching_structures:
        print(f"❌ No structures found with complexity '{level}'")
        return
    
    print(f"\n📚 Found {len(matching_structures)} structures at '{level}' complexity:")
    print("-" * 80)
    
    for i, struct in enumerate(matching_structures[:10]):  # Show first 10
        print(f"{i+1}. {struct['pdb_id']}: {struct.get('title', '')[:60]}...")
        concepts = struct.get('concepts', [])
        print(f"   Key concepts: {', '.join(concepts[:3])}")
    
    if len(matching_structures) > 10:
        print(f"   ... and {len(matching_structures) - 10} more")

def show_statistics(concept_map, concepts_data):
    """Show overall dataset statistics"""
    print("\n📈 DATASET STATISTICS")
    print("=" * 80)
    print(f"Total protein structures: {len(concepts_data)}")
    print(f"Total unique concepts: {concept_map.get('total_concepts', 'Unknown')}")
    
    # Count by complexity
    complexity_counts = defaultdict(int)
    method_counts = defaultdict(int)
    
    for struct in concepts_data:
        complexity = struct.get('complexity_level', 'Unknown')
        complexity_counts[complexity] += 1
        
        # Count experimental methods from concepts
        concepts = struct.get('concepts', [])
        for concept in concepts:
            if 'x-ray' in concept.lower() or 'crystallography' in concept.lower():
                method_counts['X-ray Crystallography'] += 1
                break
            elif 'cryo' in concept.lower() or 'em' in concept.lower():
                method_counts['Cryo-EM'] += 1
                break
    
    print(f"\nComplexity Levels:")
    for level, count in sorted(complexity_counts.items()):
        print(f"  • {level}: {count} structures")
    
    print(f"\nExperimental Methods:")
    for method, count in sorted(method_counts.items()):
        print(f"  • {method}: {count} structures")

def show_help():
    """Show usage examples and help"""
    print("\n🔍 MOLECULAR BIOLOGY QUERY SYSTEM - HELP")
    print("=" * 80)
    print("""
USAGE EXAMPLES:

Search by concept:
  python3 query.py --concept "protein structure"
  python3 query.py --concept "enzyme"
  python3 query.py --concept "cryo-em"

Look up specific PDB ID:
  python3 query.py --pdb 1A02
  python3 query.py --pdb 4HHB

Filter by experimental method:
  python3 query.py --method "x-ray"
  python3 query.py --method "cryo-em"

Filter by complexity:
  python3 query.py --complexity "basic"
  python3 query.py --complexity "advanced"

Show dataset statistics:
  python3 query.py --stats

Show this help:
  python3 query.py --help

QUICK SHORTCUTS:
  python3 query.py enzyme           # Search for enzyme concepts
  python3 query.py 1A02            # Look up PDB ID if 4 chars
    """)

def main():
    parser = argparse.ArgumentParser(
        description='Query the Molecular Biology Educational Model',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('query', nargs='?', help='Quick search term or PDB ID')
    parser.add_argument('--concept', '-c', help='Search by concept name')
    parser.add_argument('--pdb', '-p', help='Look up specific PDB ID')
    parser.add_argument('--method', '-m', help='Filter by experimental method')
    parser.add_argument('--complexity', '-x', help='Filter by complexity level')
    parser.add_argument('--stats', '-s', action='store_true', help='Show dataset statistics')
    
    args = parser.parse_args()
    
    # Show help if no arguments
    if len(sys.argv) == 1:
        show_help()
        return
    
    # Load data
    print("🔄 Loading educational framework data...")
    concept_map, concepts_data, lesson_templates = load_educational_data()
    
    # Handle quick query (positional argument)
    if args.query:
        query = args.query
        # Check if it looks like a PDB ID (4 characters, alphanumeric)
        if len(query) == 4 and query.isalnum():
            search_by_pdb_id(query, concepts_data)
        else:
            search_by_concept(query, concept_map, concepts_data)
        return
    
    # Handle specific flags
    if args.concept:
        search_by_concept(args.concept, concept_map, concepts_data)
    elif args.pdb:
        search_by_pdb_id(args.pdb, concepts_data)
    elif args.method:
        filter_by_method(args.method, concepts_data)
    elif args.complexity:
        filter_by_complexity(args.complexity, concepts_data)
    elif args.stats:
        show_statistics(concept_map, concepts_data)
    else:
        show_help()

if __name__ == '__main__':
    main()