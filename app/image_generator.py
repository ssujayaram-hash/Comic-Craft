import os
import base64
from pathlib import Path

from google import genai
from dotenv import load_dotenv


load_dotenv()


IMAGE_MODEL = "gemini-3.1-flash-image"

PANELS_DIR = Path("static/panels")
PANELS_DIR.mkdir(parents=True, exist_ok=True)


client = genai.Client(
    api_key=os.getenv("GEMINI_IMAGE_API_KEY")
)


def generate_panel_image(
    image_prompt: str,
    panel_number: int
):
    """
    Generate one comic panel image using Gemini.
    """

    if not os.getenv("GEMINI_IMAGE_API_KEY"):
        raise RuntimeError(
            "GEMINI_IMAGE_API_KEY is missing from .env"
        )

    prompt = f"""
Create a single comic-book panel illustration.

{image_prompt}

Requirements:
- High-quality comic illustration
- Clear main character
- Clear environment
- Strong visual storytelling
- Consistent character appearance
- No captions
- No speech bubbles
- No written text
- Suitable for a five-panel comic
"""

    interaction = client.interactions.create(
        model=IMAGE_MODEL,
        input=prompt,
        response_format={
            "type": "image",
            "mime_type": "image/jpeg",
            "aspect_ratio": "16:9",
            "image_size": "1K"
        }
    )

    if not interaction.output_image:
        raise RuntimeError(
            f"Gemini did not return an image for panel {panel_number}."
        )

    image_data = base64.b64decode(
        interaction.output_image.data
    )

    output_path = (
        PANELS_DIR / f"panel_{panel_number}.jpg"
    )

    with open(output_path, "wb") as file:
        file.write(image_data)

    return str(output_path).replace("\\", "/")


def generate_all_panel_images(outline):
    """
    Generate images for all five panels.
    """

    panels = outline.get("panels", [])

    if len(panels) != 5:
        raise ValueError(
            "ComicCraft requires exactly 5 panels."
        )

    image_paths = []

    for panel in panels:

        panel_number = panel.get("panel_number")

        image_prompt = panel.get(
            "image_prompt",
            ""
        )

        if not image_prompt:
            raise ValueError(
                f"Image prompt missing for panel {panel_number}."
            )

        image_path = generate_panel_image(
            image_prompt,
            panel_number
        )

        image_paths.append(image_path)

    return image_paths