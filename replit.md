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
  prek/bible/               # PreK Bible ABCs
  kindergarten/bible/       # Kindergarten God's Numbers
  grade1/science/           # 1st Grade: Days of Creation
  grade2/science/           # 2nd Grade: God's Amazing Animals
  grade3/reading/           # 3rd Grade: Stories of Faith
  grade4/history/           # 4th Grade: America's Godly Heritage
  grade5/science/           # 5th Grade: The Human Body
  grade6/history/           # 6th Grade: Ancient Civilizations
  grade7/science/           # 7th Grade: Earth Science
  grade8/history/           # 8th Grade: American History
  grade9/civics/            # 9th Grade: Civics & Government
  grade10/history/          # 10th Grade: World History
  grade11/reading/          # 11th Grade: American Literature
  grade12/civics/           # 12th Grade: Economics & Free Enterprise
templates/
  base.html                 # Base template with header, nav, footer
  index.html                # Homepage with role selection
  dashboard.html            # Course Dashboard with available courses
  course.html               # Course page listing lessons (generic)
  lesson.html               # Lesson detail for elementary (memory verse, activity)
  lesson_civics.html        # Lesson detail for middle/high school (scripture sidebar, reflection)
  quiz.html                 # Interactive quiz with scoring
static/
  css/style.css             # All styles including civics layout
```

## Database Schema (PostgreSQL)
- **students**: id, username, display_name, role, created_at
- **completed_lessons**: student_id, grade, subject, unit, lesson_id, completed_at
- **quiz_scores**: student_id, grade, subject, unit, quiz_id, score, total, percentage, answers (JSONB)

## Available Courses (14 total)
| Grade | Subject | Course Title |
|-------|---------|-------------|
| PreK | Bible | Bible ABCs — Learning Letters Through Scripture |
| Kindergarten | Bible | God's Numbers — Counting Through Scripture |
| 1st Grade | Science | The Days of Creation |
| 2nd Grade | Science | God's Amazing Animals |
| 3rd Grade | Reading | Stories of Faith — Reading and Writing with Purpose |
| 4th Grade | History | America's Godly Heritage — From Columbus to the Constitution |
| 5th Grade | Science | The Human Body — Fearfully and Wonderfully Made |
| 6th Grade | History | Ancient Civilizations — God's Hand in History |
| 7th Grade | Science | Earth Science — Exploring God's World |
| 8th Grade | History | American History — Providence and Liberty |
| 9th Grade | Civics | Civics & Government — Foundations of Liberty |
| 10th Grade | History | World History — The Unfolding of God's Plan |
| 11th Grade | Reading | American Literature — Faith, Freedom, and the Written Word |
| 12th Grade | Civics | Economics & Free Enterprise — Biblical Stewardship |

## Content System
Lessons are stored as JSON files in `lessons/<grade>/<subject>/`. Each course has:
- `course.json`: metadata, unit structure, quiz references
- Individual lesson JSON files with lesson content
- Quiz JSON files with questions and explanations

**Elementary format** (PreK-5): memory_verse, objective, content (string array), activity, discussion
**Middle/High school format**: scripture_connection (verses array), content (heading/paragraphs), reflection_questions, key_concepts, primary_source

Template routing: lessons with `scripture_connection` field use `lesson_civics.html`; others use `lesson.html`.

To add new courses: create a new directory under `lessons/`, add `course.json` and lesson files. The app auto-discovers available courses.

## Grade Levels
GRADE_LEVELS in app.py includes: prek, kindergarten, grade1-grade12 (15 levels total)

## Worldview Filter
All content adheres to:
- **Science**: Creationist perspective, intelligent design, literal Genesis, Young Earth
- **History**: Providential history, Western Civilization, American Exceptionalism
- **Civics**: Biblical basis for government, Originalist Constitution, Natural Law, limited government
- **Reading/Literature**: Biblical values, Christian literary analysis
- **Bible**: Direct Scripture study, age-appropriate
- **Economics**: Free market from Biblical stewardship perspective

## Running the App
```
python app.py
```
Runs on port 5000.
