# ui/components.py

import os
import re
import tkinter.filedialog as fd
import customtkinter as ctk
from core.parser import parse_questions
from core.generator import generate_report

class ReportBuilderUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("✨ Lab Report Builder ✨")
        self.geometry("1100x700")
        self.minsize(1000, 600)

        self.report_number_var = ctk.StringVar()
        self.teacher_name_var = ctk.StringVar()
        self.students = []
        self.objectives_text = None
        self.software_text = None
        self.lab_tasks_text = None
        self.conclusion_text = None

        self.questions_frame = None
        self.questions = []  # [{title, images: [(path, title)]}]

        self.template_path = os.path.join("assets", "template.docx")

        self._build_scrollable_ui()

    def _build_scrollable_ui(self):
        scroll_frame = ctk.CTkScrollableFrame(self)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self._build_ui_content(scroll_frame)

    def _build_ui_content(self, container):
        header = ctk.CTkFrame(container)
        header.pack(fill="x", pady=10, padx=10)

        ctk.CTkLabel(header, text="Report No.").pack(side="left", padx=5)
        ctk.CTkEntry(header, textvariable=self.report_number_var, width=80).pack(side="left")

        ctk.CTkLabel(header, text="Submitted to").pack(side="left", padx=5)
        ctk.CTkEntry(header, textvariable=self.teacher_name_var, width=200).pack(side="left")

        ctk.CTkButton(header, text="Choose Template", command=self._choose_template).pack(side="right", padx=5)

        # Student section
        student_frame = ctk.CTkFrame(container)
        student_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(student_frame, text="Students:").pack(anchor="w")
        self.student_container = ctk.CTkFrame(student_frame)
        self.student_container.pack(anchor="w")

        ctk.CTkButton(student_frame, text="+ Add Student", command=self._add_student).pack(anchor="w", pady=2)

        # Objective
        self.objectives_text = ctk.CTkTextbox(container, height=80)
        self._section_label(container, "Objectives").pack(anchor="w", padx=10)
        self.objectives_text.pack(fill="x", padx=10, pady=5)

        # Software
        self.software_text = ctk.CTkTextbox(container, height=80)
        self._section_label(container, "Software Used").pack(anchor="w", padx=10)
        self.software_text.pack(fill="x", padx=10, pady=5)

        # Lab Tasks
        self.lab_tasks_text = ctk.CTkTextbox(container, height=120)
        self._section_label(container, "Lab Tasks").pack(anchor="w", padx=10)
        self.lab_tasks_text.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(container, text="Parse Questions", command=self._parse_questions).pack(pady=5)

        # Questions area
        self._section_label(container, "Questions").pack(anchor="w", padx=10)
        self.questions_frame = ctk.CTkScrollableFrame(container, height=250)
        self.questions_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Conclusion
        self.conclusion_text = ctk.CTkTextbox(container, height=80)
        self._section_label(container, "Conclusion").pack(anchor="w", padx=10)
        self.conclusion_text.pack(fill="x", padx=10, pady=5)

        # Bottom buttons
        bottom = ctk.CTkFrame(container)
        bottom.pack(fill="x", pady=10)

        ctk.CTkButton(bottom, text="✨ Preview Layout ✨", command=self._preview_layout).pack(side="left", padx=5)
        ctk.CTkButton(bottom, text="+ Add Question", command=self._manual_add_question).pack(side="left", padx=5)
        ctk.CTkButton(bottom, text="🪄 Generate DOCX", command=self._generate_docx).pack(side="right", padx=5)

    def _section_label(self, container, text):
        return ctk.CTkLabel(container, text=text, font=("Helvetica", 14, "bold"))

    def _add_student(self):
        frame = ctk.CTkFrame(self.student_container)
        name_var = ctk.StringVar()
        roll_var = ctk.StringVar()
        ctk.CTkEntry(frame, placeholder_text="Name", textvariable=name_var, width=200).pack(side="left", padx=2)
        ctk.CTkEntry(frame, placeholder_text="Roll No.", textvariable=roll_var, width=100).pack(side="left", padx=2)
        ctk.CTkButton(frame, text="X", width=25, command=lambda f=frame: self._remove_student(f)).pack(side="left", padx=2)
        frame.pack(anchor="w", pady=2)
        self.students.append((frame, name_var, roll_var))

    def _remove_student(self, frame):
        for s in self.students:
            if s[0] == frame:
                self.students.remove(s)
                break
        frame.destroy()

    def _choose_template(self):
        path = fd.askopenfilename(title="Choose Template", filetypes=[("Word Documents", "*.docx")])
        if path:
            self.template_path = path

    def _parse_questions(self):
        text = self.lab_tasks_text.get("1.0", "end").strip()
        parsed = parse_questions(text)
        self._clear_questions()
        for q in parsed:
            self._create_question_block(q)

    def _manual_add_question(self):
        self._create_question_block({"title": "New Question", "images": []})

    def _create_question_block(self, qdata):
        q_frame = ctk.CTkFrame(self.questions_frame)
        title_var = ctk.StringVar(value=qdata["title"])
        ctk.CTkEntry(q_frame, textvariable=title_var).pack(fill="x", padx=5, pady=2)

        img_container = ctk.CTkFrame(q_frame)
        img_container.pack(fill="x", padx=5, pady=5)

        images = []

        def add_img():
            path = fd.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.bmp")])
            if not path:
                return
            img_title = ctk.StringVar()
            img_frame = ctk.CTkFrame(img_container)
            ctk.CTkLabel(img_frame, text=os.path.basename(path)).pack(side="left", padx=2)
            ctk.CTkEntry(img_frame, placeholder_text="Image Title", textvariable=img_title, width=150).pack(side="left", padx=2)
            ctk.CTkButton(img_frame, text="X", width=25, command=lambda f=img_frame: remove_img(f)).pack(side="left", padx=2)
            img_frame.pack(anchor="w", pady=2)
            images.append((img_frame, path, img_title))

        def remove_img(frame):
            for i in images:
                if i[0] == frame:
                    images.remove(i)
                    break
            frame.destroy()

        ctk.CTkButton(q_frame, text="+ Add Image", command=add_img).pack(anchor="w", padx=5, pady=2)

        self.questions.append({"frame": q_frame, "title_var": title_var, "images": images})
        q_frame.pack(fill="x", pady=5)

    def _clear_questions(self):
        for q in self.questions:
            q["frame"].destroy()
        self.questions.clear()

    def _preview_layout(self):
        preview = ctk.CTkToplevel(self)
        preview.title("✨ Preview Layout ✨")
        preview.geometry("600x600")
        box = ctk.CTkTextbox(preview)
        box.pack(fill="both", expand=True)

        box.insert("end", f"Report No: {self.report_number_var.get()}\n")
        box.insert("end", f"Submitted to: {self.teacher_name_var.get()}\n\n")
        box.insert("end", "Students:\n")
        for s in self.students:
            box.insert("end", f" - {s[1].get()} ({s[2].get()})\n")

        box.insert("end", "\nObjectives:\n" + self.objectives_text.get("1.0", "end").strip() + "\n")
        box.insert("end", "\nSoftware Used:\n" + self.software_text.get("1.0", "end").strip() + "\n")

        box.insert("end", "\nQuestions:\n")
        for i, q in enumerate(self.questions, 1):
            box.insert("end", f"{i}. {q['title_var'].get()}\n")
            for img in q["images"]:
                box.insert("end", f"   - {os.path.basename(img[1])} ({img[2].get()})\n")

        box.insert("end", "\nConclusion:\n" + self.conclusion_text.get("1.0", "end").strip())
        box.configure(state="disabled")

    def _generate_docx(self):
        students_data = [(s[1].get(), s[2].get()) for s in self.students]
        objectives = self.objectives_text.get("1.0", "end").strip()
        software = self.software_text.get("1.0", "end").strip()
        conclusion = self.conclusion_text.get("1.0", "end").strip()

        questions_data = []
        for q in self.questions:
            q_title = q["title_var"].get()
            q_images = [(img[1], img[2].get()) for img in q["images"]]
            questions_data.append((q_title, q_images))

        out_path = fd.asksaveasfilename(defaultextension=".docx", filetypes=[("Word Document", "*.docx")])
        if out_path:
            generate_report(
                template_path=self.template_path,
                output_path=out_path,
                report_number=self.report_number_var.get(),
                teacher_name=self.teacher_name_var.get(),
                students=students_data,
                objectives=objectives,
                software=software,
                questions=questions_data,
                conclusion=conclusion
            )
