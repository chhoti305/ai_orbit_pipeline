"""
Hand-curated entities for categories with no free, reliable public API —
same justification as companies.py already in this repo. Each entry is a
real, verifiable product; researched and entered manually.
"""
from schema import build_entity


def get_curated_entities():
    records = []

    robots = [
        {"name": "Figure 02", "desc": "General-purpose humanoid robot for industrial tasks", "url": "https://www.figure.ai/"},
        {"name": "Optimus", "desc": "Tesla's humanoid robot platform", "url": "https://www.tesla.com/AI"},
        {"name": "Atlas", "desc": "Boston Dynamics' electric humanoid robot", "url": "https://bostondynamics.com/atlas/"},
        {"name": "Spot", "desc": "Boston Dynamics' quadruped robot for inspection tasks", "url": "https://bostondynamics.com/products/spot/"},
        {"name": "Unitree G1", "desc": "Compact humanoid robot platform", "url": "https://www.unitree.com/g1"},
    ]
    for r in robots:
        records.append(build_entity(
            entity_type="robot", name=r["name"], description=r["desc"], url=r["url"],
            categories=["Robots"], source_name="Manual Research", source_url=r["url"],
        ))

    devices = [
        {"name": "Humane AI Pin", "desc": "Wearable AI device with projected display", "url": "https://humane.com/"},
        {"name": "Rabbit R1", "desc": "Pocket AI assistant device", "url": "https://www.rabbit.tech/"},
        {"name": "NVIDIA Jetson Orin", "desc": "Edge AI hardware module for robotics and vision", "url": "https://developer.nvidia.com/embedded/jetson-orin"},
        {"name": "Meta Ray-Ban Display", "desc": "Smart glasses with built-in AI assistant", "url": "https://www.meta.com/ai-glasses/"},
    ]
    for d in devices:
        records.append(build_entity(
            entity_type="device", name=d["name"], description=d["desc"], url=d["url"],
            categories=["Devices"], source_name="Manual Research", source_url=d["url"],
        ))

    personal = [
        {"name": "ChatGPT", "desc": "General-purpose personal AI assistant", "url": "https://chatgpt.com/"},
        {"name": "Claude", "desc": "Personal AI assistant by Anthropic", "url": "https://claude.ai/"},
        {"name": "Google Gemini", "desc": "Personal AI assistant integrated with Google services", "url": "https://gemini.google.com/"},
        {"name": "Perplexity", "desc": "AI-powered personal research and search assistant", "url": "https://www.perplexity.ai/"},
    ]
    for p in personal:
        records.append(build_entity(
            entity_type="personal", name=p["name"], description=p["desc"], url=p["url"],
            categories=["Personal"], source_name="Manual Research", source_url=p["url"],
        ))

    creative = [
        {"name": "Midjourney", "desc": "AI image generation for creative and artistic work", "url": "https://www.midjourney.com/"},
        {"name": "Runway", "desc": "AI video generation and editing platform", "url": "https://runwayml.com/"},
        {"name": "Suno", "desc": "AI music generation tool", "url": "https://suno.com/"},
        {"name": "ElevenLabs", "desc": "AI voice generation and cloning platform", "url": "https://elevenlabs.io/"},
    ]
    for c in creative:
        records.append(build_entity(
            entity_type="creative", name=c["name"], description=c["desc"], url=c["url"],
            categories=["Creative"], source_name="Manual Research", source_url=c["url"],
        ))

    return records


if __name__ == "__main__":
    results = get_curated_entities()
    print(f"Got {len(results)} curated records")