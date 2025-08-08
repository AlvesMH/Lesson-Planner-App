# 🎓 Lesson Plan Generator

An AI-powered teaching assistant that helps educators **design engaging, professional-grade lesson plans** in minutes.

This web app uses modern AI with your own uploaded documents (PDF, DOCX) for **context-aware lesson planning**.  
It produces:

- 📝 **Complete lesson plans** (with timing breakdowns)  
- 👥 **Group activity handouts** in customizable formats  
- 📋 **Instructor pointers & helpers** for in-class delivery  

Built with **FastAPI** + **React** for speed, ease of use, and a polished professional UI.

---

## 💡 Tips for Best Results

### Upload relevant, clean documents (avoid scanned images without OCR).

### For more creativity, increase Temperature slightly (0.4–0.7).

### Use Advanced settings for token and probability control when refining outputs.

### Keep lesson length realistic for content depth.

### Save your DOCX outputs immediately after generation — Render's free tier has ephemeral storage.


## 🚀 Benefits

### 1. Save Hours of Prep Time
Instead of starting from scratch, generate a **timed, structured plan** tailored to your course level and teaching style.

### 2. Personalize with Your Materials
Upload your existing slides, readings, or notes — the AI uses them for **augmented generation** so the output reflects **your** content.

### 3. Flexible Activity Generation
Choose from 10 pre-designed **group activity formats** for interactive learning, or skip them if not needed.

### 4. Instructor Cheat Sheets
Instantly generate a **bullet-point summary** with key talking points, reminders, and tips for delivering the lesson.

### 5. Professional Look & Feel
Outputs are **.DOCX** files ready to print or share with students and co-teachers.

---

## 📸 How It Works

1. **Enter course info** – Title, academic level, lesson length, and teaching style preset.
2. **Adjust creativity** – Tune *Temperature*, *top_p*, and *max_tokens* for AI output style.
3. **Upload materials** – PDFs or DOCX files for the AI to reference.
4. **Generate lesson plan** – Initial draft *omits activity details* but reserves time for them.
5. **Add group activities** – Pick a format from the built-in library and download a ready-to-use student handout.
6. **Get instructor pointers** – Download a teacher-focused document with bullet points, reminders, and helper tips.

---

## 🖥 Using the App

### **Main Screen**
- **Course / Unit**: The title of your lesson.
- **Level**: Undergrad or Postgrad.
- **Preset**: Lecture, Lab, Seminar, or Workshop.
- **Lesson Minutes**: Total time available for the lesson.
- **Temperature**: Adjusts AI creativity (lower = more factual, higher = more creative).
- **Advanced Settings**: Optional *top_p* and *max_tokens* controls.
- **Include Group Work** / **Include Quiz**: Flags for lesson structure (time budget only; details generated later).

### **Buttons**
- **Generate Lesson Plan**: Creates the initial plan (with activity slot reserved).
- **Generate Class Activity**: Lets you choose one of 10 activity formats and download a student handout (.docx).
- **Generate Instructor Pointers**: Creates a bullet-point cheat sheet for teaching (.docx).
- **How to Use**: Opens a quick guide within the app.

---

## 📂 Output Files

All downloadable outputs are in **Microsoft Word (.DOCX)** format:
- `lesson_plan.docx` – Full lesson plan with timing breakdown.
- `activity_handout.docx` – Student-facing activity instructions.
- `instructor_pointers.docx` – Teacher-facing bullet-point notes.

---

## 🛠 Local Development

### **Requirements**
- Python 3.11+
- Node.js 18+
- pip & npm installed

### **Setup**
```bash
# Clone repo
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

# Backend setup
pip install -r requirements.txt

# Frontend setup
cd frontend
npm install
npm run build
cd ..

# Run server
uvicorn backend.main:app --reload
Open: http://127.0.0.1:8000
```

---

## 📜 License
**_MIT License – Free for personal and educational use._**

