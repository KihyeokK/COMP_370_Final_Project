import json
import argparse
import matplotlib.pyplot as plt

LEFT_MAX = -3.0
RIGHT_MIN = 3.0

def get_bias_category(score):
    if score <= LEFT_MAX:
        return "Left"
    if score >= RIGHT_MIN:
        return "Right"
    return "Center"

def generate_bias_pie_chart(articles_file, bias_file, output):
    with open(articles_file, "r") as f:
        articles = json.load(f)["articles"]

    with open(bias_file, "r") as f:
        sources = json.load(f)["sources"]

    source_scores = {s["journal_name"]: s["simulated_bias_score"] for s in sources}

    id_to_name = {
        "the-new-york-times": "The New York Times",
        "ca-national-news": "CBC News",
        "the-seattle-times": "The Seattle Times",
        "the-wall-street-journal": "The Wall Street Journal",
        "los-angeles-times": "Los Angeles Times",
        "new-york-magazine": "New York Magazine",
        "nypost": "New York Post",
        "business-insider": "Business Insider",
        "usa-today": "USA Today",
        "nbc-news": "NBC News",
        "the-atlantic": "The Atlantic",
        "gothamist": "Gothamist",
        "abc-news": "ABC News",
        "fox-news": "Fox News",
        "nydailynews": "NY Daily News",
        "pagesix": "Page Six"
    }

    counts = {}
    for a in articles:
        src = id_to_name.get(a["id"], a["id"])
        counts[src] = counts.get(src, 0) + 1

    distribution = {"Left": 0, "Center": 0, "Right": 0}

    for src, count in counts.items():
        score = source_scores.get(src)
        if score is not None:
            category = get_bias_category(score)
            distribution[category] += count

    labels = [k for k, v in distribution.items() if v > 0]
    sizes = [v for v in distribution.values() if v > 0]

    colors = {
        "Left": "blue",
        "Center": "gray",
        "Right": "red"
    }
    plot_colors = [colors[l] for l in labels]

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(
        sizes,
        labels=labels,
        autopct=lambda p: f"{p:.1f}%\n({int(p * sum(sizes) / 100)} articles)",
        startangle=90,
        colors=plot_colors
    )
    ax.axis("equal")
    ax.set_title(f"Mamdani Coverage by Media Bias ({sum(sizes)} Articles)", fontsize=14)

    plt.tight_layout()
    plt.savefig(output)
    print(f"Saved: {output}")


def main():
    parser = argparse.ArgumentParser(description="Generate media bias distribution pie chart")
    parser.add_argument("--articles_file", type=str, required=True)
    parser.add_argument("--bias_file", type=str, required=True)
    parser.add_argument("--output", type=str, default="media_bias_distribution.png")
    args = parser.parse_args()
    generate_bias_pie_chart(args.articles_file, args.bias_file, args.output)

if __name__ == "__main__":
    main()
