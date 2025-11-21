import json
import matplotlib.pyplot as plt
import pandas as pd
import argparse

def visualize_media_bias(data_file, output_map):

    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
            sources = data.get("sources", [])
    except FileNotFoundError:
        print(f"Error: Bias data file '{data_file}' not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{data_file}'.")
        return
    
    if not sources:
        print("Error: No source data found in the file.")
        return

    df = pd.DataFrame(sources)
    df = df[['journal_name', 'simulated_bias_score']]
    df['simulated_bias_score'] = pd.to_numeric(df['simulated_bias_score'])

    # Setup Visualization - Slightly smaller, cleaner canvas
    fig, ax = plt.subplots(figsize=(10, 6))

    # --- Plotting the Bias Scores ---
    
    y_pos = range(len(df))
    
    # Define Color mapping for points (kept for clarity)
    def get_color(score):
        if score > 5.0:
            return 'firebrick' # Strong Right (darker red)
        elif score > 1.0:
            return 'lightcoral' # Lean Right
        elif score < -5.0:
            return 'midnightblue' # Strong Left (darker blue)
        elif score < -1.0:
            return 'skyblue' # Lean Left
        else:
            return 'darkgray' # Center
            
    colors = df['simulated_bias_score'].apply(get_color)
    
    # Plot the source dots: decreased size to 100 (from 150)
    ax.scatter(df['simulated_bias_score'], y_pos, c=colors, s=100, zorder=3)

    # 1. Zero Line (Center/Neutral)
    ax.axvline(0, color='black', linestyle='-', linewidth=1, zorder=1)

    # 3. Text Labels for Regions (Simplified positioning and appearance)
    ax.text(-9.5, len(df), 'FAR LEFT', color='midnightblue', fontsize=10, weight='bold', ha='left')
    ax.text(9.5, len(df), 'FAR RIGHT', color='firebrick', fontsize=10, weight='bold', ha='right')
    ax.text(0, len(df), 'CENTER', color='black', fontsize=10, weight='bold', ha='center')

    # 4. Label the individual data points (sources)
    for i, row in df.iterrows():
        align = 'right'
        x_offset = -0.2 if row['simulated_bias_score'] < 0 else 0.2
                
        # Annotate with journal name
        ax.annotate(row['journal_name'], 
                    (row['simulated_bias_score'] + x_offset, y_pos[i]),
                    ha=align, va='center', fontsize=9, clip_on=True)
        
        # Annotate with score value (placed directly over/under the dot)
        ax.annotate(f"{row['simulated_bias_score']:.1f}", 
                    (row['simulated_bias_score'], y_pos[i] - 0.2), # Adjusted vertical position
                    ha='center', va='top', fontsize=7, color='black')
    
    # --- Final Axis and Title Setup ---
    
    ax.set_yticks([])  
    ax.set_yticklabels([])
    
    ax.set_xlabel("Media Bias Score (Left: -10 | Center: 0 | Right: +10)", fontsize=10)
    ax.set_title("Media Bias Map of Mamdani Coverage Sources", fontsize=12, weight='bold')
    
    ax.set_xlim(-10, 10)
    ax.set_ylim(-1, len(df) + 1)
    
    ax.grid(axis='y', visible=False)
    ax.grid(axis='x', linestyle=':', alpha=0.4)
    ax.tick_params(axis='x', which='both', bottom=True, top=False, labelbottom=True)
    
    plt.tight_layout()
    
    plt.savefig(output_map)
    
    print(f"Visualization saved successfully as {output_map}")
    
def main():
    parser = argparse.ArgumentParser(description="Filter news articles")

    parser.add_argument("--input", type=str, required=True,
                        help="media bias")
    parser.add_argument("--output", type=str, required=True,
                        help="map")

    args = parser.parse_args()
    visualize_media_bias(args.input, args.output)
    

if __name__ == "__main__":
    main()