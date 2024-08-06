from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User, Game
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

# Ruta para el login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('game.game_index'))
        else:
            flash('Credenciales incorrectas, por favor intente nuevamente.')
    return render_template('login.html')

# Ruta para el registro
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        is_admin = request.form.get('is_admin') == 'on'

        user = User.query.filter_by(username=username).first()

        if user:
            flash('El nombre de usuario ya existe.')
        else:
            new_user = User(username=username, password=generate_password_hash(password, method='sha256'), is_admin=is_admin)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('game.game_index'))
    return render_template('register.html')

# Ruta para cerrar sesión
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# Ruta para la administración de usuarios (solo para administradores)
@auth.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        return redirect(url_for('game.game_index'))
    
    users = User.query.all()
    return render_template('admin.html', users=users)

# Ruta para editar un usuario (solo para administradores)
@auth.route('/admin/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if not current_user.is_admin:
        return redirect(url_for('game.game_index'))
    
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        is_admin = request.form.get('is_admin') == 'on'

        user.username = username
        if password:
            user.password = generate_password_hash(password, method='sha256')
        user.is_admin = is_admin

        db.session.commit()
        return redirect(url_for('auth.admin'))
    
    return render_template('edit_user.html', user=user)

# Ruta para eliminar un usuario (solo para administradores, baja lógica)
@auth.route('/admin/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        return redirect(url_for('game.game_index'))
    
    user = User.query.get_or_404(user_id)
    user.is_active = False  # Baja lógica
    db.session.commit()
    
    return redirect(url_for('auth.admin'))
