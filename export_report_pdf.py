"""
export_report_pdf.py
Build the technical report PDF from Technical_Report.md.

Usage:
    python export_report_pdf.py
"""

import base64
import html as html_lib
import os
import re
from pathlib import Path

import markdown
from xhtml2pdf import pisa

ROOT = Path(__file__).resolve().parent
REPORT_MD = ROOT / "report" / "Technical_Report.md"
REPORT_PDF = ROOT / "report" / "Technical_Report.pdf"
REPORT_HTML = ROOT / "report" / "Technical_Report.html"

APPENDIX_IMAGES = [
    ("Design Diagrams", [
        ("Use Case Diagram", "diagrams/use_case_diagram.png"),
        ("System Architecture", "diagrams/architecture_diagram.png"),
        ("Flowchart – Student Registration", "diagrams/flowchart_registration.png"),
        ("Flowchart – Marks Entry and Grade Computation", "diagrams/flowchart_marks_grade.png"),
        ("UML Class Diagram", "diagrams/uml_class_diagram.png"),
        ("Menu Structure", "diagrams/menu_structure.png"),
    ]),
    ("Visualizations", [
        ("Bar Chart – Average by Subject", "outputs/charts/bar_chart.png"),
        ("Histogram – Score Distribution", "outputs/charts/histogram.png"),
        ("Pie Chart – Grade Distribution", "outputs/charts/pie_chart.png"),
        ("Line Graph – Student Averages", "outputs/charts/line_graph.png"),
    ]),
    ("Execution Screenshots", [
        ("Main Menu", "screenshots/01_main_menu.png"),
        ("Display Students", "screenshots/02_display_students.png"),
        ("Academic Transcript", "screenshots/03_transcript.png"),
        ("Statistical Analysis", "screenshots/04_statistics.png"),
        ("OOP Example", "screenshots/05_oop_demo.png"),
    ]),
]


def image_to_data_uri(path: Path) -> str:
    if not path.exists():
        return ""
    ext = path.suffix.lower().replace(".", "")
    mime = "jpeg" if ext in ("jpg", "jpeg") else ext
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/{mime};base64,{encoded}"


def build_appendix_html() -> str:
    parts = []
    appendix_letter = ord("D")
    for section_title, images in APPENDIX_IMAGES:
        parts.append(f"<h2>Appendix {chr(appendix_letter)}: {html_lib.escape(section_title)}</h2>")
        appendix_letter += 1
        for caption, rel_path in images:
            uri = image_to_data_uri(ROOT / rel_path)
            if not uri:
                parts.append(f"<p><em>{html_lib.escape(caption)} – image not found.</em></p>")
                continue
            parts.append(
                f"<p><strong>{html_lib.escape(caption)}</strong></p>"
                f'<img src="{uri}" style="max-width: 100%; margin-bottom: 16px;" />'
            )
    return "\n".join(parts)


def md_to_html(text: str) -> str:
    return markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "nl2br"],
    )


def build_html_document(body_html: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>BSD 314 Technical Report</title>
<style>
@page {{
    size: A4;
    margin: 2cm;
}}
body {{
    font-family: Helvetica, Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.45;
    color: #222;
}}
h1 {{
    font-size: 18pt;
    border-bottom: 2px solid #2F5496;
    padding-bottom: 6px;
}}
h2 {{
    font-size: 14pt;
    color: #2F5496;
    margin-top: 24px;
}}
h3 {{
    font-size: 12pt;
    color: #404040;
}}
h4 {{
    font-size: 11pt;
    color: #555;
}}
table {{
    border-collapse: collapse;
    width: 100%;
    margin: 12px 0;
    font-size: 10pt;
}}
th, td {{
    border: 1px solid #888;
    padding: 6px 8px;
    text-align: left;
}}
th {{
    background: #2F5496;
    color: white;
}}
code, pre {{
    font-family: Courier, monospace;
    font-size: 9pt;
    background: #f4f4f4;
}}
pre {{
    padding: 10px;
    border: 1px solid #ddd;
    white-space: pre-wrap;
}}
img {{
    max-width: 100%;
    display: block;
    margin: 8px 0 18px;
}}
hr {{
    border: none;
    border-top: 1px solid #ccc;
    margin: 20px 0;
}}
ul, ol {{
    margin: 8px 0 8px 22px;
}}
p {{
    margin: 8px 0;
}}
</style>
</head>
<body>
{body_html}
{build_appendix_html()}
</body>
</html>
"""


def export_pdf(html_content: str, pdf_path: Path) -> bool:
    with open(pdf_path, "wb") as pdf_file:
        result = pisa.CreatePDF(html_content, dest=pdf_file, encoding="utf-8")
    return not result.err


def main():
    if not REPORT_MD.exists():
        print(f"Report not found: {REPORT_MD}")
        return 1

    print("Building technical report...")
    md_text = REPORT_MD.read_text(encoding="utf-8")
    body_html = md_to_html(md_text)
    html_content = build_html_document(body_html)

    REPORT_HTML.write_text(html_content, encoding="utf-8")
    print(f"HTML saved: {REPORT_HTML}")

    if export_pdf(html_content, REPORT_PDF):
        print(f"PDF saved: {REPORT_PDF}")
        return 0

    print("PDF export failed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
