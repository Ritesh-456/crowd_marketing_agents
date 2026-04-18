from tools.openrouter_llm import call_llm


def research_company(scraped_data):
    print("\n[Research Agent] Step 2: Extracting content...\n")

    if not scraped_data:
        return "❌ No data found from website."

    content = ""
    for item in scraped_data:
        content += item.get("text", "") + "\n"

    content = content[:4000]

    print("[Research Agent] Step 3: Sending to LLM...\n")

    prompt = f"""
You are a market research analyst.

Analyze the website content below and provide:

1. What the product does
2. Who are the target users
3. Key features

Website Content:
{content}
"""

    return call_llm(prompt)