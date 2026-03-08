# Covenant Academy — K-12 Homeschool LMS

## Overview
A comprehensive K-12 Homeschool Resource Platform built with Python/Flask. The platform hosts courseware for Preschool through High School from a conservative, Judeo-Evangelical Christian, and Creation-based (Young Earth/Biblical) worldview.

## Architecture
- **Backend**: Python 3.11 + Flask
- **Frontend**: Jinja2 templates with vanilla CSS/JS
- **Server**: Flask dev server on port 5000

## File Structure
```
app.py                      # Main Flask application with routes and curriculum data
templates/
  base.html                 # Base template with header, nav, footer
  index.html                # Homepage with role selection, grade levels, subjects
  dashboard.html            # Course Dashboard with grade/subject selection
  course.html               # Course page listing lessons
  lesson.html               # Individual lesson detail view
  quiz.html                 # Interactive quiz with scoring
static/
  css/style.css             # All styles
  js/                       # JavaScript (quiz logic is inline currently)
  images/                   # Static images
curriculum/
  prek/ - grade12/          # Content directories for each grade level
  grade1/science/           # Proof of concept: Days of Creation
roles/                      # User role modules (parent, teacher, student)
```

## Current State (Phase 1)
- Homepage with role selection (Parent, Teacher, Student)
- Course Dashboard with grade level and subject selection
- Proof of concept: 1st Grade Science — "The Days of Creation"
  - 7 complete lesson plans (one per day of creation)
  - Scripture memory verses for each lesson
  - Discussion questions and hands-on activities
  - 10-question interactive quiz with scoring and explanations
- All other grade/subject combinations show "Coming Soon"

## Worldview Filter
All content adheres to:
- **Science**: Creationist perspective, intelligent design, literal Genesis
- **History**: Providential history, Western Civilization, American Exceptionalism
- **Ethics/Literature**: Biblical scripture, traditional Judeo-Christian values

## Running the App
```
python app.py
```
Runs on port 5000.
