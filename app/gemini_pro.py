import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_story(outline):
    prompt = f"""
Turn the following 5-panel comic outline into a complete comic script.

OUTLINE:
{json.dumps(outline, indent=2)}

For every panel, provide:
- panel_number
- title
- narration
- dialogue

Return ONLY valid JSON in this format:

{{
  "panels": [
    {{
      "panel_number": 1,
      "title": "Panel title",
      "narration": "Short narration",
      "dialogue": [
        {{
          "character": "Character name",
          "text": "Dialogue"
        }}
      ]
    }}
  ]
}}

There must be exactly 5 panels.
Keep the dialogue short enough to fit naturally inside a comic panel.
Make the story flow naturally from panel 1 to panel 5.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)