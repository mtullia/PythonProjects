
import argparse
import os
import sys
import math
import warnings

import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

def pick_numeric_feature_columns(df: pd.DataFrame):
    # Use X*, Y*, Power* columns and any other numeric columns except clearly non-features
    candidates = []
    for col in df.columns:
        if col.lower() in {"qw"}:
            # keep qW too—it could be informative
            candidates.append(col)
            continue
        if col.lower() in {"total_power"}:
            candidates.append(col)
            continue
        if col.startswith(("X", "Y", "Power")):
            candidates.append(col)
    # If nothing matched, fallback to all numeric
    if not candidates:
        candidates = df.select_dtypes(include=[np.number]).columns.tolist()
    return candidates

def try_auto_k(X, k_min=2, k_max=8, random_state=42, n_init=10):
    best_k = None
    best_score = -1
    for k in range(k_min, k_max + 1):
        km = KMeans(n_clusters=k, random_state=random_state, n_init=n_init)
        labels = km.fit_predict(X)
        # Single cluster or noisy result check
        if len(set(labels)) < 2:
            continue
        score = silhouette_score(X, labels)
        if score > best_score:
            best_score = score
            best_k = k
    if best_k is None:
        # Fallback
        best_k = 4
    return best_k

def plot_clusters_2d(X2, labels, title, out_png):
    plt.figure()
    # Scatter plot without specifying colors (let matplotlib choose defaults)
    plt.scatter(X2[:, 0], X2[:, 1], s=6, c=labels)
    plt.title(title)
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.tight_layout()
    plt.savefig(out_png, dpi=160)
    plt.close()

def process_file(path, args):
    base = os.path.splitext(os.path.basename(path))[0]
    print(f"\n=== Processing: {base} ===")
    df = pd.read_csv(path)
    feature_cols = pick_numeric_feature_columns(df)

    # Drop rows with all-NaN in selected features; fill remaining NaNs with column medians
    X = df[feature_cols].copy()
    X = X.dropna(how="all")
    X = X.fillna(X.median(numeric_only=True))

    # Optional sampling for speed
    if args.sample and len(X) > args.sample:
        X = X.sample(n=args.sample, random_state=42)

    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # PCA for clustering and 2D visualization
    pca_k = args.pca_components
    pca = PCA(n_components=pca_k, random_state=42)
    X_pca = pca.fit_transform(X_scaled)

    # 2D for plotting
    pca2 = PCA(n_components=2, random_state=42)
    X_2d = pca2.fit_transform(X_scaled)

    # --- K-MEANS ---
    if args.kmeans_k == "auto":
        k = try_auto_k(X_pca, k_min=args.kmeans_k_min, k_max=args.kmeans_k_max)
    else:
        k = int(args.kmeans_k)

    kmeans = KMeans(n_clusters=k, random_state=42, n_init=args.kmeans_n_init)
    km_labels = kmeans.fit_predict(X_pca)

    # --- DBSCAN ---
    dbscan = DBSCAN(eps=args.dbscan_eps, min_samples=args.dbscan_min_samples, n_jobs=-1)
    db_labels = dbscan.fit_predict(X_pca)

    # Assemble results
    result = X.copy()
    result["pc1"] = X_2d[:, 0]
    result["pc2"] = X_2d[:, 1]
    result["kmeans_label"] = km_labels
    result["dbscan_label"] = db_labels

    # Save CSV
    out_csv = os.path.join(args.out_dir, f"{base}_clustered.csv")
    os.makedirs(args.out_dir, exist_ok=True)
    result.to_csv(out_csv, index=False)
    print(f"Saved clustered CSV -> {out_csv}")

    # Save plots
    plot_clusters_2d(X_2d, km_labels, f"{base} - KMeans (k={k})", os.path.join(args.out_dir, f"{base}_kmeans.png"))
    plot_clusters_2d(X_2d, db_labels, f"{base} - DBSCAN (eps={args.dbscan_eps}, min_samples={args.dbscan_min_samples})", os.path.join(args.out_dir, f"{base}_dbscan.png"))
    print(f"Saved scatter plots -> {args.out_dir}/{base}_kmeans.png and {args.out_dir}/{base}_dbscan.png")

def main():
    parser = argparse.ArgumentParser(description="Clustering pipeline: K-Means and DBSCAN on combined coordinate+power features.")
    parser.add_argument("--files", nargs="+", required=True, help="CSV files to cluster.")
    parser.add_argument("--out_dir", default="cluster_outputs", help="Directory to write outputs.")
    parser.add_argument("--sample", type=int, default=10000, help="Optional row cap per file for speed (0 disables sampling).")
    parser.add_argument("--pca_components", type=int, default=10, help="Number of PCA components used for clustering.")
    parser.add_argument("--kmeans_k", default="auto", help='K for K-Means (integer) or "auto" to choose via silhouette.')
    parser.add_argument("--kmeans_k_min", type=int, default=2, help="Minimum k when using auto.")
    parser.add_argument("--kmeans_k_max", type=int, default=8, help="Maximum k when using auto.")
    parser.add_argument("--kmeans_n_init", type=int, default=10, help="KMeans n_init.")
    parser.add_argument("--dbscan_eps", type=float, default=2.0, help="DBSCAN eps (on PCA space).")
    parser.add_argument("--dbscan_min_samples", type=int, default=10, help="DBSCAN min_samples.")

    args = parser.parse_args()

    for f in args.files:
        if not os.path.exists(f):
            print(f"File not found: {f}", file=sys.stderr)
            continue
        try:
            process_file(f, args)
        except Exception as e:
            print(f"Error processing {f}: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
