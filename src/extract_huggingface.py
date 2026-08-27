import requests
from schema import build_entity
from utils import clean_text, normalize_url

HF_API = "https://huggingface.co/api/models"

SEARCH_TERMS = ["text-generation", "image-generation", "speech-recognition", "translation", "object-detection", "text-classification", "question-answering", "summarization", "text-to-speech", "image-classification"]

# Human-readable labels for HF pipeline_tag values -> Task entities.
# Keeps the Task description useful instead of just echoing the raw tag.
TASK_DESCRIPTIONS = {
    "text-generation": "Generate coherent text from a prompt",
    "image-generation": "Create images from text or other inputs",
    "speech-recognition": "Convert spoken audio into text",
    "translation": "Translate text between languages",
    "object-detection": "Detect and localize objects in images",
    "text-classification": "Assign labels or categories to text",
    "question-answering": "Answer questions given context or documents",
    "summarization": "Condense long text into a shorter summary",
    "text-to-speech": "Convert text into spoken audio",
    "image-classification": "Assign labels or categories to images",
}


def extract_huggingface_models():
    """
    Returns a combined list of records:
      - entity_type "model"  (one per unique HF model)
      - entity_type "task"   (one per unique pipeline_tag seen, deduped)
    Keeping both in one list matches the existing run.py pattern of
    aggregating whatever each extractor returns into the master dataset.
    """
    records = []
    seen_model_ids = set()
    seen_task_tags = set()

    for term in SEARCH_TERMS:
        params = {"search": term, "sort": "downloads", "direction": -1, "limit": 15}
        response = requests.get(HF_API, params=params, timeout=15)

        if response.status_code != 200:
            print(f"Hugging Face request failed for '{term}': {response.status_code}")
            continue

        items = response.json()

        for model in items:
            model_id = model.get("id") or model.get("modelId")
            if not model_id or model_id in seen_model_ids:
                continue
            seen_model_ids.add(model_id)

            url = normalize_url(f"https://huggingface.co/{model_id}")
            tags = model.get("tags", [])
            pipeline_tag = model.get("pipeline_tag")

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
                    "pipeline_tag": pipeline_tag,
                    "last_modified": model.get("lastModified"),  # used later to tag "new"
                },
            )
            records.append(record)

            # Derive a Task entity from pipeline_tag, once per unique tag.
            if pipeline_tag and pipeline_tag not in seen_task_tags:
                seen_task_tags.add(pipeline_tag)
                task_url = normalize_url(f"https://huggingface.co/models?pipeline_tag={pipeline_tag}")
                task_record = build_entity(
                    entity_type="task",
                    name=pipeline_tag.replace("-", " ").title(),
                    description=TASK_DESCRIPTIONS.get(pipeline_tag, f"AI task: {pipeline_tag}"),
                    url=task_url,
                    categories=["Tasks"],
                    source_name="Hugging Face",
                    source_url=task_url,
                    extra={"pipeline_tag": pipeline_tag},
                )
                records.append(task_record)

    return records


if __name__ == "__main__":
    results = extract_huggingface_models()
    models = [r for r in results if r["entity_type"] == "model"]
    tasks = [r for r in results if r["entity_type"] == "task"]
    print(f"Got {len(models)} models, {len(tasks)} tasks")
    if results:
        print(results[0])