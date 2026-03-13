from flask import Flask, render_template, request, jsonify, redirect, url_for, Response, make_response
import os
import logging
from datetime import datetime
from content_loader import (
    load_course, load_lesson, load_quiz,
    get_all_lessons_for_course, get_lesson_navigation,
    get_available_courses
)
from db import record_quiz_score, init_db

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.environ.get("SESSION_SECRET", "homeschool-lms-dev-key"))

init_db()

GRADE_LEVELS = {
    "prek": {"name": "Pre-Kindergarten", "short": "PreK", "order": 0},
    "kindergarten": {"name": "Kindergarten", "short": "K", "order": 0.5},
    "grade1": {"name": "1st Grade", "short": "1st", "order": 1},
    "grade2": {"name": "2nd Grade", "short": "2nd", "order": 2},
    "grade3": {"name": "3rd Grade", "short": "3rd", "order": 3},
    "grade4": {"name": "4th Grade", "short": "4th", "order": 4},
    "grade5": {"name": "5th Grade", "short": "5th", "order": 5},
    "grade6": {"name": "6th Grade", "short": "6th", "order": 6},
    "grade7": {"name": "7th Grade", "short": "7th", "order": 7},
    "grade8": {"name": "8th Grade", "short": "8th", "order": 8},
    "grade9": {"name": "9th Grade", "short": "9th", "order": 9},
    "grade10": {"name": "10th Grade", "short": "10th", "order": 10},
    "grade11": {"name": "11th Grade", "short": "11th", "order": 11},
    "grade12": {"name": "12th Grade", "short": "12th", "order": 12},
}

SUBJECTS = {
    "science": {"name": "Science", "icon": "🔬"},
    "math": {"name": "Mathematics", "icon": "📐"},
    "reading": {"name": "Reading & Language Arts", "icon": "📖"},
    "history": {"name": "History & Social Studies", "icon": "🏛️"},
    "bible": {"name": "Bible & Scripture", "icon": "✝️"},
    "civics": {"name": "Civics & Government", "icon": "⚖️"},
    "technology": {"name": "Technology", "icon": "💻"},
    "creative_writing": {"name": "Creative Writing", "icon": "✍️"},
    "life_skills": {"name": "Life Skills", "icon": "🛠️"},
    "art_science_projects": {"name": "Art & Science Projects", "icon": "🎨"},
}

USER_ROLES = {
    "parent": {"name": "Parent / Teacher", "description": "Assign Lessons, Grade Essays, View Student Progress, Set Rewards."},
    "teacher": {"name": "Teacher", "description": "Create lessons, grade assignments, and track student progress"},
    "student": {"name": "Student", "description": "Access lessons, complete quizzes, and track your learning"},
}


def get_subject_info(subject):
    return SUBJECTS.get(subject, {"name": subject.title(), "icon": "📚"})


@app.route("/health")
def health():
    return "ok", 200


@app.route("/")
def homepage():
    try:
        available_courses = get_available_courses()
    except Exception as e:
        logging.error(f"Error loading courses: {e}")
        available_courses = []
    return render_template("index.html", roles=USER_ROLES, grades=GRADE_LEVELS,
                           subjects=SUBJECTS, available_courses=available_courses)


@app.route("/dashboard")
def dashboard():
    role = request.args.get("role", "parent")
    if role not in USER_ROLES:
        role = "parent"
    try:
        available_courses = get_available_courses()
    except Exception as e:
        logging.error(f"Error loading courses: {e}")
        available_courses = []
    return render_template("dashboard.html", role=role, roles=USER_ROLES,
                           grades=GRADE_LEVELS, subjects=SUBJECTS,
                           available_courses=available_courses)


@app.route("/grade/<grade>")
def grade_page(grade):
    grade_info = GRADE_LEVELS.get(grade)
    if not grade_info:
        return redirect(url_for("homepage"))
    available_courses = get_available_courses()
    grade_courses = [c for c in available_courses if c["grade"] == grade]
    return render_template("grade.html", grade=grade, grade_info=grade_info,
                           grades=GRADE_LEVELS, subjects=SUBJECTS,
                           grade_courses=grade_courses)


@app.route("/course/<grade>/<subject>")
def course(grade, subject):
    grade_info = GRADE_LEVELS.get(grade)
    subject_info = get_subject_info(subject)
    if not grade_info:
        return redirect(url_for("dashboard"))

    lessons, course_data = get_all_lessons_for_course(grade, subject)
    return render_template("course.html", grade=grade, grade_info=grade_info,
                           subject=subject, subject_info=subject_info,
                           lessons=lessons, course_data=course_data)


@app.route("/lesson/<grade>/<subject>/<lesson_id>")
def lesson(grade, subject, lesson_id):
    grade_info = GRADE_LEVELS.get(grade)
    subject_info = get_subject_info(subject)
    if not grade_info:
        return redirect(url_for("dashboard"))

    prev_lesson, lesson_data, next_lesson = get_lesson_navigation(grade, subject, lesson_id)
    if not lesson_data:
        return redirect(url_for("course", grade=grade, subject=subject))

    has_scripture_sidebar = "scripture_connection" in lesson_data
    has_reflection = "reflection_questions" in lesson_data

    template = "lesson_civics.html" if has_scripture_sidebar else "lesson.html"

    return render_template(template, lesson=lesson_data,
                           grade=grade, subject=subject,
                           grade_info=grade_info, subject_info=subject_info,
                           prev_lesson=prev_lesson, next_lesson=next_lesson,
                           course_data=load_course(grade, subject))


@app.route("/quiz/<grade>/<subject>")
def quiz(grade, subject):
    grade_info = GRADE_LEVELS.get(grade)
    subject_info = get_subject_info(subject)
    if not grade_info:
        return redirect(url_for("dashboard"))

    course_data = load_course(grade, subject)
    if not course_data:
        return redirect(url_for("course", grade=grade, subject=subject))

    quiz_id = course_data.get("quiz_id")
    quiz_data = load_quiz(grade, subject, quiz_id) if quiz_id else None
    if not quiz_data:
        return redirect(url_for("course", grade=grade, subject=subject))

    return render_template("quiz.html", questions=quiz_data["questions"],
                           quiz_data=quiz_data,
                           grade=grade, subject=subject,
                           grade_info=grade_info, subject_info=subject_info)


@app.route("/api/quiz/submit", methods=["POST"])
def submit_quiz():
    data = request.get_json()
    answers = data.get("answers", {})
    grade = data.get("grade", "")
    subject = data.get("subject", "")
    quiz_id = data.get("quiz_id", "")

    course_data = load_course(grade, subject)
    if not course_data:
        return jsonify({"error": "Course not found"}), 404

    actual_quiz_id = quiz_id or course_data.get("quiz_id", "")
    quiz_data = load_quiz(grade, subject, actual_quiz_id)
    if not quiz_data:
        return jsonify({"error": "Quiz not found"}), 404

    questions = quiz_data["questions"]
    results = []
    score = 0
    total = len(questions)

    for q in questions:
        user_answer = answers.get(str(q["id"]))
        is_correct = user_answer == q["correct"]
        if is_correct:
            score += 1
        results.append({
            "id": q["id"],
            "correct": is_correct,
            "correct_answer": q["correct"],
            "user_answer": user_answer,
            "explanation": q["explanation"]
        })

    percentage = round((score / total) * 100) if total > 0 else 0

    try:
        record_quiz_score(
            student_id=1,
            grade=grade,
            subject=subject,
            quiz_id=actual_quiz_id,
            score=score,
            total=total,
            percentage=percentage,
            answers=answers
        )
    except Exception as e:
        app.logger.error(f"Failed to save quiz score: {e}")

    return jsonify({
        "score": score,
        "total": total,
        "percentage": percentage,
        "results": results
    })


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/robots.txt")
def robots_txt():
    base_url = request.url_root.rstrip("/")
    content = f"""User-agent: *
Allow: /
Disallow: /api/

User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Anthropic-AI
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Bytespider
Allow: /

User-agent: CCBot
Allow: /

User-agent: PerplexityBot
Allow: /

Sitemap: {base_url}/sitemap.xml
"""
    return Response(content, mimetype="text/plain")


@app.route("/sitemap.xml")
def sitemap_xml():
    base_url = request.url_root.rstrip("/")
    today = datetime.now().strftime("%Y-%m-%d")
    available_courses = get_available_courses()

    pages = []
    pages.append({"loc": f"{base_url}/", "priority": "1.0", "changefreq": "weekly"})
    pages.append({"loc": f"{base_url}/dashboard", "priority": "0.9", "changefreq": "weekly"})

    for grade_key in GRADE_LEVELS:
        pages.append({"loc": f"{base_url}/grade/{grade_key}", "priority": "0.8", "changefreq": "monthly"})

    for c in available_courses:
        pages.append({"loc": f"{base_url}/course/{c['grade']}/{c['subject']}", "priority": "0.7", "changefreq": "monthly"})
        course_data = load_course(c["grade"], c["subject"])
        if course_data:
            lessons, _ = get_all_lessons_for_course(c["grade"], c["subject"])
            for lesson in lessons:
                pages.append({"loc": f"{base_url}/lesson/{c['grade']}/{c['subject']}/{lesson['id']}", "priority": "0.6", "changefreq": "monthly"})
            if course_data.get("quiz_id"):
                pages.append({"loc": f"{base_url}/quiz/{c['grade']}/{c['subject']}", "priority": "0.5", "changefreq": "monthly"})

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for page in pages:
        xml += "  <url>\n"
        xml += f"    <loc>{page['loc']}</loc>\n"
        xml += f"    <lastmod>{today}</lastmod>\n"
        xml += f"    <changefreq>{page['changefreq']}</changefreq>\n"
        xml += f"    <priority>{page['priority']}</priority>\n"
        xml += "  </url>\n"
    xml += "</urlset>"

    response = make_response(xml)
    response.headers["Content-Type"] = "application/xml"
    return response


@app.route("/llms.txt")
def llms_txt():
    content = """# Standard Bearer Academy

## About
Standard Bearer Academy is a comprehensive K-12 homeschool learning management system (LMS) offering 115 courses across 10 subjects, all from a conservative, Judeo-Evangelical Christian, Creation-based (Young Earth/Biblical) worldview.

## Contact
- Email: boundlessvolumes@gmail.com
- Founded by: Mike Mallek

## Subjects (10 total)
- Science (PreK-12): Creation-based, Young Earth Creationist, Intelligent Design perspective
- Mathematics (PreK-12): Standard curriculum with Biblical stewardship applications
- Reading & Language Arts (PreK-12): Phonics-based, Biblical values, Christian literary analysis
- History & Social Studies (PreK-12): Providential history, Western Civilization, American Exceptionalism
- Bible & Scripture (PreK-12): Direct Scripture study, Old and New Testament, age-appropriate
- Civics & Government (PreK-12): Constitutional originalism, Biblical basis for government, limited government
- Art & Science Projects (PreK-8): Hands-on STEAM projects, experiments, crafts exploring God's creation
- Technology (6-12): Digital citizenship, programming, cybersecurity, AI, Biblical stewardship of tools
- Creative Writing (6-12): Fiction, poetry, nonfiction — writing as worship, storytelling to glorify God
- Life Skills (6-12): Financial literacy, home economics, career prep, independent living, Biblical stewardship

## Grade Levels
PreK, Kindergarten, 1st Grade through 12th Grade (15 levels total)

## Curriculum Stats
- 115 courses
- 905+ JSON lesson/quiz files
- 6 lessons per course plus a quiz
- Free and open during beta

## Lesson Formats
- Elementary (PreK-5): Memory verse, objective, content, hands-on activity, discussion questions
- Middle/High School (6-12): Scripture connection sidebar, detailed content sections, key concepts, reflection questions, primary sources (high school)

## Worldview
All content strictly adheres to:
- Politically conservative perspective
- Judeo-Evangelical Christian theology
- Young Earth Creationism (literal Genesis, 6-day creation, ~6,000-10,000 year old earth)
- Providential history (God's hand in human events)
- Constitutional originalism
- Biblical basis for ethics, government, and education

## Technology
- Built with Python/Flask
- PostgreSQL database for progress tracking
- JSON-based curriculum content
- Responsive web design
"""
    return Response(content, mimetype="text/plain")


@app.route("/llms-full.txt")
def llms_full_txt():
    base_url = request.url_root.rstrip("/")
    available_courses = get_available_courses()
    content = f"""# Standard Bearer Academy — Full Course Catalog

> url: {base_url}
> contact: boundlessvolumes@gmail.com
> founder: Mike Mallek

## Overview
115 courses across 10 subjects, PreK through 12th Grade.
All content from a conservative, Judeo-Evangelical Christian, Creation-based worldview.
Free to use during beta.

## Pages
- Homepage: {base_url}/
- Dashboard: {base_url}/dashboard
- Robots.txt: {base_url}/robots.txt
- Sitemap: {base_url}/sitemap.xml

## Grade Level Pages
"""
    for grade_key, grade_info in GRADE_LEVELS.items():
        content += f"- {grade_info['name']}: {base_url}/grade/{grade_key}\n"

    content += "\n## Complete Course Listing\n"
    current_grade = ""
    for c in sorted(available_courses, key=lambda x: (GRADE_LEVELS.get(x["grade"], {}).get("order", 99), x["subject"])):
        grade_name = GRADE_LEVELS.get(c["grade"], {}).get("name", c["grade"])
        if grade_name != current_grade:
            current_grade = grade_name
            content += f"\n### {current_grade}\n"
        subject_name = SUBJECTS.get(c["subject"], {}).get("name", c["subject"])
        content += f"- {subject_name}: {c['title']} ({base_url}/course/{c['grade']}/{c['subject']})\n"

    return Response(content, mimetype="text/plain")


if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)
