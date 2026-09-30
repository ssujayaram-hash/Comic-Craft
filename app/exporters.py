from pathlib import Path
from fpdf import FPDF


EXPORTS_DIR = Path("static/exports")
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)


def safe_text(text):
    if text is None:
        return ""

    return str(text).encode("latin-1", "replace").decode("latin-1")


def write_text(pdf, text, font_style="", size=12):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Helvetica", font_style, size)
    pdf.multi_cell(
        pdf.epw,
        7,
        safe_text(text),
        new_x="LMARGIN",
        new_y="NEXT"
    )


def save_pdf(layout):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for panel in layout:
        pdf.add_page()

        pdf.set_x(pdf.l_margin)
        pdf.set_font("Helvetica", "B", 18)
        pdf.cell(
            pdf.epw,
            10,
            safe_text(panel["title"]),
            new_x="LMARGIN",
            new_y="NEXT",
            align="C"
        )

        image_path = panel["image_path"]

        if Path(image_path).exists():
            pdf.image(
                image_path,
                x=10,
                y=30,
                w=190
            )

        pdf.set_y(140)

        write_text(
            pdf,
            f"Scene: {panel['scene_description']}"
        )

        pdf.ln(3)

        write_text(
            pdf,
            f"Narration: {panel['narration']}",
            "I"
        )

        pdf.ln(3)

        for dialogue in panel["dialogue"]:
            character = safe_text(dialogue.get("character", ""))
            text = safe_text(dialogue.get("text", ""))

            write_text(
                pdf,
                f"{character}: {text}"
            )

    output_path = EXPORTS_DIR / "comiccraft_comic.pdf"

    pdf.output(str(output_path))

    return str(output_path).replace("\\", "/")