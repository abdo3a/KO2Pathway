#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import argparse
import os
from time import sleep

# ------------------------
# Functions
# ------------------------

def preprocess_input(input_file):
    df = pd.read_csv(input_file, sep='\t', header=None, names=['gene', 'ko_raw'])
    # Remove missing or '-' entries
    df = df[df['ko_raw'].notna() & (df['ko_raw'] != "-")]
    # Split comma-separated KO entries into multiple rows
    df = df.assign(ko=df['ko_raw'].str.split(',')).explode('ko')
    # Remove "ko:" prefix
    df['ko'] = df['ko'].str.replace('ko:', '', regex=False)
    # Drop empty or invalid KO entries
    df = df[df['ko'].str.match(r'^K\d{5}$', na=False)]
    df = df.drop(columns=['ko_raw'])
    return df

def fetch_ko_pathway_mapping(ko_list, cache_file=None):
    if cache_file and os.path.exists(cache_file):
        print(f"✅ Loading cached KO-pathway mapping from {cache_file}")
        mapping_df = pd.read_csv(cache_file, sep='\t')
    else:
        print("🔎 Fetching KO-pathway mapping from KEGG API...")
        records = []
        for ko in ko_list:
            url = f"https://rest.kegg.jp/link/pathway/ko:{ko}"
            r = requests.get(url)
            if r.status_code == 200 and r.text.strip():
                for line in r.text.strip().split("\n"):
                    parts = line.split("\t")
                    if len(parts) == 2:
                        pw = parts[1].replace("path:", "")
                        if pw.startswith("map"):
                            records.append({"ko": ko, "pathway_id": pw})
            sleep(0.2)
        mapping_df = pd.DataFrame(records)
        if cache_file:
            mapping_df.to_csv(cache_file, sep='\t', index=False)
            print(f"💾 Saved KO-pathway mapping to {cache_file}")
    return mapping_df

def fetch_pathway_descriptions(pathway_ids):
    desc_map = {}
    for pw in pathway_ids:
        url = f"https://rest.kegg.jp/list/{pw}"
        r = requests.get(url)
        if r.status_code == 200 and r.text.strip():
            desc = r.text.strip().split("\t")[1]
            desc_map[pw] = desc
        else:
            desc_map[pw] = "Unknown"
        sleep(0.2)
    return desc_map

def plot_circular_barplot(df, output_plot):
    labels = df['pathway_description'].tolist()
    counts = df['KO_count'].to_numpy()
    
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    counts = np.concatenate((counts, [counts[0]]))
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(polar=True))

    bars = ax.bar(angles, counts, width=0.25, facecolor='skyblue', edgecolor='black', linewidth=1.0, alpha=1.0)

    max_count = counts.max()
    ax.set_ylim(0, max_count)

    for angle_val, height in zip(angles[:-1], counts[:-1]):
        ax.plot([angle_val, angle_val], [height, max_count], color='gray', linestyle='--', linewidth=0.8, alpha=0.7)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=10)

    for label, angle in zip(ax.get_xticklabels(), angles[:-1]):
        rotation = np.degrees(angle)
        if angle >= np.pi/2 and angle <= 3*np.pi/2:
            label.set_rotation(rotation + 180)
            label.set_verticalalignment('center')
        else:
            label.set_rotation(rotation)
            label.set_verticalalignment('center')
        label.set_horizontalalignment('center')

    step = int(np.ceil(max_count / 5))
    yticks = np.arange(0, max_count + step, step)
    ax.set_yticks(yticks)
    ax.set_yticklabels([f'{int(t)}' for t in yticks], fontsize=8)

    ax.yaxis.grid(True, color='lightgray', linestyle='dashed', linewidth=0.7)
    ax.xaxis.grid(False)
    ax.spines['polar'].set_visible(False)

    plt.tight_layout()
    if output_plot:
        plt.savefig(output_plot, format='svg', dpi=300, bbox_inches='tight')
        print(f"📈 Plot saved to {output_plot}")
    plt.show()
    plt.close()

# ------------------------
# Main
# ------------------------

def main():
    parser = argparse.ArgumentParser(
        description="KO2Pathway: Map KEGG Orthology (KO) terms to pathways, filter, summarize, and plot."
    )
    parser.add_argument("-i", "--input", required=True, help="Input file (genes and KOs)")
    parser.add_argument("-e", "--exclude", default=None, help="Optional file listing terms to exclude (one per line)")
    parser.add_argument("-c", "--cache", default="kegg_ko_pathway_map.tsv", help="Cache file for KO-pathway mappings")
    parser.add_argument("-p", "--plot", action="store_true", help="Enable circular bar plot output")
    parser.add_argument("-o", "--output", default="kegg_pathway_summary.tsv", help="Output summary TSV")
    parser.add_argument("--plotfile", default="top20_pathways_circular_barplot.svg", help="Output plot file name")

    args = parser.parse_args()

    # Step 1: Preprocess input
    ko_df = preprocess_input(args.input)

    # Step 2: Fetch/load KO-pathway mapping
    ko_list = ko_df['ko'].unique()
    pathway_df = fetch_ko_pathway_mapping(ko_list, cache_file=args.cache)

    # Step 3: Fetch pathway descriptions
    unique_pathways = pathway_df["pathway_id"].unique()
    pathway_desc_map = fetch_pathway_descriptions(unique_pathways)
    pathway_df["pathway_description"] = pathway_df["pathway_id"].map(pathway_desc_map)

    # Step 4: Summarize
    summary_df = (
        pathway_df.groupby(["pathway_id", "pathway_description"])
        .size()
        .reset_index(name="KO_count")
    )

    # Step 5: Filtering
    if args.exclude:
        with open(args.exclude, "r") as f:
            exclude_terms = [line.strip().lower() for line in f if line.strip()]
        pattern = '|'.join(exclude_terms)
        summary_df = summary_df[~summary_df['pathway_description'].str.lower().str.contains(pattern)]

    summary_df = summary_df.drop_duplicates(subset='pathway_description', keep='first')
    summary_df = summary_df.sort_values(by="KO_count", ascending=False)

    # Step 6: Save output
    summary_df.to_csv(args.output, sep='\t', index=False)
    print(f"✅ Summary saved to {args.output}")

    # Step 7: Plot if requested
    if args.plot:
        top20_df = summary_df.head(20)
        plot_circular_barplot(top20_df, args.plotfile)

if __name__ == "__main__":
    main()
