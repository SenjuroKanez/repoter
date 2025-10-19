from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches
import os

TEMPLATE_PATH = os.path.join("assets", "template.docx")
OUTPUT_DIR = "reports"

def generate_report(data):
    # Ensure output directory exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Load template
    doc = DocxTemplate(TEMPLATE_PATH)

    # Build context for docxtpl
    context = {
        "ReportNo": data.get("report_no", ""),
        "SubmittedTo": data.get("submitted_to", ""),
        "StudentsTable": data.get("students_table", ""),
        "Objectives": data.get("objectives", ""),
        "SoftwareUsed": data.get("software", ""),
        "Conclusion": data.get("conclusion", "")
    }

    # --- Handle questions dynamically ---
    questions = data.get("questions", [])
    max_questions = 5  # how many placeholders you put in the template

    for i in range(1, max_questions + 1):
        if i <= len(questions):
            q = questions[i - 1]
            context[f"Question{i}Title"] = q.get("title", f"Question {i}")
            context[f"Question{i}Text"] = q.get("text", "")

            # Add up to 3 images per question
            for img_index in range(1, 4):
                if img_index <= len(q.get("images", [])):
                    image_path = q["images"][img_index - 1]
                    if os.path.exists(image_path):
                        context[f"Question{i}Image{img_index}"] = InlineImage(doc, image_path, Inches(4))
                    else:
                        context[f"Question{i}Image{img_index}"] = ""
                else:
                    context[f"Question{i}Image{img_index}"] = ""
        else:
            # if question doesn't exist, leave placeholders empty
            context[f"Question{i}Title"] = ""
            context[f"Question{i}Text"] = ""
            for img_index in range(1, 4):
                context[f"Question{i}Image{img_index}"] = ""

    # --- Render and save ---
    output_filename = f"Lab_Report_{data.get('report_no', 'X')}.docx"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    doc.render(context)
    doc.save(output_path)

    return output_path
