import os
import logging
import psycopg2
from psycopg2.extras import RealDictCursor, Json

logger = logging.getLogger(__name__)


def get_db():
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        pghost = os.environ.get("PGHOST")
        pgport = os.environ.get("PGPORT", "5432")
        pguser = os.environ.get("PGUSER")
        pgpassword = os.environ.get("PGPASSWORD")
        pgdatabase = os.environ.get("PGDATABASE")
        if pghost and pguser and pgdatabase:
            database_url = f"postgresql://{pguser}:{pgpassword}@{pghost}:{pgport}/{pgdatabase}"
        else:
            raise ConnectionError("No database connection info available")
    return psycopg2.connect(database_url, cursor_factory=RealDictCursor)


def init_db():
    try:
        conn = get_db()
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    display_name VARCHAR(200),
                    role VARCHAR(50) DEFAULT 'student',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                CREATE TABLE IF NOT EXISTS completed_lessons (
                    id SERIAL PRIMARY KEY,
                    student_id INTEGER REFERENCES students(id),
                    grade VARCHAR(50) NOT NULL,
                    subject VARCHAR(50) NOT NULL,
                    unit VARCHAR(50),
                    lesson_id VARCHAR(100) NOT NULL,
                    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(student_id, grade, subject, lesson_id)
                );
                CREATE TABLE IF NOT EXISTS quiz_scores (
                    id SERIAL PRIMARY KEY,
                    student_id INTEGER REFERENCES students(id),
                    grade VARCHAR(50) NOT NULL,
                    subject VARCHAR(50) NOT NULL,
                    unit VARCHAR(50),
                    quiz_id VARCHAR(100) NOT NULL,
                    score INTEGER NOT NULL,
                    total INTEGER NOT NULL,
                    percentage INTEGER NOT NULL,
                    answers JSONB,
                    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                INSERT INTO students (id, username, display_name, role)
                VALUES (1, 'default', 'Default Student', 'student')
                ON CONFLICT (id) DO NOTHING;
            """)
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.warning(f"Database initialization skipped: {e}")


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
