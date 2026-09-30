import os
import json

from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_outline(
    story_prompt: str,
    character_name: str,
    setting: str,
    tone: str,
    art_style: str
):
    prompt = f"""
Create a 5-panel comic outline.

Story: {story_prompt}
Character: {character_name}
Setting: {setting}
Tone: {tone}
Art style: {art_style}

Return ONLY JSON.

Format:
{{
  "panels": [
    {{
      "panel_number": 1,
      "title": "title",
      "scene_description": "short scene",
      "image_prompt": "short visual prompt"
    }}
  ]
}}

Create exactly 5 panels.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    return json.loads(text)