from fastapi import (
    APIRouter,
    Form,
    HTTPException,
    Request,
    UploadFile,
    File
)

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.gemini_flash import generate_outline
from app.gemini_pro import generate_story
from app.layout_builder import build_comic_layout
from app.exporters import save_pdf

from pathlib import Path


router = APIRouter()

templates = Jinja2Templates(directory="templates")

PANELS_DIR = Path("static/panels")
PANELS_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# TEST ROUTE
# --------------------------------------------------

@router.get("/test")
def test_route():
    return {
        "message": "ComicCraft routes are working!"
    }


# --------------------------------------------------
# STEP 1:
# Generate story, outline and image prompts
# --------------------------------------------------

@router.post("/generate", response_class=HTMLResponse)
async def generate_comic(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...)
):

    try:

        # Generate 5-panel outline
        outline = generate_outline(
            story_prompt,
            character_name,
            setting,
            tone,
            art_style
        )

        # Generate narration and dialogue
        story = generate_story(outline)

        # Show the five image prompts
        # and allow the user to upload images manually
        return templates.TemplateResponse(
            request=request,
            name="comic_upload.html",
            context={
                "outline": outline,
                "story": story
            }
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Story generation failed: {str(e)}"
        )


# --------------------------------------------------
# STEP 2:
# Upload the 5 manually generated images
# --------------------------------------------------

@router.post("/upload-images", response_class=HTMLResponse)
async def upload_images(
    request: Request,

    outline_json: str = Form(...),
    story_json: str = Form(...),

    panel_1: UploadFile = File(...),
    panel_2: UploadFile = File(...),
    panel_3: UploadFile = File(...),
    panel_4: UploadFile = File(...),
    panel_5: UploadFile = File(...)
):

    try:

        import json

        # Convert hidden JSON back into Python dictionaries
        outline = json.loads(outline_json)
        story = json.loads(story_json)

        uploaded_files = [
            panel_1,
            panel_2,
            panel_3,
            panel_4,
            panel_5
        ]

        image_paths = []

        # Save each uploaded image
        for index, upload in enumerate(
            uploaded_files,
            start=1
        ):

            if not upload.filename:
                raise HTTPException(
                    status_code=400,
                    detail=f"Panel {index} image is missing."
                )

            # Get file extension
            extension = Path(
                upload.filename
            ).suffix.lower()

            # Allowed image formats
            allowed_extensions = [
                ".jpg",
                ".jpeg",
                ".png",
                ".webp"
            ]

            if extension not in allowed_extensions:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Panel {index}: unsupported image format. "
                        "Use JPG, JPEG, PNG or WEBP."
                    )
                )

            # Save with predictable filename
            output_path = (
                PANELS_DIR /
                f"panel_{index}{extension}"
            )

            # Read image
            image_data = await upload.read()

            # Save image
            with open(output_path, "wb") as file:
                file.write(image_data)

            image_paths.append(
                str(output_path).replace("\\", "/")
            )

        # Build comic layout
        layout = build_comic_layout(
            outline,
            story,
            image_paths
        )

        # Create PDF
        pdf_path = save_pdf(layout)

        # Show professional comic preview
        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={
                "layout": layout,
                "pdf_path": "/" + pdf_path
            }
        )

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Comic creation failed: {str(e)}"
        )


# --------------------------------------------------
# JSON API ROUTE
# --------------------------------------------------

@router.post("/generate-comic/json")
async def generate_comic_json(data: dict):

    try:

        story_prompt = data.get(
            "story_prompt",
            ""
        )

        character_name = data.get(
            "character_name",
            ""
        )

        setting = data.get(
            "setting",
            ""
        )

        tone = data.get(
            "tone",
            ""
        )

        art_style = data.get(
            "art_style",
            ""
        )

        outline = generate_outline(
            story_prompt,
            character_name,
            setting,
            tone,
            art_style
        )

        story = generate_story(outline)

        return {
            "outline": outline,
            "story": story
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Generation failed: {str(e)}"
        )


# --------------------------------------------------
# EXPORT SUCCESS PAGE
# --------------------------------------------------

@router.get(
    "/export-success",
    response_class=HTMLResponse
)
async def export_success(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={}
    )