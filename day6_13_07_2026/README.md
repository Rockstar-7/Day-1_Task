# Green Skills & Sustainability Clustering — K-Means Analysis

## 1. Dataset
`data/green_sustainability_raw.csv` — 186 country-level records with 8 sustainability /
green-skill indicators:

| Feature | Meaning |
|---|---|
| renewable_share | % of energy from renewables |
| co2_per_capita | CO2 emissions per capita (tons) |
| energy_per_capita | Energy consumption per capita (kWh) |
| green_jobs_pct | % of workforce in green jobs |
| forest_area_pct | % of land covered by forest |
| recycling_rate | % of waste recycled |
| gdp_per_capita | GDP per capita (USD) |
| env_policy_score | Composite environmental policy strength score (0–100) |

> Note: built as a realistic, seeded synthetic dataset (ranges modeled on
> real-world reporting from sources like IEA / World Bank / IRENA) so the
> full pipeline — messy data, cleaning, EDA, clustering, evaluation — can be
> demonstrated end to end. Swap in a real CSV with the same column names to
> rerun on actual data.

## 2. Data Cleaning (`scripts/02_full_pipeline.py`)
- Removed 6 duplicate rows
- Treated impossible values as missing (CO2 > 30 t/capita, negative energy
  use, recycling rate > 100%, GDP > $150k) and imputed all missing values
  with the column **median** (robust to skew/outliers)
- Result: 180 clean rows, 0 missing values

## 3. Exploratory Analysis (seaborn)
- `01_correlation_heatmap.png` — renewable share and env. policy score are
  strongly positively correlated; CO2 per capita is negatively correlated
  with both
- `02_feature_distributions.png` — histograms + KDEs per feature
- `03_boxplots.png` — outlier check after cleaning

## 4. Clustering — K-Means
- Standardized all 8 features (`StandardScaler`)
- Tested k = 2–8 using **elbow method** (inertia) and **silhouette score**
  (`04_elbow_and_silhouette.png`)
- Silhouette alone peaks at k=2, but that only separates "green leaders"
  from everyone else. The elbow bends around **k=4**, and k=4 also produces
  4 clearly interpretable, policy-relevant groups — so k=4 was chosen as
  the final model instead of blindly maximizing silhouette.

## 5. Results — 4 Clusters Found

| Cluster | Label | Renewable % | CO2/capita | GDP/capita | Policy score |
|---|---|---|---|---|---|
| 0 | **Industrial High-Emission** | 17.8% | 12.1 t | $25,470 | 42.4 |
| 1 | **Green Leaders** | 70.1% | 4.1 t | $53,713 | 83.0 |
| 2 | **Resource-Constrained** | 22.3% | 1.5 t | $3,113 | 30.0 |
| 3 | **Emerging & Transitioning** | 31.9% | 5.6 t | $9,637 | 52.1 |

Visuals: `05_pca_clusters.png`, `06_pairplot_by_cluster.png`,
`07_cluster_profile_heatmap.png`

## 6. Evaluation
| Metric | Score | Interpretation |
|---|---|---|
| Silhouette Score | **0.450** | Reasonably well-separated, cohesive clusters |
| Davies-Bouldin Index | **0.848** | Lower is better; indicates good cluster separation |
| Recovery of known structure | 178/180 correct (98.9%) | Cross-check against the 4 latent archetypes used to generate the data |

## 7. How to Reproduce
```bash
pip install pandas seaborn matplotlib scikit-learn
python scripts/01_generate_dataset.py   # creates raw dataset
python scripts/02_full_pipeline.py      # cleans, analyzes, clusters, evaluates
```

## 8. Files
```
data/green_sustainability_raw.csv          raw (messy) dataset
data/green_sustainability_clustered.csv    cleaned dataset + cluster labels
data/cluster_profiles.csv                  mean feature values per cluster
data/cluster_vs_true_archetype.csv         validation cross-tab
plots/01–07_*.png                          all seaborn/matplotlib visuals
scripts/01_generate_dataset.py
scripts/02_full_pipeline.py
```
