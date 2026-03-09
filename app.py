from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
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
}

USER_ROLES = {
    "parent": {"name": "Parent / Teacher", "description": "Assign Lessons, Grade Essays, View Student Progress, Set Rewards."},
    "teacher": {"name": "Teacher", "description": "Create lessons, grade assignments, and track student progress"},
    "student": {"name": "Student", "description": "Access lessons, complete quizzes, and track your learning"},
}


def get_subject_info(subject):
    return SUBJECTS.get(subject, {"name": subject.title(), "icon": "📚"})


@app.route("/")
def homepage():
    available_courses = get_available_courses()
    return render_template("index.html", roles=USER_ROLES, grades=GRADE_LEVELS,
                           subjects=SUBJECTS, available_courses=available_courses)


@app.route("/dashboard")
def dashboard():
    role = request.args.get("role", "parent")
    if role not in USER_ROLES:
        role = "parent"
    available_courses = get_available_courses()
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


if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)
