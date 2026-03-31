from flask import Blueprint, render_template, session, redirect, url_for,request
from config.db_config import get_db_connection

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/dashboard')
def dashboard():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('auth.login'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Total Students (users with role student)
    cursor.execute("SELECT COUNT(*) AS total FROM users WHERE role='student'")
    total_students = cursor.fetchone()['total']

    # Total Quizzes
    cursor.execute("SELECT COUNT(*) AS total FROM quizzes")
    total_quizzes = cursor.fetchone()['total']

    # Total Questions
    cursor.execute("SELECT COUNT(*) AS total FROM questions")
    total_questions = cursor.fetchone()['total']

    # Total Attempts
    cursor.execute("SELECT COUNT(*) AS total FROM attempts")
    total_attempts = cursor.fetchone()['total']

    # Average Score
    cursor.execute("SELECT AVG(score) AS avg_score FROM attempts")
    avg_result = cursor.fetchone()
    avg_score = avg_result['avg_score'] if avg_result['avg_score'] else 0

    # Recent Attempts
    cursor.execute("""
        SELECT u.name, q.title, a.score, a.attempted_on
        FROM attempts a
        JOIN users u ON u.id = a.user_id
        JOIN quizzes q ON q.id = a.quiz_id
        ORDER BY a.attempted_on DESC
        LIMIT 5
    """)
    recent_attempts = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'admin/dashboard.html',
        total_students=total_students,
        total_quizzes=total_quizzes,
        total_questions=total_questions,
        total_attempts=total_attempts,
        avg_score=round(avg_score, 2),
        recent_attempts=recent_attempts
    )


    # return render_template('admin/dashboard.html', name=session['name'])

@admin.route('/users')
def users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users ORDER BY id DESC")
    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('admin/users.html', users=users)

# =========================
# ADD USER
# =========================
@admin.route('/users/add', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    role = request.form['role']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (name, email, password, role)
        VALUES (%s, %s, %s, %s)
    """, (name, email, password, role))

    print(name, email, password, role)

    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/admin/users')


# =========================
# UPDATE USER
# =========================
@admin.route('/users/update/<int:id>', methods=['POST'])
def update_user(id):
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    role = request.form['role']

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        UPDATE users
        SET name=%s, email=%s, password=%s, role=%s
        WHERE id=%s
    """

    values = (name, email, password, role, id)

    print("Updating:", values)

    cursor.execute(query, values)
    conn.commit()

    print("Rows affected:", cursor.rowcount)

    cursor.close()
    conn.close()

    return redirect('/admin/users')



# =========================
# DELETE USER
# =========================
@admin.route('/users/delete/<int:id>')
def delete_user(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id=%s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/admin/users')


@admin.route('/categories')
def categories():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM categories ORDER BY id DESC")
    categories = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('admin/categories.html', categories=categories)


@admin.route('/categories/add', methods=['POST'])
def add_category():
    name = request.form['name']
    status = request.form['status']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO categories (name, status)
        VALUES (%s, %s)
    """, (name, status))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/admin/categories')


@admin.route('/categories/update/<int:id>', methods=['POST'])
def update_category(id):
    name = request.form['name']
    status = request.form['status']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE categories
        SET name=%s, status=%s
        WHERE id=%s
    """, (name, status, id))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/admin/categories')


@admin.route('/categories/delete/<int:id>')
def delete_category(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM categories WHERE id=%s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/admin/categories')


# =========================
# QUIZZES LIST
# =========================
@admin.route('/quizzes')
def quizzes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT quizzes.*, categories.name AS category_name
        FROM quizzes
        LEFT JOIN categories ON quizzes.category_id = categories.id
        ORDER BY quizzes.id DESC
    """)
    quizzes = cursor.fetchall()

    cursor.execute("SELECT * FROM categories WHERE status='active'")
    categories = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('admin/quizzes.html',
                           quizzes=quizzes,
                           categories=categories)


# ADD QUIZ
@admin.route('/quizzes/add', methods=['POST'])
def add_quiz():
    category_id = request.form['category_id']
    title = request.form['title']
    time_limit = request.form['time_limit']
    total_marks = request.form['total_marks']
    status = request.form['status']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO quizzes (category_id, title, time_limit, total_marks, status)
        VALUES (%s, %s, %s, %s, %s)
    """, (category_id, title, time_limit, total_marks, status))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/admin/quizzes')


# UPDATE QUIZ
@admin.route('/quizzes/update/<int:id>', methods=['POST'])
def update_quiz(id):
    category_id = request.form['category_id']
    title = request.form['title']
    time_limit = request.form['time_limit']
    total_marks = request.form['total_marks']
    status = request.form['status']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE quizzes
        SET category_id=%s, title=%s, time_limit=%s,
            total_marks=%s, status=%s
        WHERE id=%s
    """, (category_id, title, time_limit, total_marks, status, id))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/admin/quizzes')


# DELETE QUIZ
@admin.route('/quizzes/delete/<int:id>')
def delete_quiz(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM quizzes WHERE id=%s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/admin/quizzes')


# Questions Module

@admin.route('/questions/<int:quiz_id>')
def questions(quiz_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Quiz info
    cursor.execute("SELECT * FROM quizzes WHERE id=%s", (quiz_id,))
    quiz = cursor.fetchone()

    # Questions of this quiz
    cursor.execute("""
        SELECT * FROM questions
        WHERE quiz_id=%s
        ORDER BY id DESC
    """, (quiz_id,))
    questions = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'admin/questions.html',
        questions=questions,
        quiz=quiz
    )

# Add

@admin.route('/questions/add/<int:quiz_id>', methods=['POST'])
def add_question(quiz_id):
    question_text = request.form['question_text']
    option_a = request.form['option_a']
    option_b = request.form['option_b']
    option_c = request.form['option_c']
    option_d = request.form['option_d']
    correct_option = request.form['correct_option']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO questions
        (quiz_id, question_text, option_a, option_b, option_c, option_d, correct_option)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (
        quiz_id,
        question_text,
        option_a,
        option_b,
        option_c,
        option_d,
        correct_option
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(f'/admin/questions/{quiz_id}')


# update

@admin.route('/questions/update/<int:id>/<int:quiz_id>', methods=['POST'])
def update_question(id, quiz_id):
    question_text = request.form['question_text']
    option_a = request.form['option_a']
    option_b = request.form['option_b']
    option_c = request.form['option_c']
    option_d = request.form['option_d']
    correct_option = request.form['correct_option']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE questions
        SET question_text=%s,
            option_a=%s,
            option_b=%s,
            option_c=%s,
            option_d=%s,
            correct_option=%s
        WHERE id=%s
    """, (
        question_text,
        option_a,
        option_b,
        option_c,
        option_d,
        correct_option,
        id
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(f'/admin/questions/{quiz_id}')


@admin.route('/questions/delete/<int:id>/<int:quiz_id>')
def delete_question(id, quiz_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM questions WHERE id=%s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(f'/admin/questions/{quiz_id}')

@admin.route('/leaderboard/<int:quiz_id>')
def leaderboard(quiz_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Quiz Info
    cursor.execute("SELECT * FROM quizzes WHERE id=%s", (quiz_id,))
    quiz = cursor.fetchone()

    # Top 5 (Highest Score per student)
    query = """
        SELECT 
    u.name,
    MAX(a.score) AS highest_score,
    MAX(a.total_questions) AS total_questions,
    (MAX(a.score) / MAX(a.total_questions)) * 100 AS percentage
    FROM attempts a
    JOIN users u ON u.id = a.user_id
    WHERE a.quiz_id = %s
    GROUP BY a.user_id, u.name
    ORDER BY percentage DESC
    LIMIT 5;
    """
    cursor.execute(query, (quiz_id,))
    leaderboard = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'admin/leaderboard.html',
        quiz=quiz,
        leaderboard=leaderboard
    )



@admin.route('/attempts')
def admin_attempts():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT 
            a.id,
            u.name AS student_name,
            q.title AS quiz_title,
            a.score,
            a.total_questions,
            a.attempted_on
        FROM attempts a
        JOIN users u ON a.user_id = u.id
        JOIN quizzes q ON a.quiz_id = q.id
        ORDER BY a.attempted_on DESC
    """
    cursor.execute(query)
    attempts = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('admin/attempts.html', attempts=attempts)


@admin.route('/results')
def admin_results():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT 
            q.id AS quiz_id,
            q.title,
            u.name,
            MAX(a.score) AS highest_score
        FROM attempts a
        JOIN users u ON a.user_id = u.id
        JOIN quizzes q ON a.quiz_id = q.id
        GROUP BY a.user_id, a.quiz_id
        ORDER BY q.id, highest_score DESC
    """

    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('admin/results.html', results=results)


@admin.route('/reports')
def admin_reports():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Total students
    cursor.execute("SELECT COUNT(*) AS total_students FROM users WHERE role='student'")
    total_students = cursor.fetchone()['total_students']

    # Total quizzes
    cursor.execute("SELECT COUNT(*) AS total_quizzes FROM quizzes")
    total_quizzes = cursor.fetchone()['total_quizzes']

    # Total attempts
    cursor.execute("SELECT COUNT(*) AS total_attempts FROM attempts")
    total_attempts = cursor.fetchone()['total_attempts']

    cursor.close()
    conn.close()

    return render_template(
        'admin/reports.html',
        total_students=total_students,
        total_quizzes=total_quizzes,
        total_attempts=total_attempts
    )



