import json
import statistics

# Load the extracted features
with open('model_data/features.json') as f:
    features = json.load(f)

print("=" * 70)
print("PDB DATASET ANALYSIS & MODEL INSIGHTS")
print("=" * 70)

# Filter by experiment type
xray = [f for f in features if f['is_xray'] == 1]
em = [f for f in features if f['is_em'] == 1]
nmr = [f for f in features if f['is_nmr'] == 1]

print(f"\n[DATA SUMMARY]")
print(f"  Total structures: {len(features)}")
print(f"  X-Ray Diffraction: {len(xray)}")
print(f"  Electron Microscopy: {len(em)}")
print(f"  NMR: {len(nmr)}")

# Resolution analysis
xray_res = [f['resolution'] for f in xray if f['resolution'] > 0]
em_res = [f['resolution'] for f in em if f['resolution'] > 0]

print(f"\n[RESOLUTION QUALITY]")
if xray_res:
    print(f"  X-Ray Resolution (Å):")
    print(f"    Count: {len(xray_res)}/{len(xray)}")
    print(f"    Range: {min(xray_res):.2f} - {max(xray_res):.2f}")
    print(f"    Mean: {statistics.mean(xray_res):.2f}")
    print(f"    Median: {statistics.median(xray_res):.2f}")

if em_res:
    print(f"\n  Cryo-EM Resolution (Å):")
    print(f"    Count: {len(em_res)}/{len(em)}")
    print(f"    Range: {min(em_res):.2f} - {max(em_res):.2f}")
    print(f"    Mean: {statistics.mean(em_res):.2f}")
    print(f"    Median: {statistics.median(em_res):.2f}")

# Complexity analysis
poly_counts = [f['polymer_entity_count'] for f in features]
water_counts = [f['water_entity_count'] for f in features]
nonpoly_counts = [f['nonpolymer_entity_count'] for f in features]

print(f"\n[STRUCTURAL COMPLEXITY]")
print(f"  Polymer Entities:")
print(f"    Range: {min(poly_counts)} - {max(poly_counts)}")
print(f"    Mean: {statistics.mean(poly_counts):.1f}")
print(f"  Water Molecules:")
print(f"    Range: {min(water_counts)} - {max(water_counts)}")
print(f"    Mean: {statistics.mean(water_counts):.1f}")
print(f"  Non-Polymer Entities:")
print(f"    Range: {min(nonpoly_counts)} - {max(nonpoly_counts)}")
print(f"    Mean: {statistics.mean(nonpoly_counts):.1f}")

# Cell dimensions
cell_volumes = [f['cell_volume'] for f in features if f['cell_volume'] > 0]
cell_a_vals = [f['cell_a'] for f in features if f['cell_a'] > 0]

print(f"\n[UNIT CELL]")
if cell_volumes:
    print(f"  Volume (Ų):")
    print(f"    Range: {min(cell_volumes):.0f} - {max(cell_volumes):.0f}")
    print(f"    Mean: {statistics.mean(cell_volumes):.0f}")

if cell_a_vals:
    print(f"  Dimension A (Å):")
    print(f"    Range: {min(cell_a_vals):.1f} - {max(cell_a_vals):.1f}")
    print(f"    Mean: {statistics.mean(cell_a_vals):.1f}")

# Insights
print(f"\n[KEY INSIGHTS FOR MODELING]")
print(f"  ✓ Good size dataset: {len(features)} structures")
print(f"  ✓ Diverse methods: X-ray, Cryo-EM")
print(f"  ✓ Variable complexity: Polymers range from 1-{max(poly_counts)} entities")

if xray_res or em_res:
    print(f"  ✓ Resolution data available for {len(xray_res) + len(em_res)} structures")
    print(f"  → Can predict resolution quality from structural features")

high_res = sum(1 for r in (xray_res + em_res) if r < 2.5)
print(f"  → {high_res}/{len(xray_res) + len(em_res)} structures have high resolution (< 2.5 Å)")

print(f"\n[RECOMMENDED MODEL TARGETS]")
print(f"  1. Predict resolution quality (regression)")
print(f"  2. Classify structure complexity (easy/medium/hard)")
print(f"  3. Predict experiment type (X-ray vs Cryo-EM)")
print(f"  4. Estimate # of polymer entities")

print("\n" + "=" * 70)
print("Ready to build your machine learning model!")
print("=" * 70)
