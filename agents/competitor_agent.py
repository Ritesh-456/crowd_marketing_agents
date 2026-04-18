from tools.openrouter_llm import call_llm
from tools.logger import log_info, log_error


def competitor_analysis(product_summary, scraped_data):
    log_info("Competitor agent started")

    content = ""
    for item in scraped_data:
        content += item.get("text", "") + "\n"

    content = content[:4000]

    prompt = f"""
Extract competitors and compare.

Product:
{product_summary}

Content:
{content}
"""

    try:
        response = call_llm(prompt)
        log_info("Competitor analysis completed")
        return response

    except Exception as e:
        log_error(f"Competitor agent error: {str(e)}")
        return "❌ Competitor analysis failed"