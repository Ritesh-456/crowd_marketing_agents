import json
from tools.apify_scraper import scrape_website
from agents.research_agent import research_company
from agents.competitor_agent import competitor_analysis
from agents.reddit_agent import fetch_reddit_posts, extract_pain_and_reply


def main():
    url = "https://www.crowdwisdomtrading.com/"

    print("\n🚀 Step 1: Scraping Website...\n")
    data = scrape_website(url)

    print("\n🚀 Step 2: Research Agent...\n")
    summary = research_company(data)

    print("\n========== PRODUCT SUMMARY ==========\n")
    print(summary)

    print("\n🚀 Step 3: Competitor Agent...\n")
    competitor_result = competitor_analysis(summary, data)

    print("\n========== COMPETITOR ANALYSIS ==========\n")
    print(competitor_result)

    # ✅ Reddit Step (MUST be inside main)
    print("\n🚀 Step 4: Reddit Pain Agent...\n")

    posts = fetch_reddit_posts()
    reddit_results = extract_pain_and_reply(posts)

    print("\n========== REDDIT RESPONSES ==========\n")

    for r in reddit_results:
        print("\nPost:", r["post"])
        print("Link:", r["link"])
        print("Reply:", r["reply"])
        print("-" * 50)

    # ✅ Save output AFTER everything is ready
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump({
            "summary": summary,
            "competitors": competitor_result,
            "reddit": reddit_results
        }, f, indent=4)


if __name__ == "__main__":
    main()