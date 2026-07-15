"""
Green Skills & Sustainability - K-Means Clustering Pipeline
============================================================
Steps:
 1. Load raw data
 2. Clean (missing values, duplicates, invalid outliers)
 3. EDA with seaborn (distributions, correlation heatmap, boxplots)
 4. Preprocess (scale features)
 5. Choose k (elbow method + silhouette score)
 6. Fit final K-Means
 7. Evaluate (silhouette, Davies-Bouldin, cluster profiles)
 8. Visualize clusters (PCA 2D + seaborn pairplot by cluster)
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.decomposition import PCA

sns.set_theme(style="whitegrid", palette="viridis")
DATA = "/home/claude/project/data/green_sustainability_raw.csv"
PLOTS = "/home/claude/project/plots"
OUT_CSV = "/home/claude/project/data/green_sustainability_clustered.csv"

FEATURES = [
    "renewable_share", "co2_per_capita", "energy_per_capita", "green_jobs_pct",
    "forest_area_pct", "recycling_rate", "gdp_per_capita", "env_policy_score",
]

# ---------------------------------------------------------------------------
# 1. LOAD
# ---------------------------------------------------------------------------
df = pd.read_csv(DATA)
print("Raw shape:", df.shape)
print("Missing values per column:\n", df.isna().sum())
print("Duplicate rows (excluding true_group label):",
      df.drop(columns=["true_group"]).duplicated().sum())

# ---------------------------------------------------------------------------
# 2. CLEAN
# ---------------------------------------------------------------------------
df_clean = df.drop_duplicates(subset=["country"]).copy()

# Fix invalid/impossible values -> treat as missing, then impute
df_clean.loc[df_clean["co2_per_capita"] > 30, "co2_per_capita"] = np.nan
df_clean.loc[df_clean["energy_per_capita"] < 0, "energy_per_capita"] = np.nan
df_clean.loc[df_clean["recycling_rate"] > 100, "recycling_rate"] = np.nan
df_clean.loc[df_clean["gdp_per_capita"] > 150000, "gdp_per_capita"] = np.nan

# Impute remaining missing values with the median (robust to skew/outliers)
for col in FEATURES:
    df_clean[col] = df_clean[col].fillna(df_clean[col].median())

print("\nCleaned shape:", df_clean.shape)
print("Missing values after cleaning:", df_clean[FEATURES].isna().sum().sum())

# ---------------------------------------------------------------------------
# 3. EDA (seaborn)
# ---------------------------------------------------------------------------
# 3a. Correlation heatmap
plt.figure(figsize=(9, 7))
corr = df_clean[FEATURES].corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, square=True)
plt.title("Correlation Between Sustainability Indicators")
plt.tight_layout()
plt.savefig(f"{PLOTS}/01_correlation_heatmap.png", dpi=150)
plt.close()

# 3b. Distributions
fig, axes = plt.subplots(2, 4, figsize=(18, 8))
for ax, col in zip(axes.flat, FEATURES):
    sns.histplot(df_clean[col], kde=True, ax=ax, color="seagreen")
    ax.set_title(col)
plt.suptitle("Feature Distributions (post-cleaning)")
plt.tight_layout()
plt.savefig(f"{PLOTS}/02_feature_distributions.png", dpi=150)
plt.close()

# 3c. Boxplots to check remaining outliers
fig, axes = plt.subplots(2, 4, figsize=(18, 8))
for ax, col in zip(axes.flat, FEATURES):
    sns.boxplot(y=df_clean[col], ax=ax, color="lightgreen")
    ax.set_title(col)
plt.suptitle("Outlier Check (post-cleaning)")
plt.tight_layout()
plt.savefig(f"{PLOTS}/03_boxplots.png", dpi=150)
plt.close()

# ---------------------------------------------------------------------------
# 4. PREPROCESS
# ---------------------------------------------------------------------------
X = df_clean[FEATURES].values
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ---------------------------------------------------------------------------
# 5. CHOOSE K -- elbow method + silhouette score
# ---------------------------------------------------------------------------
k_range = range(2, 9)
inertias = []
sil_scores = []
for k in k_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)
    inertias.append(km.inertia_)
    sil_scores.append(silhouette_score(X_scaled, labels))

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
axes[0].plot(list(k_range), inertias, marker="o", color="seagreen")
axes[0].set_xlabel("Number of clusters (k)")
axes[0].set_ylabel("Inertia (within-cluster SS)")
axes[0].set_title("Elbow Method")

axes[1].plot(list(k_range), sil_scores, marker="o", color="darkgreen")
axes[1].set_xlabel("Number of clusters (k)")
axes[1].set_ylabel("Silhouette Score")
axes[1].set_title("Silhouette Score by k")
plt.tight_layout()
plt.savefig(f"{PLOTS}/04_elbow_and_silhouette.png", dpi=150)
plt.close()

best_silhouette_k = list(k_range)[int(np.argmax(sil_scores))]
print(f"\nSilhouette scores by k: {dict(zip(k_range, np.round(sil_scores, 3)))}")
print(f"k with single highest silhouette score: {best_silhouette_k}")

# NOTE ON MODEL SELECTION:
# The silhouette score alone peaks at k=2, but that just separates
# "green leaders" from everyone else and hides real differences between
# industrial high-emission, emerging/transitioning, and resource-constrained
# countries -- a distinction that matters a lot for a green-skills/policy
# use case. The elbow plot also shows a clear bend around k=4. So we select
# k=4 as the final, more actionable choice, and report both metrics for
# transparency rather than blindly taking the silhouette-maximizing k.
best_k = 4
print(f"Chosen k for final model (elbow + domain interpretability): {best_k}")

# ---------------------------------------------------------------------------
# 6. FINAL MODEL
# ---------------------------------------------------------------------------
final_km = KMeans(n_clusters=best_k, random_state=42, n_init=10)
df_clean["cluster"] = final_km.fit_predict(X_scaled)

# ---------------------------------------------------------------------------
# 7. EVALUATE
# ---------------------------------------------------------------------------
sil = silhouette_score(X_scaled, df_clean["cluster"])
db = davies_bouldin_score(X_scaled, df_clean["cluster"])
print(f"\nFinal model (k={best_k}) evaluation:")
print(f"  Silhouette Score:     {sil:.3f}  (higher is better, max 1.0)")
print(f"  Davies-Bouldin Index: {db:.3f}  (lower is better)")

cluster_profile = df_clean.groupby("cluster")[FEATURES].mean().round(2)
cluster_sizes = df_clean["cluster"].value_counts().sort_index()
print("\nCluster sizes:\n", cluster_sizes)
print("\nCluster profiles (feature means):\n", cluster_profile)

# Cross-check against the known ground-truth archetype (since this is
# synthetic data) -- purely for our own validation, not used by the model.
crosstab = pd.crosstab(df_clean["true_group"], df_clean["cluster"])
print("\nCross-tab: true archetype vs. discovered cluster:\n", crosstab)

cluster_profile.to_csv("/home/claude/project/data/cluster_profiles.csv")
crosstab.to_csv("/home/claude/project/data/cluster_vs_true_archetype.csv")

# ---------------------------------------------------------------------------
# 8. VISUALIZE CLUSTERS
# ---------------------------------------------------------------------------
pca = PCA(n_components=2, random_state=42)
coords = pca.fit_transform(X_scaled)
df_clean["pca1"] = coords[:, 0]
df_clean["pca2"] = coords[:, 1]

plt.figure(figsize=(9, 7))
sns.scatterplot(
    data=df_clean, x="pca1", y="pca2", hue="cluster", palette="Set2",
    s=70, alpha=0.85,
)
plt.title(f"K-Means Clusters (k={best_k}) — PCA-Reduced View")
plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% var)")
plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% var)")
plt.tight_layout()
plt.savefig(f"{PLOTS}/05_pca_clusters.png", dpi=150)
plt.close()

# Pairplot on a few key features colored by cluster
key_feats = ["renewable_share", "co2_per_capita", "gdp_per_capita", "env_policy_score"]
pp = sns.pairplot(df_clean, vars=key_feats, hue="cluster", palette="Set2", diag_kind="kde")
pp.fig.suptitle("Key Features by Cluster", y=1.02)
pp.savefig(f"{PLOTS}/06_pairplot_by_cluster.png", dpi=150)
plt.close()

# Cluster profile heatmap (standardized means) for interpretation
plt.figure(figsize=(9, 5))
profile_z = (cluster_profile - cluster_profile.mean()) / cluster_profile.std()
sns.heatmap(profile_z, annot=cluster_profile, fmt=".1f", cmap="RdYlGn", center=0)
plt.title("Cluster Profiles (color = relative level, numbers = actual mean)")
plt.tight_layout()
plt.savefig(f"{PLOTS}/07_cluster_profile_heatmap.png", dpi=150)
plt.close()

df_clean.to_csv(OUT_CSV, index=False)
print(f"\nSaved cleaned + clustered dataset to: {OUT_CSV}")
print("All plots saved to:", PLOTS)
