# File: app/prompts.py
"""Prompt templates for the generation pipeline.

*One source of truth for every LLM in the repo.*

This revision deepens each lesson‑plan section and tells the model it **may
supplement** the uploaded context with generally accepted knowledge of the
subject (based on the Course / Unit name) when that will enrich learning.
"""

from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

# ---------------------------------------------------------------------------
# System persona
# ---------------------------------------------------------------------------

SYSTEM_MESSAGE = (
    "You are an award‑winning instructional designer and university lecturer. "
    "You excel at constructive alignment, backward design, Bloom’s *revised* "
    "taxonomy, and Gagné’s Nine Events of Instruction.  Your lesson plans are "
    "student‑centred, inclusively written, and ready to paste into Blackboard "
    "Ultra without further editing.  When relevant, you may incorporate "
    "commonly‑accepted disciplinary facts **not** present in the supplied "
    "documents if they clearly improve learning outcomes."
)

# ---------------------------------------------------------------------------
# Human prompt
# ---------------------------------------------------------------------------

HUMAN_TEMPLATE = """\
### Context
{context}

### Lesson Parameters
- **Course / Unit**: {course_title}
- **Academic level**: {level}
- **Preset type**: {preset}
- **Lesson length**: {lesson_minutes} minutes
- **Include group work?** {group_work}
- **Include quiz?** {include_quiz}

### Your task
Using **only** the information above and your own disciplinary expertise, draft
an enriched Markdown lesson plan that follows **all** headings and constraints
below *exactly*.

---
## 1 Overview  
*120‑word cap; engaging, nuanced rationale that links prior knowledge, real‑world significance, and how today’s concepts fit the overall unit.*

## 2 Intended Learning Outcomes  
*3–6 bullets; each ends with a Bloom tag in italics (Remember, Understand, Apply, Analyse, Evaluate, Create).*  Outcomes must be SMART and scoped to the single lesson.

## 3 Session Structure  
Markdown table with **bold major phases** (e.g. *Introduction*, *Concept Discovery*, *Practice & Feedback*, *Reflection*).  Each phase may have 1‑3 indented sub‑rows.  Columns:
`Start – End | Phase | Gagné Event | Learning Activity (brief) | Resources`  
Allocate times that *sum exactly* to the lesson length.

## 4 Group‑Work Activity  
*Omit entire heading if* **Include group work?** is `False`.  Otherwise:
1. 90‑word description that tells students *what* they will create and *why it matters*.
2. **Instructions** – ordered list detailing roles, deliverables, and timing.
3. **Rubric** – table `Criteria | Excellent | Good | Fair | Poor`.

## 5 MCQ Quiz  
*Omit if* **Include quiz?** is `False`. Otherwise write **exactly 10 questions**. Each question:
```text
### Q1
A. …
B. …
C. …
D. …
**Answer: C**
```
Questions must be higher‑order where possible; options must all be plausible.

## 6 Constructive Alignment Check  
Short paragraph evaluating coherence between learning outcomes, activities, and assessment. If misalignment exists, begin the paragraph with ⚠️ and specify which section to revise.

---
**Formatting rules**
1. Use second‑person plural where possible ("students will …").
2. No unexplained jargon; link technical terms in parentheses if needed.
3. Output **pure GitHub‑flavoured Markdown** – no HTML.
"""

# ---------------------------------------------------------------------------
# Prompt objects
# ---------------------------------------------------------------------------

LESSON_CHAT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_MESSAGE),
    ("human", HUMAN_TEMPLATE),
])

LESSON_STRING_PROMPT = PromptTemplate.from_template(SYSTEM_MESSAGE + "\n\n" + HUMAN_TEMPLATE)

# Export alias used by the rest of the code (chat models preferred)
LESSON_PROMPT = LESSON_CHAT_PROMPT

