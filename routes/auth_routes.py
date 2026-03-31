from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from config.db_config import get_db_connection
import random
from flask_mail import Message
from extensions import mail

auth = Blueprint('auth', __name__)

# ================= LOGIN =================
@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user and user['password'] == password:

            # 🔹 Generate OTP
            otp = str(random.randint(100000, 999999))

            print("OTP : "+ otp)

            # Store in session
            session['temp_user'] = user
            session['otp'] = otp

            # 🔹 Send Email
            msg = Message(
                subject='Your OTP - Quiz System',
                sender='quizwebsite2026@gmail.com',
                recipients=[email]
            )
            msg.body = f"Your OTP is: {otp}"

            mail.send(msg)

            flash("OTP sent to your email!", "success")
            return redirect(url_for('auth.verify_otp'))

        flash("Invalid Email or Password!", "danger")

    return render_template('auth/login.html')


# ================= VERIFY OTP =================
@auth.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():

    if request.method == 'POST':
        user_otp = request.form['otp']
        session_otp = session.get('otp')

        if user_otp == session_otp:

            user = session.get('temp_user')

            # Final login
            session['user_id'] = user['id']
            session['name'] = user['name']
            session['role'] = user['role']

            # Clear temp data
            session.pop('otp', None)
            session.pop('temp_user', None)

            flash("Login Successful!", "success")

            if user['role'] == 'admin':
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('user.dashboard'))

        flash("Invalid OTP!", "danger")

    return render_template('auth/verify_otp.html')


# ================= LOGOUT =================
@auth.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!", "info")
    return redirect(url_for('auth.login'))