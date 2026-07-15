"""
Generate a realistic 'Green Skills & Sustainability' country-level dataset.

Since this is a synthetic dataset (built to mimic real-world sustainability
indicators such as those published by IEA, World Bank, and IRENA), it is
seeded with 4 latent country archetypes so that K-Means has genuine
structure to discover -- then noise + missing values + duplicates are
added to make it realistic for a data-cleaning exercise.
"""

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

N_PER_GROUP = 45  # 4 groups x 45 = 180 countries (synthetic names)

# ---------------------------------------------------------------------------
# 1. Define 4 latent "archetypes" of countries w.r.t. green/sustainability
#    profile. Each archetype has different typical ranges for each feature.
# ---------------------------------------------------------------------------
archetypes = {
    "green_leader": dict(          # Nordic-style: high renewables, low emissions
        renewable_share=(55, 90),
        co2_per_capita=(2, 6),
        energy_per_capita=(3000, 7000),
        green_jobs_pct=(6, 14),
        forest_area_pct=(30, 70),
        recycling_rate=(45, 75),
        gdp_per_capita=(35000, 75000),
        env_policy_score=(70, 95),
    ),
    "industrial_high_emission": dict(   # heavy industry, high emissions
        renewable_share=(8, 25),
        co2_per_capita=(8, 16),
        energy_per_capita=(5000, 9000),
        green_jobs_pct=(1, 4),
        forest_area_pct=(5, 25),
        recycling_rate=(10, 30),
        gdp_per_capita=(15000, 35000),
        env_policy_score=(30, 55),
    ),
    "emerging_transitioning": dict(     # developing, growing green investment
        renewable_share=(20, 45),
        co2_per_capita=(3, 8),
        energy_per_capita=(1500, 4000),
        green_jobs_pct=(2, 6),
        forest_area_pct=(15, 45),
        recycling_rate=(15, 40),
        gdp_per_capita=(4000, 15000),
        env_policy_score=(40, 65),
    ),
    "resource_constrained": dict(       # low income & infrastructure, low emissions
        renewable_share=(10, 35),
        co2_per_capita=(0.3, 2.5),
        energy_per_capita=(300, 1200),
        green_jobs_pct=(0.5, 2.5),
        forest_area_pct=(10, 55),
        recycling_rate=(3, 15),
        gdp_per_capita=(700, 4000),
        env_policy_score=(15, 40),
    ),
}

feature_names = list(next(iter(archetypes.values())).keys())

rows = []
for group, ranges in archetypes.items():
    for i in range(N_PER_GROUP):
        row = {"country": f"{group}_{i+1:02d}", "true_group": group}
        for feat, (lo, hi) in ranges.items():
            row[feat] = rng.uniform(lo, hi)
        rows.append(row)

df = pd.DataFrame(rows)

# ---------------------------------------------------------------------------
# 2. Inject realism: missing values, duplicate rows, outliers (messy data
#    for the cleaning step).
# ---------------------------------------------------------------------------
feat_cols = feature_names
mask = rng.random((len(df), len(feat_cols))) < 0.04
for j, col in enumerate(feat_cols):
    df.loc[mask[:, j], col] = np.nan

dupes = df.sample(6, random_state=1)
df = pd.concat([df, dupes], ignore_index=True)

outlier_idx = rng.choice(df.index, size=4, replace=False)
df.loc[outlier_idx[0], "co2_per_capita"] = 55.0
df.loc[outlier_idx[1], "energy_per_capita"] = -500
df.loc[outlier_idx[2], "recycling_rate"] = 130
df.loc[outlier_idx[3], "gdp_per_capita"] = 250000

df = df.sample(frac=1, random_state=7).reset_index(drop=True)

out_path = "/home/claude/project/data/green_sustainability_raw.csv"
df.to_csv(out_path, index=False)
print(f"Saved raw dataset: {out_path}")
print(df.shape)
print(df.head())
