"""
MOLECULAR BIOLOGY CONCEPT MAPPER & LESSON PLANNER
================================================
A tool for teachers to create concept maps and lesson plans based on real PDB data

This system helps teachers:
1. Understand molecular structures from PDB
2. Map scientific concepts in biology
3. Create scaffolded lesson plans following scientific practices
4. Connect multiple concepts through concept hierarchies
"""

import json
import os
from pathlib import Path
from collections import defaultdict

# Configuration
JSON_DIR = "./pdb_data"
OUTPUT_DIR = "./educational_framework"
os.makedirs(OUTPUT_DIR, exist_ok=True)

class MolecularBiologyConceptMapper:
    """Maps PDB structures to educational biology concepts"""
    
    def __init__(self):
        self.concepts = defaultdict(list)
        self.hierarchies = defaultdict(list)
        self.lesson_templates = {}
        
    def extract_biology_concepts(self, pdb_data, pdb_id):
        """Extract educational concepts from a PDB structure"""
        concepts = {
            'pdb_id': pdb_id,
            'concepts': [],
            'complexity_level': '',
            'student_audience': [],
            'key_learning_objectives': []
        }
        
        try:
            # CONCEPT 1: Protein Structure Levels
            title = pdb_data.get('struct', {}).get('title', '')
            concepts['title'] = title
            
            # Determine structure type from title
            if 'enzyme' in title.lower():
                concepts['concepts'].append('Enzyme Function')
                concepts['key_learning_objectives'].append('Understand how enzymes catalyze reactions')
            
            if 'antibody' in title.lower() or 'immune' in title.lower():
                concepts['concepts'].append('Immune Response')
                concepts['concepts'].append('Protein-Ligand Binding')
                concepts['key_learning_objectives'].append('Explain antigen-antibody recognition')
            
            if 'receptor' in title.lower():
                concepts['concepts'].append('Cell Signaling')
                concepts['concepts'].append('Protein Structure-Function')
                concepts['key_learning_objectives'].append('Describe receptor-ligand interactions')
            
            # CONCEPT 2: Structural Complexity
            entry_info = pdb_data.get('rcsb_entry_info', {})
            poly_count = int(entry_info.get('polymer_entity_count', 0)) or 0
            
            concepts['concepts'].append('Protein Quaternary Structure')
            if poly_count > 1:
                concepts['complexity_level'] = 'Advanced'
                concepts['student_audience'].extend(['Upper High School', 'College'])
                concepts['key_learning_objectives'].append('Analyze multi-subunit protein interactions')
            else:
                concepts['complexity_level'] = 'Intermediate'
                concepts['student_audience'].extend(['High School', 'College'])
            
            # CONCEPT 3: Experimental Methods
            exptl_method = pdb_data.get('exptl', [{}])[0].get('method', '')
            if 'X-RAY' in exptl_method:
                concepts['concepts'].append('X-ray Crystallography')
                concepts['key_learning_objectives'].append('Understand how X-ray data reveals protein structure')
                concepts['student_audience'].append('College/Advanced')
            elif 'ELECTRON' in exptl_method:
                concepts['concepts'].append('Cryo-EM')
                concepts['key_learning_objectives'].append('Understand electron microscopy and image processing')
                concepts['student_audience'].append('College/Advanced')
            elif 'NMR' in exptl_method:
                concepts['concepts'].append('NMR Spectroscopy')
                concepts['student_audience'].append('College/Advanced')
            
            # CONCEPT 4: Resolution & Data Quality
            reflns = pdb_data.get('reflns', [{}])[0]
            resolution = float(reflns.get('d_resolution_high', 0)) if reflns.get('d_resolution_high') else 0
            
            if resolution > 0:
                concepts['concepts'].append('Data Quality & Resolution')
                if resolution < 2.0:
                    concepts['concepts'].append('High-Resolution Structures')
                    concepts['student_audience'].append('Research Level')
                concepts['key_learning_objectives'].append(
                    f'Interpret structural data at {resolution:.2f}Å resolution'
                )
            
            # CONCEPT 5: Molecular Interactions
            if 'ligand' in title.lower():
                concepts['concepts'].append('Ligand Binding')
                concepts['concepts'].append('Drug Design')
                concepts['key_learning_objectives'].append('Understand molecular recognition')
            
            if 'dna' in title.lower() or 'rna' in title.lower():
                concepts['concepts'].append('Nucleic Acid-Protein Interactions')
                concepts['concepts'].append('Gene Expression')
                concepts['key_learning_objectives'].append('Connect DNA sequence to protein structure')
            
            # CONCEPT 6: Cellular Location & Function
            concepts['concepts'].append('Structure-Function Relationship')
            
            # Remove duplicates and sort
            concepts['concepts'] = sorted(list(set(concepts['concepts'])))
            concepts['student_audience'] = sorted(list(set(concepts['student_audience'])))
            
        except Exception as e:
            print(f"Error processing {pdb_id}: {e}")
        
        return concepts
    
    def build_concept_hierarchy(self):
        """Build a hierarchy of molecular biology concepts from basic to advanced"""
        return {
            "Level 1: Basic Structure": [
                "Atoms and Bonds",
                "Amino Acids",
                "Protein Backbone",
                "Secondary Structure (α-helix, β-sheet)"
            ],
            "Level 2: Protein Architecture": [
                "Protein Structure Levels",
                "Tertiary Structure",
                "Protein Folding",
                "Active Sites",
                "Domains"
            ],
            "Level 3: Complex Systems": [
                "Quaternary Structure",
                "Multi-subunit Proteins",
                "Protein-Protein Interactions",
                "Enzyme Catalysis"
            ],
            "Level 4: Biological Function": [
                "Protein Function",
                "Cell Signaling",
                "Enzyme Kinetics",
                "Metabolic Pathways"
            ],
            "Level 5: Experimental Science": [
                "X-ray Crystallography",
                "Cryo-EM",
                "NMR Spectroscopy",
                "Structural Data Interpretation"
            ],
            "Level 6: Applications": [
                "Drug Design",
                "Disease & Protein Mutations",
                "Protein Engineering",
                "Biotechnology"
            ]
        }
    
    def create_lesson_template(self, concept, level, pdb_id=None):
        """Create a lesson plan template for a specific concept"""
        return {
            "concept": concept,
            "difficulty_level": level,
            "pdb_example": pdb_id,
            "learning_objectives": [
                "Students will understand the core principle",
                "Students will visualize the concept with molecular structures",
                "Students will apply the concept to real biological problems"
            ],
            "scientific_practices": [
                "Asking Questions",
                "Developing Models",
                "Planning Investigations",
                "Analyzing Data",
                "Constructing Explanations",
                "Engaging in Argument from Evidence",
                "Obtaining, Evaluating & Communicating Information"
            ],
            "teaching_sequence": [
                {
                    "phase": "Engagement",
                    "activities": [
                        "Show real PDB structure (3D visualization)",
                        "Ask guiding questions about molecular properties"
                    ],
                    "duration": "5-10 minutes"
                },
                {
                    "phase": "Exploration",
                    "activities": [
                        "Students interact with PDB structure online",
                        "Students collect data about structure features",
                        "Students form hypotheses"
                    ],
                    "duration": "15-20 minutes"
                },
                {
                    "phase": "Explanation",
                    "activities": [
                        "Connect observations to scientific principles",
                        "Explain concept through guided discovery",
                        "Use multiple representations (2D, 3D, sequence)"
                    ],
                    "duration": "15 minutes"
                },
                {
                    "phase": "Elaboration",
                    "activities": [
                        "Apply concept to similar structures",
                        "Solve problems using PDB data",
                        "Make connections to other concepts"
                    ],
                    "duration": "15-20 minutes"
                },
                {
                    "phase": "Evaluation",
                    "activities": [
                        "Concept mapping exercise",
                        "Written explanation of concept",
                        "Peer discussion and critique"
                    ],
                    "duration": "10-15 minutes"
                }
            ],
            "resources": [
                "RCSB PDB (www.rcsb.org)",
                "Mol* Viewer (online 3D visualization)",
                "NCBI Structure Database",
                "NextStrain for viral protein evolution"
            ],
            "assessment": {
                "formative": "Observation checklists, concept sketches, peer feedback",
                "summative": "Concept map, explanation essay, problem-solving tasks"
            },
            "connections": {
                "previous_concepts": "List concepts that should be taught first",
                "subsequent_concepts": "List concepts that build on this one",
                "real_world_applications": "Disease research, drug development, biotechnology"
            }
        }
    
    def process_pdb_files(self):
        """Process all PDB files and extract concepts"""
        files = list(Path(JSON_DIR).glob("*.json"))
        all_concepts = []
        
        print(f"Processing {len(files)} PDB structures for educational concepts...\n")
        
        for i, json_file in enumerate(files):
            if i % 200 == 0:
                print(f"  [{i}/{len(files)}] Processing structures...")
            
            try:
                with open(json_file, 'r') as f:
                    pdb_data = json.load(f)
                    concepts = self.extract_biology_concepts(pdb_data, json_file.stem)
                    if concepts['concepts']:
                        all_concepts.append(concepts)
            except Exception as e:
                pass
        
        return all_concepts
    
    def generate_concept_map(self, all_concepts):
        """Generate a concept map from extracted concepts"""
        concept_frequency = defaultdict(int)
        concept_to_pdb = defaultdict(list)
        
        for data in all_concepts:
            pdb_id = data['pdb_id']
            for concept in data['concepts']:
                concept_frequency[concept] += 1
                concept_to_pdb[concept].append(pdb_id)
        
        # Sort by frequency
        sorted_concepts = sorted(concept_frequency.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "total_concepts": len(concept_frequency),
            "most_common_concepts": sorted_concepts[:20],
            "concept_to_examples": dict(concept_to_pdb),
            "complexity_distribution": self._analyze_complexity(all_concepts),
            "audience_distribution": self._analyze_audience(all_concepts)
        }
    
    def _analyze_complexity(self, all_concepts):
        """Analyze complexity distribution"""
        distribution = defaultdict(int)
        for data in all_concepts:
            level = data.get('complexity_level', 'Not specified')
            distribution[level] += 1
        return dict(distribution)
    
    def _analyze_audience(self, all_concepts):
        """Analyze target audience distribution"""
        distribution = defaultdict(int)
        for data in all_concepts:
            for audience in data.get('student_audience', []):
                distribution[audience] += 1
        return dict(distribution)


def main():
    print("=" * 70)
    print("MOLECULAR BIOLOGY CONCEPT MAPPER")
    print("Educational Framework for Teaching Protein Science")
    print("=" * 70)
    
    mapper = MolecularBiologyConceptMapper()
    
    # Step 1: Build concept hierarchy
    print("\n[1/5] Building concept hierarchy...")
    hierarchy = mapper.build_concept_hierarchy()
    with open(f"{OUTPUT_DIR}/concept_hierarchy.json", 'w') as f:
        json.dump(hierarchy, f, indent=2)
    print("   ✓ Concept hierarchy created")
    
    # Step 2: Process PDB structures
    print("\n[2/5] Extracting educational concepts from PDB structures...")
    all_concepts = mapper.process_pdb_files()
    print(f"   ✓ Extracted concepts from {len(all_concepts)} structures")
    
    # Step 3: Generate concept map
    print("\n[3/5] Generating concept maps...")
    concept_map = mapper.generate_concept_map(all_concepts)
    with open(f"{OUTPUT_DIR}/concept_map.json", 'w') as f:
        json.dump(concept_map, f, indent=2)
    print(f"   ✓ {concept_map['total_concepts']} unique concepts identified")
    
    # Step 4: Create lesson templates
    print("\n[4/5] Generating lesson plan templates...")
    lesson_templates = {}
    top_concepts = [c[0] for c in concept_map['most_common_concepts'][:10]]
    for concept in top_concepts:
        lesson_templates[concept] = mapper.create_lesson_template(concept, "Intermediate")
    
    with open(f"{OUTPUT_DIR}/lesson_templates.json", 'w') as f:
        json.dump(lesson_templates, f, indent=2)
    print(f"   ✓ Created templates for {len(lesson_templates)} key concepts")
    
    # Step 5: Save detailed concepts
    print("\n[5/5] Saving detailed concept data...")
    with open(f"{OUTPUT_DIR}/extracted_concepts.json", 'w') as f:
        json.dump(all_concepts, f, indent=2)
    
    # Step 6: Create teacher guide
    print("\n[6/5] Creating teacher guide...")
    create_teacher_guide(concept_map, hierarchy)
    
    # Final summary
    print("\n" + "=" * 70)
    print("FRAMEWORK CREATION COMPLETE!")
    print("=" * 70)
    print(f"\n📊 Statistics:")
    print(f"   • Total PDB structures analyzed: {len(all_concepts)}")
    print(f"   • Unique concepts identified: {concept_map['total_concepts']}")
    print(f"   • Lesson templates created: {len(lesson_templates)}")
    print(f"\n📁 Output files in {OUTPUT_DIR}/:")
    print(f"   • concept_hierarchy.json - Learning progression map")
    print(f"   • concept_map.json - Frequency and examples")
    print(f"   • lesson_templates.json - Complete lesson plans")
    print(f"   • extracted_concepts.json - Detailed concept data")
    print(f"   • teacher_guide.md - Guide for educators")
    print(f"\n🎯 Next steps:")
    print(f"   1. Review concept_hierarchy.json to understand learning progression")
    print(f"   2. Use lesson_templates.json to develop curriculum")
    print(f"   3. Share concept maps with students for visual learning")
    print(f"   4. Reference PDB examples from concept_map.json in your lessons")


def create_teacher_guide(concept_map, hierarchy):
    """Create a markdown guide for teachers"""
    guide = """# MOLECULAR BIOLOGY CONCEPT MAPPER - Teacher's Guide

## Overview
This framework helps you create concept maps and lesson plans based on real protein structures from the Protein Data Bank (PDB).

## What is This Tool?
- **Data Source**: Real 3D protein structures from the RCSB PDB
- **Purpose**: Help students understand molecular biology through authentic scientific data
- **Approach**: Use scientific practices to scaffold learning from atoms to cellular function

## How to Use This Framework

### 1. Understanding Concept Hierarchies
The framework organizes concepts from basic to advanced:
- **Level 1**: Atoms, bonds, amino acids (building blocks)
- **Level 2**: Protein folding, secondary structures
- **Level 3**: Complex protein systems and quaternary structures
- **Level 4**: Biological function in cells
- **Level 5**: How scientists study proteins
- **Level 6**: Real-world applications

### 2. Creating Concept Maps
A concept map shows relationships between ideas:
```
Protein
  ├── Made of: Amino Acids
  │    └── Connected by: Peptide Bonds
  ├── Forms: Secondary Structures
  │    ├── α-helix
  │    └── β-sheet
  ├── Folds into: 3D Structure (Tertiary)
  │    └── Determines: Function
  └── Multiple copies: Quaternary Structure
       └── Example: Hemoglobin (4 subunits)
```

### 3. Using PDB Examples in Class
Each concept has real PDB structure examples. You can:
- Show students actual protein structures via RCSB PDB website
- Have students measure distances between atoms
- Ask students to predict function from structure
- Compare related proteins to see structure variations

### 4. Scientific Practices Integration
Each lesson incorporates the Next Generation Science Standards practices:
- **Asking Questions**: "Why does this protein have this shape?"
- **Developing Models**: Building 3D mental models of structures
- **Analyzing Data**: Using PDB data to support claims
- **Constructing Explanations**: Connecting structure to function
- **Engaging in Arguments**: Debating structure interpretations

### 5. Lesson Structure (5E Model)
Each lesson includes:
1. **Engagement**: Hook with interesting structure
2. **Exploration**: Students investigate the structure
3. **Explanation**: Teacher explains scientific principle
4. **Elaboration**: Apply to new examples
5. **Evaluation**: Assess student understanding

## Key Concepts by Level

### For High School Students:
- Protein structure basics
- How amino acid sequence determines shape
- Structure-function relationship
- Enzyme catalysis
- Antibody-antigen interactions

### For College Students:
- Detailed structural classification
- Thermodynamics of protein folding
- X-ray crystallography methods
- Cryo-EM data interpretation
- Protein dynamics and conformational changes

### For Research-Level:
- Advanced structural biology
- Molecular dynamics simulations
- Structure-guided drug design
- Protein engineering

## Resources for Your Classroom

### Websites
- **RCSB PDB** (www.rcsb.org): Access real structures
- **Mol\\* Viewer**: Online 3D structure visualization
- **NCBI Structure**: Sequence-structure relationships
- **PDBx/mmCIF Format**: Understanding structural data

### Teaching Tools
- 3D protein viewers (free online versions)
- Structure image collections
- Sequence alignment tools
- Mutation databases

## Assessment Ideas

### Formative Assessment
- **Observation**: Watch students explore PDB structures
- **Concept Sketches**: Have students draw what they observe
- **Exit Tickets**: Quick understanding checks
- **Peer Discussion**: Talk-aloud reasoning

### Summative Assessment
- **Concept Map Creation**: Students build their own concept hierarchies
- **Written Explanation**: Explain protein function from structure
- **Problem Solving**: Predict outcomes of mutations
- **Research Project**: Analyze a protein of interest

## Common Student Misconceptions

1. **"Proteins are static"**
   - Reality: Proteins are dynamic and flexible
   - Solution: Show protein dynamics simulations

2. **"All proteins are enzymes"**
   - Reality: Many structural, regulatory, and transport proteins exist
   - Solution: Classify proteins by function

3. **"Structure is determined by chemistry alone"**
   - Reality: Kinetics, thermodynamics, and cellular environment matter
   - Solution: Discuss protein misfolding and disease

4. **"Amino acids just link in a chain"**
   - Reality: Specific interactions between amino acids drive folding
   - Solution: Show how hydrophobic/hydrophilic properties drive structure

## Tips for Success

1. **Start Simple**: Begin with small, well-studied proteins
2. **Use Visuals**: Show many different structure representations
3. **Connect to Health**: Link proteins to diseases and treatments
4. **Make it Interactive**: Let students explore PDB structures
5. **Scaffold Complexity**: Build from one subunit to multi-subunit complexes
6. **Real Data**: Always use actual PDB data from research

## Sample Lesson Arc (Multi-day)

**Day 1**: What are amino acids? (Building blocks)
**Day 2**: How do they connect? (Peptide bonds)
**Day 3**: What shapes form? (Secondary structure)
**Day 4**: How do proteins fold? (Tertiary structure)
**Day 5**: What about multiple copies? (Quaternary structure)
**Day 6**: How do they work? (Function and catalysis)
**Day 7**: How do we study them? (Experimental methods)
**Day 8**: What goes wrong? (Mutations and disease)
**Day 9**: How can we fix it? (Biotechnology)
**Day 10**: Student presentations

## Questions to Ask Students

- "Why do you think this protein has this specific shape?"
- "How would changing one amino acid affect the function?"
- "What would happen if we heated this protein?"
- "How is this protein similar to/different from this other one?"
- "Why do you think scientists chose this method to study this protein?"
- "How could we use this protein to treat disease?"

## Further Learning
- Next Generation Science Standards (NGSS) alignments
- Integration with chemistry, physics, and health courses
- Connections to evolution and diversity
- Current research frontiers in structural biology

---
*Framework created using real protein structures from the RCSB Protein Data Bank*
*Designed to support evidence-based, inquiry-driven science education*
"""
    
    with open(f"{OUTPUT_DIR}/teacher_guide.md", 'w') as f:
        f.write(guide)


if __name__ == "__main__":
    main()
