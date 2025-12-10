import json
import os
from pathlib import Path
import statistics

# Configuration
JSON_DIR = "./pdb_data"
OUTPUT_DIR = "./model_data"

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_features(json_data):
    """Extract features from PDB JSON data"""
    features = {}
    
    try:
        features['pdb_id'] = json_data.get('rcsb_id', '')
        
        # Experimental method
        exptl_method = json_data.get('exptl', [{}])[0].get('method', 'UNKNOWN')
        features['method'] = exptl_method
        features['is_xray'] = 1 if 'X-RAY' in exptl_method else 0
        features['is_nmr'] = 1 if 'NMR' in exptl_method else 0
        features['is_em'] = 1 if 'ELECTRON' in exptl_method or 'CRYO-EM' in exptl_method else 0
        
        # Resolution from reflections
        reflns = json_data.get('reflns', [{}])[0]
        features['resolution'] = float(reflns.get('d_resolution_high', 0)) if reflns.get('d_resolution_high') else 0
        
        # Unit cell
        cell = json_data.get('cell', {})
        features['cell_volume'] = float(cell.get('volume', 0)) if cell.get('volume') else 0
        features['cell_a'] = float(cell.get('length_a', 0)) if cell.get('length_a') else 0
        features['cell_b'] = float(cell.get('length_b', 0)) if cell.get('length_b') else 0
        features['cell_c'] = float(cell.get('length_c', 0)) if cell.get('length_c') else 0
        
        # Structure info
        struct = json_data.get('struct', {})
        features['title'] = struct.get('title', '')
        
        # Refinement statistics
        refine = json_data.get('refine', [{}])[0]
        features['r_work'] = float(refine.get('ls_R_factor_R_work', 0)) if refine.get('ls_R_factor_R_work') else 0
        features['r_free'] = float(refine.get('ls_R_factor_R_free', 0)) if refine.get('ls_R_factor_R_free') else 0
        
        # Entry info
        entry_info = json_data.get('rcsb_entry_info', {})
        features['polymer_entity_count'] = int(entry_info.get('polymer_entity_count', 0)) or 0
        features['nonpolymer_entity_count'] = int(entry_info.get('nonpolymer_entity_count', 0)) or 0
        features['water_entity_count'] = int(entry_info.get('water_entity_count', 0)) or 0
        
        # Deposition date
        accession = json_data.get('rcsb_accession_info', {})
        features['has_deposition_date'] = 1 if accession.get('deposit_date') else 0
        
        return features
    except Exception as e:
        return None

def load_json_files(directory):
    """Load all JSON files from directory"""
    data = []
    files = list(Path(directory).glob("*.json"))
    
    print(f"Loading {len(files)} JSON files...")
    
    for i, json_file in enumerate(files):
        if i % 100 == 0 and i > 0:
            print(f"  Processed {i}/{len(files)}")
        
        try:
            with open(json_file, 'r') as f:
                json_data = json.load(f)
                features = extract_features(json_data)
                if features:
                    data.append(features)
        except Exception as e:
            pass  # Skip files with errors
    
    return data

def main():
    print("=" * 70)
    print("PDB MODEL BUILDING - FEATURE EXTRACTION")
    print("=" * 70)
    
    # Load data
    print("\n[1/4] Loading JSON files...")
    raw_data = load_json_files(JSON_DIR)
    print(f"   ✓ Loaded {len(raw_data)} records\n")
    
    if len(raw_data) < 10:
        print("   ⚠️  Not enough records to build a model!")
        return
    
    # Analyze features
    print("[2/4] Analyzing extracted features...")
    
    # Resolution statistics
    resolutions = [d['resolution'] for d in raw_data if d['resolution'] > 0]
    print(f"\n   Resolution (Å) - {len(resolutions)} valid entries:")
    if resolutions:
        print(f"     Range: {min(resolutions):.2f} - {max(resolutions):.2f}")
        print(f"     Mean: {statistics.mean(resolutions):.2f}")
    
    # Method distribution
    methods = {}
    for d in raw_data:
        m = d['method']
        methods[m] = methods.get(m, 0) + 1
    print(f"\n   Experimental Methods:")
    for method, count in sorted(methods.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"     {method}: {count}")
    
    # R-factor statistics
    r_works = [d['r_work'] for d in raw_data if d['r_work'] > 0]
    r_frees = [d['r_free'] for d in raw_data if d['r_free'] > 0]
    
    if r_works:
        print(f"\n   R-Work - {len(r_works)} valid entries:")
        print(f"     Range: {min(r_works):.4f} - {max(r_works):.4f}")
        print(f"     Mean: {statistics.mean(r_works):.4f}")
    
    if r_frees:
        print(f"\n   R-Free - {len(r_frees)} valid entries:")
        print(f"     Range: {min(r_frees):.4f} - {max(r_frees):.4f}")
        print(f"     Mean: {statistics.mean(r_frees):.4f}")
    
    # Polymer info
    poly_counts = [d['polymer_entity_count'] for d in raw_data]
    print(f"\n   Polymer Entities:")
    print(f"     Range: {min(poly_counts)} - {max(poly_counts)}")
    print(f"     Mean: {statistics.mean(poly_counts):.2f}")
    
    # Save extracted features
    print("\n[3/4] Saving extracted features...")
    
    with open(f"{OUTPUT_DIR}/features.json", 'w') as f:
        json.dump(raw_data, f, indent=2)
    print(f"   ✓ features.json ({len(raw_data)} records)")
    
    # Summary statistics
    summary = {
        "total_records": len(raw_data),
        "resolution": {
            "valid_entries": len(resolutions),
            "min": min(resolutions) if resolutions else None,
            "max": max(resolutions) if resolutions else None,
            "mean": statistics.mean(resolutions) if resolutions else None,
        },
        "r_work": {
            "valid_entries": len(r_works),
            "mean": statistics.mean(r_works) if r_works else None,
        },
        "r_free": {
            "valid_entries": len(r_frees),
            "mean": statistics.mean(r_frees) if r_frees else None,
        },
        "polymer_entities": {
            "min": min(poly_counts),
            "max": max(poly_counts),
            "mean": statistics.mean(poly_counts),
        },
        "methods": methods
    }
    
    with open(f"{OUTPUT_DIR}/summary.json", 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"   ✓ summary.json")
    
    print("\n[4/4] Ready for model training!")
    print("\n" + "=" * 70)
    print("NEXT STEPS:")
    print("=" * 70)
    print("""
To build a machine learning model, you have two options:

OPTION 1: Use scikit-learn (requires installation)
  pip install pandas numpy scikit-learn
  python3 build_model.py

OPTION 2: Simple statistical analysis (no dependencies)
  python3 analyze_model.py

Start with Option 2 to explore your data, then move to Option 1
for more advanced machine learning models!
""")

if __name__ == "__main__":
    main()
