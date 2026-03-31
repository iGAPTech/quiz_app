from flask import Blueprint, render_template, session, redirect, url_for,request
from config.db_config import get_db_connection
from datetime import datetime

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    user_id = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Total active quizzes
    cursor.execute("SELECT COUNT(*) AS total_quizzes FROM quizzes WHERE status='active'")
    total_quizzes = cursor.fetchone()['total_quizzes']

    # Total attempts by this student
    cursor.execute("SELECT COUNT(*) AS total_attempts FROM attempts WHERE user_id=%s", (user_id,))
    total_attempts = cursor.fetchone()['total_attempts']

    cursor.close()
    conn.close()

    return render_template(
        'user/dashboard.html',
        total_quizzes=total_quizzes,
        total_attempts=total_attempts,
        name=session.get('name')
    )


# =========================
# AVAILABLE QUIZZES
# =========================
@user.route('/quizzes')
def available_quizzes():
    if 'user_id' not in session or session['role'] != 'student':
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch only active quizzes with category
    cursor.execute("""
        SELECT q.*, c.name AS category_name
        FROM quizzes q
        JOIN categories c ON q.category_id = c.id
        WHERE q.status = 'active'
        ORDER BY q.id DESC
    """)

    quizzes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('user/quizzes.html', quizzes=quizzes)



# =========================
# START QUIZ
# =========================
@user.route('/start-quiz/<int:quiz_id>')
def start_quiz(quiz_id):
    if 'user_id' not in session or session['role'] != 'student':
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get quiz details
    cursor.execute("SELECT * FROM quizzes WHERE id=%s", (quiz_id,))
    quiz = cursor.fetchone()

    # Get questions
    cursor.execute("SELECT * FROM questions WHERE quiz_id=%s", (quiz_id,))
    questions = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'user/start_quiz.html',
        quiz=quiz,
        questions=questions
    )


# =========================
# SUBMIT QUIZ
# =========================
@user.route('/submit-quiz/<int:quiz_id>', methods=['POST'])
def submit_quiz(quiz_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get questions
    cursor.execute("SELECT id, correct_option FROM questions WHERE quiz_id=%s", (quiz_id,))
    questions = cursor.fetchall()

    score = 0

    for q in questions:
        qid = str(q['id'])
        selected = request.form.get(qid)

        if selected == q['correct_option']:
            score += 1

    total_questions = len(questions)

    # Save attempt
    cursor2 = conn.cursor()
    cursor2.execute("""
        INSERT INTO attempts (user_id, quiz_id, score, total_questions, attempted_on)
        VALUES (%s, %s, %s, %s, %s)
    """, (user_id, quiz_id, score, total_questions, datetime.now()))

    conn.commit()
    cursor.close()
    cursor2.close()
    conn.close()

    return render_template(
        'user/result.html',
        score=score,
        total=total_questions
    )


@user.route('/my-attempts')
def my_attempts():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            a.id,
            q.title,
            a.score,
            a.total_questions,
            a.attempted_on
        FROM attempts a
        JOIN quizzes q ON a.quiz_id = q.id
        WHERE a.user_id = %s
        ORDER BY a.attempted_on DESC
    """, (user_id,))

    attempts = cursor.fetchall()
    cursor.close()

    return render_template(
        'user/my_attempts.html',
        attempts=attempts
    )


@user.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/')

    user_id = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # User info
    cursor.execute("SELECT id, name, email, role, created_at FROM users WHERE id=%s", (user_id,))
    user_data = cursor.fetchone()

    # Stats
    cursor.execute("SELECT COUNT(*) AS total_attempts FROM attempts WHERE user_id=%s", (user_id,))
    total_attempts = cursor.fetchone()['total_attempts']

    cursor.execute("SELECT MAX(score) AS best_score FROM attempts WHERE user_id=%s", (user_id,))
    best_score = cursor.fetchone()['best_score']

    cursor.close()
    conn.close()

    return render_template(
        'user/profile.html',
        user=user_data,
        total_attempts=total_attempts,
        best_score=best_score
    )

@user.route('/leaderboard')
def user_leaderboard():
    if 'user_id' not in session:
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT 
            u.name,
            SUM(a.score) AS total_score,
            COUNT(a.id) AS total_attempts
        FROM attempts a
        JOIN users u ON u.id = a.user_id
        GROUP BY a.user_id
        ORDER BY total_score DESC
        LIMIT 10
    """
    cursor.execute(query)
    leaderboard = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'user/leaderboard.html',
        leaderboard=leaderboard
    )




