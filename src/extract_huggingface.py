import requests
from schema import build_entity
from utils import clean_text, normalize_url

HF_API = "https://huggingface.co/api/models"

SEARCH_TERMS = ["text-generation", "image-generation", "speech-recognition", "translation", "object-detection", "text-classification", "question-answering", "summarization", "text-to-speech", "image-classification"]

def extract_huggingface_models():
    records = []
    seen_ids = set()

    for term in SEARCH_TERMS:
        params = {"search": term, "sort": "downloads", "direction": -1, "limit": 15}
        response = requests.get(HF_API, params=params, timeout=15)

        if response.status_code != 200:
            print(f"Hugging Face request failed for '{term}': {response.status_code}")
            continue

        items = response.json()

        for model in items:
            model_id = model.get("id") or model.get("modelId")
            if not model_id or model_id in seen_ids:
                continue
            seen_ids.add(model_id)

            url = normalize_url(f"https://huggingface.co/{model_id}")
            tags = model.get("tags", [])

            record = build_entity(
                entity_type="model",
                name=model_id,
                description=clean_text(f"Model tagged: {', '.join(tags[:6])}") if tags else "",
                url=url,
                categories=["Models"],
                source_name="Hugging Face",
                source_url=url,
                extra={
                    "provider": model_id.split("/")[0] if "/" in model_id else None,
                    "downloads": model.get("downloads", 0),
                },
            )
            records.append(record)

    return records


if __name__ == "__main__":
    results = extract_huggingface_models()
    print(f"Got {len(results)} records")
    if results:
        print(results[0])