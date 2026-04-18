from apify_client import ApifyClient
import os
from dotenv import load_dotenv
from tools.logger import log_info, log_error

load_dotenv()

APIFY_TOKEN = os.getenv("APIFY_API_TOKEN")


def scrape_website(url):
    log_info("Starting website scraping")

    client = ApifyClient(APIFY_TOKEN)

    try:
        run = client.actor("apify/website-content-crawler").call(
            run_input={
                "startUrls": [{"url": url}],
                "maxCrawlDepth": 1,
                "maxPagesPerCrawl": 5
            }
        )

        items = client.dataset(run["defaultDatasetId"]).list_items().items

        log_info("Scraping completed successfully")
        return items

    except Exception as e:
        log_error(f"Scraping error: {str(e)}")
        return []