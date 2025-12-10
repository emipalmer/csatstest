"""
QUICK START GUIDE FOR TEACHERS
Generate ready-to-use lesson outlines from the educational framework
"""

import json
import os

OUTPUT_DIR = "./educational_framework"

def create_quick_start():
    """Create a quick start guide with immediate lesson ideas"""
    
    # Load the concept map
    with open(f"{OUTPUT_DIR}/concept_map.json") as f:
        concept_map = json.load(f)
    
    # Create quick lesson ideas
    quick_lessons = {
        "5_minute_hook": {
            "title": "5-Minute Classroom Hook",
            "description": "Grab student attention in 5 minutes",
            "idea": """
Show students this image:
A colorful 3D protein structure from RCSB PDB

Ask: "What is this?"
"Is it art? Is it alive? Is it a building blueprint?"

Answer: "It's a PROTEIN! A single molecule from your body right now!"

"Every day, your cells are making thousands of these structures.
Your hair, your muscles, your immune system—all made of proteins.
Today, we're going to learn what proteins are and how they work."

Resources:
- Visit www.rcsb.org
- Search for "insulin" or "hemoglobin"
- Show the 3D structure in Mol* Viewer
            """
        },
        
        "structure_function_lesson": {
            "title": "Protein Structure Determines Function",
            "duration": "1 class period",
            "standards_aligned": ["NGSS HS-LS1-1", "NGSS HS-LS1-2"],
            "learning_target": "Students will understand that protein shape determines what it does",
            "lesson_steps": [
                {
                    "step": 1,
                    "phase": "Engagement (5 min)",
                    "activity": "Show a lock and key. Ask: What would happen if the key was bent?",
                    "science_practice": "Asking Questions"
                },
                {
                    "step": 2,
                    "phase": "Exploration (10 min)",
                    "activity": "Students explore a protein structure online at RCSB PDB. Find the 'active site'.",
                    "science_practice": "Asking Questions, Analyzing Data",
                    "materials": "Computer access, RCSB PDB website"
                },
                {
                    "step": 3,
                    "phase": "Explanation (10 min)",
                    "activity": "Explain: Proteins have specific shapes like keys. When a substrate (ligand) fits, it works!",
                    "science_practice": "Developing & Using Models",
                    "discussion": "Why would a slightly different shape not work? (Lock and key analogy)"
                },
                {
                    "step": 4,
                    "phase": "Elaboration (10 min)",
                    "activity": "Mutation challenge: Show what happens when a protein is mutated (shape changes).",
                    "examples": [
                        "Sickle cell: Hemoglobin mutation changes shape",
                        "Cystic fibrosis: CFTR protein can't fold correctly"
                    ],
                    "science_practice": "Constructing Explanations"
                },
                {
                    "step": 5,
                    "phase": "Evaluation (5 min)",
                    "activity": "Exit ticket: Draw a protein shape and explain why shape matters.",
                    "assessment": "Conceptual understanding of structure-function"
                }
            ]
        },
        
        "experimental_methods_lesson": {
            "title": "How Do Scientists See Proteins?",
            "duration": "2-3 class periods",
            "standards_aligned": ["NGSS HS-ETS1-1", "Scientific practices"],
            "learning_target": "Understand how X-ray crystallography and Cryo-EM reveal protein structures",
            "lesson_steps": [
                {
                    "step": 1,
                    "activity": "Show X-ray diffraction pattern image",
                    "question": "What is this? How does it show us what proteins look like?"
                },
                {
                    "step": 2,
                    "activity": "Explain X-ray crystallography (simplified)",
                    "key_points": [
                        "Grow protein crystals",
                        "Shoot X-rays through them",
                        "Measure diffraction pattern",
                        "Computer reconstructs 3D model"
                    ]
                },
                {
                    "step": 3,
                    "activity": "Compare with Cryo-EM",
                    "key_points": [
                        "Freeze proteins in ice",
                        "Shoot electrons (not X-rays)",
                        "Take thousands of 2D images",
                        "Combine images to build 3D model"
                    ]
                },
                {
                    "step": 4,
                    "activity": "Show resolution comparison",
                    "discussion": "Higher resolution = more detail. Why does this matter?"
                },
                {
                    "step": 5,
                    "activity": "Find real examples in PDB database",
                    "task": "Search for a structure solved by X-ray and another by Cryo-EM"
                }
            ]
        },
        
        "gene_to_protein_lesson": {
            "title": "From DNA to Protein to Function",
            "duration": "3-4 class periods",
            "standards_aligned": ["NGSS HS-LS3-1"],
            "learning_target": "Connect DNA sequence → Protein structure → Biological function",
            "concept_map": """
            DNA Sequence
                    ↓
            (Transcription)
                    ↓
            mRNA Sequence
                    ↓
            (Translation)
                    ↓
            Amino Acid Sequence
                    ↓
            (Protein Folding)
                    ↓
            3D Protein Structure
                    ↓
            Biological Function
                    
            Example: Insulin Gene
            - Shows how changing one DNA base
            - Changes one amino acid
            - Changes protein shape
            - Changes how well it works
            """
        },
        
        "disease_and_mutation_lesson": {
            "title": "When Proteins Go Wrong: Genetic Disease",
            "duration": "2-3 class periods",
            "standards_aligned": ["NGSS HS-LS4-3"],
            "learning_target": "Understand how protein mutations cause disease",
            "examples": {
                "Sickle Cell Anemia": {
                    "mutation": "One amino acid change in hemoglobin",
                    "effect": "Proteins polymerize, distort cells",
                    "pdb_examples": ["1A3N - Normal hemoglobin", "2M2C - Sickle hemoglobin"]
                },
                "Cystic Fibrosis": {
                    "mutation": "CFTR protein can't fold correctly",
                    "effect": "Protein gets degraded, can't transport chloride",
                    "result": "Thick mucus builds up in lungs"
                },
                "Huntington's Disease": {
                    "mutation": "Huntingtin protein has extra repeats",
                    "effect": "Protein misfolds, forms aggregates",
                    "result": "Neurodegeneration"
                }
            }
        },
        
        "biotechnology_lesson": {
            "title": "Using Proteins to Solve Problems",
            "duration": "2 class periods",
            "standards_aligned": ["NGSS HS-ETS1-3"],
            "learning_target": "Understand applications of protein science",
            "applications": [
                "Insulin production: Genetically engineered bacteria",
                "Antibodies as medicine: Monoclonal antibodies for cancer",
                "CRISPR: Using bacterial proteins for gene editing",
                "Enzyme engineering: Proteins that break down plastic",
                "Personalized medicine: Targeting proteins based on mutations"
            ]
        },
        
        "student_projects": {
            "title": "Student Project Ideas",
            "difficulty_levels": {
                "Easy (1-2 weeks)": [
                    "Compare protein structures from two organisms (e.g., human vs. pig insulin)",
                    "Create a 3D model of a protein using craft materials",
                    "Write a 'biography' of a protein - origin, function, diseases",
                    "Analyze how resolution affects structure detail"
                ],
                "Medium (2-4 weeks)": [
                    "Research a genetic disease caused by protein mutation",
                    "Design an experiment to test protein folding conditions",
                    "Compare evolutionary relationships using protein sequences",
                    "Analyze a drug target by studying its protein structure"
                ],
                "Advanced (4+ weeks)": [
                    "Molecular dynamics simulation of protein folding",
                    "Design a protein variant with improved function",
                    "Analyze cryo-EM data and build a structure",
                    "Research and propose treatment for protein misfolding disease"
                ]
            }
        },
        
        "assessment_ideas": {
            "formative": [
                "Concept sketches (draw what you observe in 3D structure)",
                "Exit tickets (1-2 minute explanations)",
                "Peer teaching (explain concept to classmate)",
                "Structure prediction (what will happen if we change this?)"
            ],
            "summative": [
                "Concept map exam (draw relationships between concepts)",
                "Written explanation (explain a protein's function from its structure)",
                "Problem solving (analyze a mutation and predict effects)",
                "Research project (deep dive into a protein-related disease or technology)"
            ]
        },
        
        "common_questions": {
            "question": "Why are proteins important?",
            "answer": "Proteins do almost all the work in living things - enzymes, structure, movement, immunity, etc."
        }
    }
    
    # Save quick start guide
    with open(f"{OUTPUT_DIR}/quick_start_lessons.json", 'w') as f:
        json.dump(quick_lessons, f, indent=2)
    
    # Create a text version too
    text_guide = """
================================================================================
QUICK START LESSON IDEAS FOR TEACHERS
Using Real PDB Data to Teach Molecular Biology
================================================================================

LESSON 1: 5-Minute Hook (Get Them Interested!)
──────────────────────────────────────────────
Show a colorful 3D protein structure from RCSB PDB
Ask: "Is this art? A building? A living thing?"
Answer: "It's a PROTEIN - made by your cells RIGHT NOW!"

Go to: www.rcsb.org
Search: "insulin" or "hemoglobin"
Click: 3D View → Shows beautiful structure
Action: Let students explore and click around


LESSON 2: Structure Determines Function (1 Class Period)
─────────────────────────────────────────────────────────
Analogy: Lock and Key
- Shape of enzyme = lock
- Shape of substrate = key
- When key fits, it works!
- If shape is wrong, it doesn't work

Real Examples:
1. Insulin protein (hormone)
   - Makes energy production work
   - In diabetes, either can't make it or can't use it
   
2. Hemoglobin (oxygen carrier)
   - Normal: Carries oxygen around body
   - Sickle cell mutation: One amino acid different
   - Result: Cells become sickle-shaped, block blood vessels

Activity: Go to RCSB PDB
- Search "insulin" → Look at shape
- Search "hemoglobin" → Find the active site
- Students: "What could break this?", "What would happen if...?"


LESSON 3: How Scientists See Proteins (2-3 Periods)
────────────────────────────────────────────────────
Problem: Proteins are way too small to see with microscopes!

Solution 1: X-ray Crystallography
- Grow protein crystals
- Shine X-rays on them
- Measure the diffraction pattern
- Computer builds 3D model
- Nobel Prize winners: Bragg family (1915)

Solution 2: Cryo-EM (Electron Microscopy)
- Freeze proteins in super-cold ice
- Shoot electrons at them (more powerful than light)
- Take thousands of images
- Computer combines them into 3D structure
- Nobel Prize 2017: Jacques Dubochet, Joachim Frank, Richard Henderson

Show Students:
- X-ray diffraction image (looks like dots in a pattern)
- Cryo-EM images (looks like fuzzy dots)
- Final 3D structure (beautiful!)
- Ask: "How would you turn blurry images into a clear 3D model?"


LESSON 4: DNA → RNA → Protein → Function
──────────────────────────────────────────
Show the flow:
DNA Code
  ↓ (Transcription in nucleus)
mRNA Message
  ↓ (Travel to ribosome)
Protein Structure
  ↓ (Fold into 3D)
Biological Function

Real Example - Insulin Gene:
ORIGINAL: ...GAA... (codes for glutamic acid)
MUTATION: ...GUA... (codes for valine) [One base change!]
RESULT: Different amino acid → Different shape → Doesn't work as well

Activity: Show DNA sequence in NCBI
- Find corresponding protein sequence
- Look up that protein structure in PDB
- Discuss: "What does changing one letter do?"


LESSON 5: When Proteins Break (Genetic Diseases)
─────────────────────────────────────────────────
Disease = Protein doesn't work right

SICKLE CELL ANEMIA
- Hemoglobin protein has mutation
- Changed shape makes proteins stick together
- Red blood cells become sickle-shaped
- Block blood vessels → pain and damage

CYSTIC FIBROSIS
- CFTR protein can't fold correctly
- Misfolded proteins get destroyed
- Can't transport salt and water
- Thick mucus builds up in lungs

HUNTINGTON'S DISEASE
- Huntingtin protein has too many repeats
- Protein misfolds and clumps
- Kills brain cells
- No symptoms until midlife

Activity: Choose a disease
1. Research the mutated protein
2. Find it in PDB database
3. Create a presentation explaining:
   - Normal version vs mutated version
   - Why the mutation causes the disease
   - Possible treatments


LESSON 6: Real-World Applications
──────────────────────────────────
INSULIN
- Extracted from pigs and cows (expensive, limited supply)
- Now: Use genetic engineering
- Insert human insulin gene into bacteria
- Bacteria make human insulin!
- Cost: Down 90%, available to more people

ANTIBODIES as MEDICINE
- Your immune system makes antibodies (Y-shaped proteins)
- Can be designed to attack cancer cells
- Called "monoclonal antibodies"
- Herceptin: Designed to attack breast cancer proteins
- Approved by FDA, saves lives

CRISPR GENE EDITING
- Uses bacterial proteins (Cas9)
- Can edit DNA precisely
- Could fix genetic diseases before symptoms
- Future: Personalized medicine based on your DNA


QUICK ACTIVITY IDEAS
────────────────────
🔬 Measure protein distances
- Open structure in Mol* (mol-star.org)
- Measure distance between two atoms
- Discuss: Why might this distance matter?

🧬 Compare protein sequences
- Use NCBI BLAST
- Compare human insulin to pig, cow, chicken
- Count amino acid differences
- Ask: "Why are some sequences more similar?"

🎨 Draw your observations
- Students sketch what they see in 3D structure
- Label parts (active site, binding pocket, domains)
- Explain relationships in a concept map

🔍 Mutation prediction
- Show a specific amino acid position
- Ask: "What happens if we change this to a different amino acid?"
- Check literature or databases for real mutation effects

📊 Data analysis
- Graph resolution vs discovery date
- Ask: "Is technology improving? How?"
- Project: Future of protein structure determination


ASSESSMENT
──────────
Formative (During learning):
- Observation checklist while exploring PDB
- Student questions (best ones show thinking)
- Peer explanations
- Concept sketches with labels

Summative (After learning):
- Written: Explain how a protein's structure determines its function
- Visual: Create a concept map of protein science
- Problem: Given a mutation, predict its effect
- Project: Analyze a disease-causing protein


RESOURCES FOR YOUR CLASSROOM
────────────────────────────
FREE Online Tools:
✓ RCSB PDB (www.rcsb.org) - Access all protein structures
✓ Mol* Viewer (mol-star.org) - Beautiful 3D visualization
✓ NCBI BLAST (blast.ncbi.nlm.nih.gov) - Compare sequences
✓ Jmol (jmol.sourceforge.net) - Open source viewer
✓ PyMOL Educational License - Professional tool

Lesson Resources:
✓ PDB Education Portal (www.rcsb.org/learn)
✓ Khan Academy - Protein structure videos
✓ Nature Scitable - Free biology lessons
✓ YouTube: "Protein Structure Visualization"

Real Research:
✓ PubMed Central - Read actual research papers
✓ bioRxiv - Preprints from cutting-edge research
✓ Disease-specific databases (e.g., CysticFibrosisDB)


NEXT STEPS
──────────
1. Pick ONE lesson from above
2. Try it with a small class or pilot group
3. Collect student feedback
4. Refine and improve
5. Share what you learn with other teachers!

Remember: You're teaching WITH REAL SCIENTIFIC DATA
Your students are learning what ACTUAL RESEARCHERS use
This is authentic science education! 🔬

Questions? Visit RCSB PDB education portal for support!

================================================================================
"""
    
    with open(f"{OUTPUT_DIR}/quick_start_lessons.txt", 'w') as f:
        f.write(text_guide)
    
    print("✓ Quick start lessons created!")
    return quick_lessons


if __name__ == "__main__":
    print("Creating quick start lesson guide...")
    create_quick_start()
    print("\n✓ Files created:")
    print("  - quick_start_lessons.json (structured data)")
    print("  - quick_start_lessons.txt (teacher-friendly format)")
    print("\nOpen quick_start_lessons.txt to see lesson ideas!")
