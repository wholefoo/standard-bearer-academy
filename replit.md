# Covenant Academy — K-12 Homeschool LMS

## Overview
A comprehensive K-12 Homeschool Resource Platform built with Python/Flask. The platform hosts courseware for Preschool through High School from a conservative, Judeo-Evangelical Christian, and Creation-based (Young Earth/Biblical) worldview.

## Architecture
- **Backend**: Python 3.11 + Flask
- **Database**: PostgreSQL (stores student progress, quiz scores)
- **Content**: JSON files in `lessons/` directory (file-based curriculum)
- **Frontend**: Jinja2 templates with vanilla CSS/JS
- **Server**: Flask dev server on port 5000

## File Structure
```
app.py                      # Main Flask application with routes
content_loader.py           # JSON file-based curriculum content loader
db.py                       # Database utilities for progress/quiz tracking
lessons/                    # All curriculum content as JSON files
  grade1/science/           # 1st Grade Science: Days of Creation
    course.json             # Course metadata and unit structure
    day1.json - day7.json   # Individual lesson files
    creation_quiz.json      # Quiz questions
  grade9/civics/            # High School Civics & Government
    course.json             # Course metadata (Unit 1: Foundations of Liberty)
    1_1.json - 1_4.json     # Lesson files with scripture connections
    unit1_quiz.json         # Quiz questions
templates/
  base.html                 # Base template with header, nav, footer
  index.html                # Homepage with role selection
  dashboard.html            # Course Dashboard with available courses
  course.html               # Course page listing lessons (generic)
  lesson.html               # Lesson detail for elementary (memory verse, activity)
  lesson_civics.html        # Lesson detail for civics (scripture sidebar, reflection questions)
  quiz.html                 # Interactive quiz with scoring
static/
  css/style.css             # All styles including civics layout
roles/                      # User role modules (future expansion)
```

## Database Schema (PostgreSQL)
- **students**: id, username, display_name, role, created_at
- **completed_lessons**: student_id, grade, subject, unit, lesson_id, completed_at
- **quiz_scores**: student_id, grade, subject, unit, quiz_id, score, total, percentage, answers (JSONB)

## Available Courses
1. **1st Grade Science**: "The Days of Creation" — 7 lessons covering Genesis 1-2
2. **9th Grade Civics & Government**: "Foundations of Liberty" — 4 lessons
   - Lesson 1.1: The Source of Authority (Social Contract vs. Covenantal)
   - Lesson 1.2: Rights vs. Privileges (Imago Dei, Declaration of Independence)
   - Lesson 1.3: Stewardship of Power (Checks & Balances, Federalist No. 51)
   - Lesson 1.4: The Hebrew Republic (Exodus 18, Ancient Israel's governance)

## Content System
Lessons are stored as JSON files in `lessons/<grade>/<subject>/`. Each course has:
- `course.json`: metadata, unit structure, quiz references
- Individual lesson JSON files with lesson content
- Quiz JSON files with questions and explanations

To add new courses: create a new directory under `lessons/`, add `course.json` and lesson files. The app auto-discovers available courses.

## Worldview Filter
All content adheres to:
- **Science**: Creationist perspective, intelligent design, literal Genesis
- **History**: Providential history, Western Civilization, American Exceptionalism
- **Civics**: Biblical basis for government, Originalist Constitution, Natural Law, limited government
- **Ethics/Literature**: Biblical scripture, traditional Judeo-Christian values

## Running the App
```
python app.py
```
Runs on port 5000.
