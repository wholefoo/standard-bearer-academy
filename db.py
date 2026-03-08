import os
import psycopg2
from psycopg2.extras import RealDictCursor, Json


def get_db():
    return psycopg2.connect(os.environ["DATABASE_URL"], cursor_factory=RealDictCursor)


def record_completed_lesson(student_id, grade, subject, lesson_id, unit=None):
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO completed_lessons (student_id, grade, subject, unit, lesson_id)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (student_id, grade, subject, lesson_id) DO NOTHING
            """, (student_id, grade, subject, unit, lesson_id))
        conn.commit()
    finally:
        conn.close()


def record_quiz_score(student_id, grade, subject, quiz_id, score, total, percentage, answers=None, unit=None):
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO quiz_scores (student_id, grade, subject, unit, quiz_id, score, total, percentage, answers)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (student_id, grade, subject, unit, quiz_id, score, total, percentage,
                  Json(answers) if answers else None))
        conn.commit()
    finally:
        conn.close()


def get_student_progress(student_id, grade=None, subject=None):
    conn = get_db()
    try:
        with conn.cursor() as cur:
            query = "SELECT * FROM completed_lessons WHERE student_id = %s"
            params = [student_id]
            if grade:
                query += " AND grade = %s"
                params.append(grade)
            if subject:
                query += " AND subject = %s"
                params.append(subject)
            query += " ORDER BY completed_at DESC"
            cur.execute(query, params)
            return cur.fetchall()
    finally:
        conn.close()


def get_quiz_history(student_id, grade=None, subject=None):
    conn = get_db()
    try:
        with conn.cursor() as cur:
            query = "SELECT * FROM quiz_scores WHERE student_id = %s"
            params = [student_id]
            if grade:
                query += " AND grade = %s"
                params.append(grade)
            if subject:
                query += " AND subject = %s"
                params.append(subject)
            query += " ORDER BY completed_at DESC"
            cur.execute(query, params)
            return cur.fetchall()
    finally:
        conn.close()
