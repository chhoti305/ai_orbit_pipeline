from schema import build_entity

COMPANIES_DATA = [
    {"name": "OpenAI", "description": "Creator of ChatGPT and GPT models.", "url": "https://openai.com", "founded": 2015, "hq": "San Francisco, USA"},
    {"name": "Anthropic", "description": "AI safety company that builds Claude.", "url": "https://anthropic.com", "founded": 2021, "hq": "San Francisco, USA"},
    {"name": "Google DeepMind", "description": "Google's AI research lab, creator of Gemini.", "url": "https://deepmind.google", "founded": 2010, "hq": "London, UK"},
    {"name": "Meta AI", "description": "Meta's AI research division, creator of Llama models.", "url": "https://ai.meta.com", "founded": 2013, "hq": "Menlo Park, USA"},
    {"name": "Hugging Face", "description": "Open platform for sharing AI models and datasets.", "url": "https://huggingface.co", "founded": 2016, "hq": "New York, USA"},
    {"name": "Stability AI", "description": "Maker of Stable Diffusion image generation models.", "url": "https://stability.ai", "founded": 2019, "hq": "London, UK"},
    {"name": "Mistral AI", "description": "French AI lab building open-weight language models.", "url": "https://mistral.ai", "founded": 2023, "hq": "Paris, France"},
    {"name": "Cohere", "description": "Enterprise-focused large language model company.", "url": "https://cohere.com", "founded": 2019, "hq": "Toronto, Canada"},
    {"name": "xAI", "description": "Elon Musk's AI company, creator of Grok.", "url": "https://x.ai", "founded": 2023, "hq": "San Francisco, USA"},
    {"name": "Perplexity AI", "description": "AI-powered answer engine and search assistant.", "url": "https://perplexity.ai", "founded": 2022, "hq": "San Francisco, USA"},
]


def get_companies():
    records = []
    for c in COMPANIES_DATA:
        record = build_entity(
            entity_type="company",
            name=c["name"],
            description=c["description"],
            url=c["url"],
            categories=["Companies"],
            source_name="Curated List",
            source_url=c["url"],
            extra={
                "founded_year": c["founded"],
                "headquarters": c["hq"],
            },
        )
        records.append(record)
    return records