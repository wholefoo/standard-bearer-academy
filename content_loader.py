import json
import os

LESSONS_DIR = os.path.join(os.path.dirname(__file__), "lessons")

SUBJECT_MAP = {
    "civics": {"name": "Civics & Government", "icon": "🏛️"},
}


def load_course(grade, subject):
    course_path = os.path.join(LESSONS_DIR, grade, subject, "course.json")
    if not os.path.exists(course_path):
        return None
    with open(course_path, "r") as f:
        return json.load(f)


def load_lesson(grade, subject, lesson_id):
    lesson_path = os.path.join(LESSONS_DIR, grade, subject, f"{lesson_id}.json")
    if not os.path.exists(lesson_path):
        return None
    with open(lesson_path, "r") as f:
        return json.load(f)


def load_quiz(grade, subject, quiz_id):
    quiz_path = os.path.join(LESSONS_DIR, grade, subject, f"{quiz_id}.json")
    if not os.path.exists(quiz_path):
        return None
    with open(quiz_path, "r") as f:
        return json.load(f)


def get_all_lessons_for_course(grade, subject):
    course = load_course(grade, subject)
    if not course:
        return [], None
    lessons = []
    for unit in course.get("units", []):
        for lesson_id in unit.get("lessons", []):
            lesson = load_lesson(grade, subject, lesson_id)
            if lesson:
                lesson["unit_id"] = unit["id"]
                lesson["unit_title"] = unit["title"]
                lessons.append(lesson)
    return lessons, course


def get_lesson_navigation(grade, subject, lesson_id):
    lessons, course = get_all_lessons_for_course(grade, subject)
    if not lessons:
        return None, None, None
    current = None
    prev_lesson = None
    next_lesson = None
    for i, lesson in enumerate(lessons):
        if lesson["id"] == lesson_id:
            current = lesson
            if i > 0:
                prev_lesson = lessons[i - 1]
            if i < len(lessons) - 1:
                next_lesson = lessons[i + 1]
            break
    return prev_lesson, current, next_lesson


def get_available_courses():
    courses = []
    if not os.path.exists(LESSONS_DIR):
        return courses
    for grade_dir in sorted(os.listdir(LESSONS_DIR)):
        grade_path = os.path.join(LESSONS_DIR, grade_dir)
        if not os.path.isdir(grade_path):
            continue
        for subject_dir in sorted(os.listdir(grade_path)):
            subject_path = os.path.join(grade_path, subject_dir)
            course_file = os.path.join(subject_path, "course.json")
            if os.path.isdir(subject_path) and os.path.exists(course_file):
                course = load_course(grade_dir, subject_dir)
                if course:
                    courses.append({
                        "grade": grade_dir,
                        "subject": subject_dir,
                        "title": course.get("title", ""),
                        "description": course.get("description", ""),
                    })
    return courses
