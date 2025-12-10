# 🔍 Molecular Biology Query System

Easy command-line access to your educational model with 1,061 protein structures.

## Quick Start

```bash
# Show dataset statistics
python3 query.py --stats

# Search for concepts containing "enzyme"
python3 query.py enzyme

# Look up a specific PDB ID
python3 query.py 1A02

# Search by concept
python3 query.py --concept "protein structure"

# Filter by experimental method
python3 query.py --method "cryo-em"

# Filter by complexity level
python3 query.py --complexity "advanced"

# Show help
python3 query.py --help
```

## Features

✅ **Concept Search** - Find structures by molecular biology concepts
✅ **PDB Lookup** - Get detailed info about specific protein structures  
✅ **Method Filtering** - Filter by X-ray crystallography or Cryo-EM
✅ **Complexity Levels** - Find structures appropriate for different student levels
✅ **Statistics** - Overview of your complete dataset
✅ **Quick Search** - Simple positional arguments for common queries

## Example Queries

```bash
# Teaching about enzymes
python3 query.py enzyme

# Looking up transcription factors
python3 query.py --concept "gene expression"

# Finding high-resolution X-ray structures
python3 query.py --method "x-ray"

# Getting basic level structures for intro students
python3 query.py --complexity "basic"

# Look up the NFAT/DNA complex structure
python3 query.py 1A02
```

## Your Dataset

- 📊 **1,061 protein structures** total
- 🧬 **15 unique molecular biology concepts**
- 🔬 **746 Cryo-EM** structures + **315 X-ray** structures  
- 🎓 **Advanced** (1,034) and **Intermediate** (27) complexity levels
- 🧪 Covers: protein structure, gene expression, enzyme function, and more

## Files Created

- `query.py` - Main query script
- `molbio` - Bash wrapper (use `python3 query.py` instead on Windows)
- `QUERY_README.md` - This usage guide