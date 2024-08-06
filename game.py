from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models import Game, User  # Asegúrate de que app esté en el PYTHONPATH
from app import create_app, db  # Importa db desde app
import random
import json
import sys
import os

# Ajusta el PYTHONPATH si es necesario
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

app = create_app()
game = Blueprint('game', __name__)

# Valores de los maletines
case_values = [
    0.01, 1, 5, 10, 25, 50, 75, 100, 200, 300, 400, 500, 750,
    1000, 5000, 10000, 25000, 50000, 75000, 100000, 200000,
    300000, 400000, 500000, 750000, 1000000
]

@game.route('/game')
@login_required
def game_index():
    games = Game.query.filter_by(user_id=current_user.id).all()
    return render_template('game.html', games=games)

@game.route('/game/new', methods=['POST'])
@login_required
def new_game():
    cases = random.sample(case_values, len(case_values))
    new_game = Game(user_id=current_user.id, cases=json.dumps(cases))
    db.session.add(new_game)
    db.session.commit()
    return redirect(url_for('game.game_view', game_id=new_game.id))

@game.route('/game/<int:game_id>')
@login_required
def game_view(game_id):
    game = Game.query.get_or_404(game_id)
    if game.user_id != current_user.id and not current_user.is_admin:
        return redirect(url_for('game.game_index'))
    return render_template('game_view.html', game=game.to_dict())

@game.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        return redirect(url_for('game.game_index'))
    users = User.query.all()
    return render_template('admin.html', users=users)

@game.route('/admin/delete/<int:user_id>')
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        return redirect(url_for('game.game_index'))
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('game.admin'))

@game.route('/game/select_case/<int:game_id>', methods=['POST'])
@login_required
def select_initial_case(game_id):
    game = Game.query.get_or_404(game_id)
    if game.user_id != current_user.id:
        return redirect(url_for('game.game_index'))
    
    initial_case = request.form.get('initial_case')
    if initial_case:
        game.initial_case = int(initial_case)
        game.status = 'In Progress'
        db.session.commit()
    return redirect(url_for('game.game_view', game_id=game.id))

@game.route('/game/reveal_case/<int:game_id>', methods=['POST'])
@login_required
def reveal_case(game_id):
    game = Game.query.get_or_404(game_id)
    if game.user_id != current_user.id:
        return redirect(url_for('game.game_index'))
    
    case_to_reveal = request.form.get('case_to_reveal')
    if case_to_reveal:
        revealed_cases = json.loads(game.revealed_cases)
        revealed_cases.append(int(case_to_reveal))
        game.revealed_cases = json.dumps(revealed_cases)
        db.session.commit()
    
    return redirect(url_for('game.game_view', game_id=game.id))

@game.route('/game/banker_offer/<int:game_id>', methods=['POST'])
@login_required
def banker_offer(game_id):
    game = Game.query.get_or_404(game_id)
    if game.user_id != current_user.id:
        return redirect(url_for('game.game_index'))
    
    offer = request.form.get('offer')
    if offer:
        offers = json.loads(game.offers)
        offers.append(float(offer))
        game.offers = json.dumps(offers)
        db.session.commit()
    
    return redirect(url_for('game.game_view', game_id=game.id))

@game.route('/game/accept_offer/<int:game_id>', methods=['POST'])
@login_required
def accept_offer(game_id):
    game = Game.query.get_or_404(game_id)
    if game.user_id != current_user.id:
        return redirect(url_for('game.game_index'))
    
    final_offer = request.form.get('final_offer')
    if final_offer:
        game.final_offer = float(final_offer)
        game.status = 'Completed'
        db.session.commit()
    
    return redirect(url_for('game.game_view', game_id=game.id))

@game.route('/game/switch_case/<int:game_id>', methods=['POST'])
@login_required
def switch_case(game_id):
    game = Game.query.get_or_404(game_id)
    if game.user_id != current_user.id:
        return redirect(url_for('game.game_index'))
    
    switch = request.form.get('switch')
    if switch and switch.lower() == 'yes':
        game.initial_case = int(request.form.get('new_case'))
        db.session.commit()
    
    return redirect(url_for('game.game_view', game_id=game.id))
