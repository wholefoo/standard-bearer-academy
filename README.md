# Standard Bearer Academy

A comprehensive K-12 Homeschool Learning Management System (LMS) built with Python/Flask, featuring **115 courses** and **905+ lessons and quizzes** across **10 subjects**, all rooted in a conservative, Judeo-Evangelical Christian, Creation-based (Young Earth/Biblical) worldview.

> *"Train up a child in the way he should go; even when he is old he will not depart from it."* — Proverbs 22:6

The platform is currently in **public beta** — the entire curriculum is freely accessible for review, with no login required.

---

## Table of Contents

- [Features](#features)
- [Curriculum](#curriculum)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Database Schema](#database-schema)
- [Content System](#content-system)
- [SEO & Discoverability](#seo--discoverability)
- [Roadmap](#roadmap)
- [Contact](#contact)

---

## Features

- **115 courses** spanning PreK through 12th Grade across 10 subjects
- **905+ JSON-based lesson and quiz files** with automatic course discovery
- **Interactive quizzes** with instant scoring, detailed explanations, and unlimited retakes
- **Progress tracking** for completed lessons and quiz scores (PostgreSQL-backed)
- **Responsive design** that works on desktop, laptop, tablet, and mobile
- **25-question FAQ** organized into 6 categories with accordion behavior
- **Full SEO/AEO/GEO/SMO optimization** — structured data, sitemap, social cards, and AI crawler support
- **Legal pages** — About Us, Privacy Policy, and Terms of Use
- **Public beta mode** — open access for content review with no account required

---

## Curriculum

### Grade Levels (15 total)
PreK, Kindergarten, and 1st through 12th Grade.

### Subjects (10 total)

| Subject | Grade Range | Worldview Focus |
|---|---|---|
| Science | PreK–12 | Young Earth Creationism, Intelligent Design, literal Genesis |
| Mathematics | PreK–12 | Standard curriculum with Biblical stewardship applications |
| Reading & Language Arts | PreK–12 | Phonics-based, Christian literary tradition |
| History & Social Studies | PreK–12 | Providential history, Western Civilization |
| Bible & Scripture | PreK–12 | Old and New Testament, age-appropriate depth |
| Civics & Government | PreK–12 | Constitutional originalism, Biblical basis for law |
| Art & Science Projects | PreK–8 | Hands-on STEAM creativity |
| Technology | 6–12 | Digital citizenship, programming, AI ethics |
| Creative Writing | 6–12 | Writing as worship and craft |
| Life Skills | 6–12 | Financial literacy, home economics, career prep |

### Lesson Formats

- **Elementary (PreK–5):** memory verse, learning objective, lesson content, hands-on activity, discussion questions
- **Middle/High School (6–12):** scripture connection sidebar, structured content with headings, key concepts, reflection questions, primary source references (high school)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11 + Flask |
| Database | PostgreSQL |
| Templating | Jinja2 |
| Frontend | Vanilla CSS + JavaScript |
| Content Storage | JSON files (file-based curriculum) |
| Analytics | Google Analytics 4 |
| Server | Flask (dev) / Gunicorn (production), port 5000 |

---

## Project Structure

```
app.py                      # Main Flask application with all routes
content_loader.py           # JSON file-based curriculum content loader
db.py                       # Database utilities for progress/quiz tracking
lessons/                    # All curriculum content as JSON files
  <grade>/<subject>/        # course.json + lesson files + quiz files
templates/
  base.html                 # Base template with header, nav, footer, meta tags
  index.html                # Homepage with mission, subjects, FAQ
  dashboard.html            # Parent/Teacher course dashboard
  grade.html                # Grade level course listing
  course.html               # Course page listing lessons
  lesson.html               # Lesson detail (elementary format)
  lesson_civics.html        # Lesson detail (middle/high school format)
  quiz.html                 # Interactive quiz with scoring
  about.html                # About Us page
  privacy.html              # Privacy Policy page
  terms.html                # Terms of Use page
static/
  css/style.css             # All styles
  js/                       # JavaScript
  images/                   # Social share image and assets
```

---

## Getting Started

### Prerequisites
- Python 3.11
- PostgreSQL database (connection provided via `DATABASE_URL` environment variable)

### Running the App

```bash
python app.py
```

The application runs on **port 5000**. The database tables are initialized automatically on startup via `init_db()`.

### Environment Variables
- `DATABASE_URL` — PostgreSQL connection string (or individual `PG*` variables)
- `FLASK_DEBUG` — set to `true` to enable debug mode (optional)

---

## Database Schema (PostgreSQL)

- **students** — `id`, `username`, `display_name`, `role`, `created_at`
- **completed_lessons** — `student_id`, `grade`, `subject`, `unit`, `lesson_id`, `completed_at`
- **quiz_scores** — `student_id`, `grade`, `subject`, `unit`, `quiz_id`, `score`, `total`, `percentage`, `answers` (JSONB)

---

## Content System

Lessons are stored as JSON files in `lessons/<grade>/<subject>/`. Each course includes:

- `course.json` — metadata, unit structure, quiz references
- Individual lesson JSON files
- Quiz JSON files with questions and explanations

**Template routing:** lessons containing a `scripture_connection` field render with `lesson_civics.html` (middle/high school); all others use `lesson.html` (elementary).

**Adding new courses:** create a directory under `lessons/`, add a `course.json` and lesson files — the app auto-discovers them. No code changes required, and they automatically appear in the sitemap and AI catalog files.

---

## SEO & Discoverability

- **Meta tags** — unique title, description, keywords, canonical URL on every page
- **Structured data (JSON-LD)** — EducationalOrganization, WebSite (with SearchAction), FAQPage, Course, LearningResource, Quiz, CollectionPage, BreadcrumbList
- **Open Graph & Twitter cards** — including a custom 1200×630 branded social share image
- **Dynamic XML sitemap** — `/sitemap.xml` with 5,500+ URLs, auto-generated from content
- **AI crawler support** — `/robots.txt` permits 14 AI bots; `/llms.txt` and `/llms-full.txt` provide structured summaries and the full course catalog for AI systems

---

## Roadmap

The current public beta focuses on open content review. The foundation is in place to add full LMS functionality:

- User accounts (parent, teacher, student roles) with authentication
- Multi-student progress tracking
- Parent/Teacher admin dashboard with assignment and grading tools
- Per-student transcripts and credit-hour tracking
- Diploma certificate generation
- Email notifications and course assignment workflows

---

## Contact

**Mike Mallek** — Founder
Email: [boundlessvolumes@gmail.com](mailto:boundlessvolumes@gmail.com)

---

*© 2026 Standard Bearer Academy — A Christ-Centered K-12 Homeschool Platform*
