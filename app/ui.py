# app/ui.py
from __future__ import annotations

from pathlib import Path
import markdown
import gradio as gr

from .generator import LessonPlanGenerator
from .ingest import load_and_chunk
from .vectorstore import add_new_documents, get_vectorstore

PRESETS = {
    "Lecture":   {"length": 90,  "group": False, "quiz": False},
    "Lab":       {"length": 120, "group": True,  "quiz": True},
    "Seminar":   {"length": 60,  "group": True,  "quiz": False},
    "Workshop":  {"length": 180, "group": True,  "quiz": True},
}

gen = LessonPlanGenerator()
vs = get_vectorstore()

def _apply_preset(preset_name: str):
    cfg = PRESETS[preset_name]
    return cfg["length"], cfg["group"], cfg["quiz"]


def generate(course_title, level, preset, lesson_minutes,
             include_quiz, group_work, temperature, files):

    lesson_minutes = int(lesson_minutes)          # ← new

    query_params = {
        "course_title": course_title,
        "level": level,
        "preset": preset,
        "lesson_minutes": lesson_minutes,
        "include_quiz": include_quiz,
        "group_work": group_work,
        "temperature":  temperature,
    }

    docs = []
    if files:
        for f in files:
            chunked, warns = load_and_chunk([Path(f.name)])
            docs.extend(chunked)
            if warns:
                gr.Warning("\n".join(warns))      # ← standalone alert ✅

    if docs:
        add_new_documents(vs, docs)

    md   = gen(query_params)
    html = markdown.markdown(md, extensions=["extra", "codehilite"])  # ← safer
    return md, html


def app():
    with gr.Blocks(title="Lesson-Plan-Generator",
               analytics_enabled=False) as demo:
        gr.Markdown("## 🎓 Lesson-Plan-Generator (offline)")

        with gr.Row():
            with gr.Column(scale=1):
                course_title   = gr.Textbox(label="Course / Unit")
                level          = gr.Dropdown(["Undergrad", "Postgrad"],
                                             label="Academic level")
                preset_dd      = gr.Dropdown(list(PRESETS.keys()),
                                             label="Template preset",
                                             value="Lecture")
                lesson_minutes = gr.Number(label="Length (min)", value=90)
                temperature   = gr.Slider(
                    minimum=0.0,
                    maximum=1.0,
                    step=0.05,
                    value=0.20,
                    label="LLM temperature"
                )
                group_work     = gr.Checkbox(label="Include Group Work")
                include_quiz   = gr.Checkbox(label="Include Quiz")
            file_upload = gr.File(label="Upload PDFs / DOCX",
                                 file_count="multiple",
                                 file_types=[".pdf", ".docx"])

        submit_btn = gr.Button("⚡ Generate Lesson Plan")

        with gr.Tabs():
            with gr.TabItem("Raw Markdown"):
                # shows literal Markdown, copy-friendly
                md_raw = gr.Code(label="Markdown source",
                                 language="markdown",
                                 interactive=False)
            with gr.TabItem("Rendered Preview"):
                md_render = gr.HTML()

        # ---------- Wiring ----------
        preset_dd.change(
            _apply_preset,
            inputs=preset_dd,
            outputs=[lesson_minutes, group_work, include_quiz],
        )
        submit_btn.click(
            generate,
             inputs=[course_title, level, preset_dd, lesson_minutes,
                     include_quiz, group_work, temperature, file_upload],
            outputs=[md_raw, md_render],
        )

    return demo

