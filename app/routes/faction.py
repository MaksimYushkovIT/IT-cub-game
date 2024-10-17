from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models.factionM import Faction
from ..models.userM import User
from ..models.factionM import Rank
from ..extensions import db
from flask_login import login_required,current_user

faction_blueprint = Blueprint('faction', __name__)

@faction_blueprint.route('/factions')
def factions():
    factions = Faction.query.all()
    return render_template('factions/factions.html', factions=factions)

@faction_blueprint.route('/factions/top')
def top():
    factions = Faction.query.order_by(Faction.level.desc()).limit(10).all()
    top_members = User.query.order_by(User.level.desc()).limit(10).all()
    return render_template('factions/top.html', factions=factions, top_members=top_members)

@faction_blueprint.route('/factions/<int:faction_id>')
def faction(faction_id):
    faction = Faction.query.get_or_404(faction_id)
    users = faction.users  # This will get all users in the faction
    leader = User.query.get(faction.leader_id)
    hands = User.query.filter(User.factions.any(Faction.id == faction_id), User.position == 'руки').all()
    members = User.query.filter(User.factions.any(Faction.id == faction_id)).order_by(User.level.desc()).limit(10).all()
    return render_template('factions/faction.html', faction=faction, leader=leader, hands=hands, members=members, users=users)

@faction_blueprint.route('/factions/<int:faction_id>/leader')
def faction_leader(faction_id):
    faction = Faction.query.get_or_404(faction_id)
    leader = User.query.get(faction.leader_id)
    return render_template('factions/faction_leader.html', faction=faction, leader=leader)

@faction_blueprint.route('/factions/<int:faction_id>/appoint_leader', methods=['POST'])
def appoint_faction_leader(faction_id):
    faction = Faction.query.get_or_404(faction_id)
    leader_id = request.form['leader_id']
    leader = User.query.get(leader_id)
    faction.leader_id = leader_id
    db.session.commit()
    return redirect(url_for('faction.faction', faction_id=faction_id))

@faction_blueprint.route('/factions/<int:faction_id>/hands')
def faction_hands(faction_id):
    faction = Faction.query.get_or_404(faction_id)
    hands = User.query.filter(User.factions.any(Faction.id == faction_id), User.position == 'руки').all()
    return render_template('factions/faction_hands.html', faction=faction, hands=hands)

@faction_blueprint.route('/factions/<int:faction_id>/appoint_hands', methods=['POST'])
def appoint_faction_hands(faction_id):
    faction = Faction.query.get_or_404(faction_id)
    hands_id = request.form['hands_id']
    hands = User.query.get(hands_id)
    hands.position = 'руки'
    db.session.commit()
    return redirect(url_for('faction.faction', faction_id=faction_id))

@faction_blueprint.route('/users/<int:user_id>/factions')
def user_factions(user_id):
    user = User.query.get_or_404(user_id)
    factions = user.factions.all()
    return render_template('factions/user_factions.html', user=user, factions=factions)

@faction_blueprint.route('/users/<int:user_id>/join_faction', methods=['POST'])
def join_faction(user_id):
    user = User.query.get_or_404(user_id)
    faction_id = request.form['faction_id']
    faction = Faction.query.get(faction_id)
    user.factions.append(faction)
    db.session.commit()
    return redirect(url_for('faction.user_factions', user_id=user_id))

@faction_blueprint.route('/users/<int:user_id>/leave_faction', methods=['POST'])
def leave_faction(user_id):
    user = User.query.get_or_404(user_id)
    faction_id = request.form['faction_id']
    faction = Faction.query.get(faction_id)
    user.factions.remove(faction)
    db.session.commit()
    return redirect(url_for('faction.user_factions', user_id=user_id))

@faction_blueprint.route('/factions/<int:faction_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_faction(faction_id):
    if not current_user.is_admin:
        return 'У вас нет доступа к этой странице.'
    teachers = User.query.filter(User.is_teacher == True).all()
    faction = Faction.query.get(faction_id)
    users = User.query.join(User.user_factions).filter(User.user_factions.c.faction_id == faction_id).all()
    ranks = Rank.query.filter(Rank.faction_id == faction_id).all()
    if request.method == 'POST':
        faction.name = request.form['name']
        faction.description = request.form['description']
        leader_id = request.form.get('leader')
        if leader_id:
            faction.leader_id = leader_id
        else:
            flash('Выберите лидера', 'error')
            return redirect(url_for('faction.edit_faction', faction_id=faction.id))
        faction.rank_ids = [int(rank_id) for rank_id in request.form.getlist('rank_')]
        new_rank_name = request.form['new_rank']
        if new_rank_name:
            new_rank = Rank(name=new_rank_name, faction_id=faction.id)
            db.session.add(new_rank)
            db.session.commit()
        db.session.commit()
        return redirect(url_for('faction.faction', faction_id=faction_id))
    return render_template('factions/edit_faction.html', faction=faction, users=users, ranks=ranks)