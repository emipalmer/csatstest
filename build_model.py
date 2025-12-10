import json
import os
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# Configuration
JSON_DIR = "./pdb_data"
OUTPUT_DIR = "./model_data"

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_features(json_data):
    """Extract features from PDB JSON data"""
    features = {}
    
    try:
        # Basic structure info
        struct_data = json_data.get('struct', {})
        features['title'] = struct_data.get('title', '')
        
        # Polymer info
        poly_data = json_data.get('polymer', {})
        features['polymer_count'] = len(poly_data.get('pdb_chains', []))
        
        # Get average monomer count
        monomer_counts = []
        for chain_data in poly_data.get('pdb_chains', []):
            monomer_counts.append(len(chain_data.get('monomers', [])))
        features['avg_monomers'] = np.mean(monomer_counts) if monomer_counts else 0
        features['max_monomers'] = np.max(monomer_counts) if monomer_counts else 0
        
        # Crystallography info
        exptl_data = json_data.get('exptl', [{}])[0]
        features['resolution'] = float(exptl_data.get('resolution', 0)) if exptl_data.get('resolution') else 0
        
        # Release date (convert to numerical days since epoch)
        release_date = json_data.get('rcsb_accession_info', {}).get('release_date', '')
        features['has_release_date'] = 1 if release_date else 0
        
        return features
    except Exception as e:
        print(f"Error extracting features: {e}")
        return None

def load_json_files(directory):
    """Load all JSON files from directory"""
    data = []
    files = list(Path(directory).glob("*.json"))
    
    print(f"Loading {len(files)} JSON files...")
    
    for i, json_file in enumerate(files):
        if i % 100 == 0:
            print(f"  Processed {i}/{len(files)}")
        
        try:
            with open(json_file, 'r') as f:
                json_data = json.load(f)
                features = extract_features(json_data)
                if features:
                    features['pdb_id'] = json_file.stem
                    data.append(features)
        except Exception as e:
            print(f"Error loading {json_file}: {e}")
    
    return data

def main():
    print("=" * 60)
    print("PDB Model Builder")
    print("=" * 60)
    
    # Load data
    print("\n1. Loading JSON files...")
    raw_data = load_json_files(JSON_DIR)
    print(f"   Loaded {len(raw_data)} records")
    
    # Create DataFrame
    print("\n2. Creating DataFrame...")
    df = pd.DataFrame(raw_data)
    print(df.head())
    print(f"\n   Shape: {df.shape}")
    print(f"\n   Data types:\n{df.dtypes}")
    print(f"\n   Missing values:\n{df.isnull().sum()}")
    
    # Basic statistics
    print("\n3. Feature Statistics:")
    print(df.describe())
    
    # Prepare features for modeling
    print("\n4. Preparing features for modeling...")
    
    # Select numerical features
    numerical_features = ['polymer_count', 'avg_monomers', 'max_monomers', 'resolution', 'has_release_date']
    
    # Create feature matrix
    X = df[numerical_features].copy()
    
    # Fill NaN values
    X = X.fillna(X.mean())
    
    print(f"   Feature matrix shape: {X.shape}")
    print(f"   Features: {list(X.columns)}")
    
    # Create target (using resolution as target for demonstration)
    # This could be changed based on your modeling goal
    y = df['resolution'].copy()
    
    # Filter out invalid resolution values
    valid_idx = (y > 0) & (y < 10)  # Reasonable resolution range
    X = X[valid_idx]
    y = y[valid_idx]
    
    print(f"   Valid samples: {len(X)}")
    
    if len(X) < 10:
        print("\n   ⚠️  Not enough valid samples to build a model!")
        print("   Please download more JSON files and try again.")
        return
    
    # Split data
    print("\n5. Splitting data (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"   Training samples: {len(X_train)}")
    print(f"   Test samples: {len(X_test)}")
    
    # Normalize features
    print("\n6. Normalizing features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Build model
    print("\n7. Training Random Forest model...")
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    print("\n8. Model Evaluation:")
    y_pred = model.predict(X_test_scaled)
    
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    print(f"   MSE: {mse:.4f}")
    print(f"   RMSE: {rmse:.4f}")
    print(f"   R² Score: {r2:.4f}")
    
    # Feature importance
    print("\n9. Feature Importance:")
    importance_df = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    print(importance_df)
    
    # Save results
    print("\n10. Saving results...")
    df.to_csv(f"{OUTPUT_DIR}/features.csv", index=False)
    importance_df.to_csv(f"{OUTPUT_DIR}/feature_importance.csv", index=False)
    
    # Save summary
    with open(f"{OUTPUT_DIR}/model_summary.txt", 'w') as f:
        f.write("PDB MODEL SUMMARY\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Total samples: {len(df)}\n")
        f.write(f"Valid training samples: {len(X_train)}\n")
        f.write(f"Valid test samples: {len(X_test)}\n\n")
        f.write("MODEL PERFORMANCE\n")
        f.write(f"RMSE: {rmse:.4f}\n")
        f.write(f"R² Score: {r2:.4f}\n\n")
        f.write("FEATURE IMPORTANCE\n")
        f.write(importance_df.to_string())
    
    print(f"   ✓ Saved to {OUTPUT_DIR}/")
    
    print("\n" + "=" * 60)
    print("Model building complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
