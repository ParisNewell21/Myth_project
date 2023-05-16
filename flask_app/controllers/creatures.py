from flask_app import app 
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.creature import Creature


###profile###
@app.route('/feed')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    all_creatures = Creature.get_all()
    user = User.get_by_id({"id":session['user_id']})
    return render_template("creature_feed.html",user=user, all_creatures = all_creatures)


@app.route('/creature/<int:id>')
def view_creature(id):
    if 'user_id' not in session:
        return redirect('/login')
    creature=Creature.get_all({'id': id})
    return render_template('myth_stories.html', creature=creature)
#############################################################################################


@app.route('/new/creature')
def new_creature():
    if 'user_id' not in session:
        return redirect('/logout')
    user = User.get_by_id({"id":session['user_id']})
    return render_template('add_creature.html', user=user )


@app.route('/add/creature', methods=["POST"])
def add():
    if not Creature.validate_creature(request.form):
        return redirect('/new/creature')
    data = {
        "creature_name": request.form['creature_name']
    }
    Creature.add_creature(data)
    print(request.form)
    return redirect('/feed')
###########################################################################


@app.route('/edit/<int:id>')
def edit_display(id):
    if 'user_id' not in session:
        return redirect('/logout')
    creature=creature.get_one({'id': id})
    user = User.get_by_id({"id":session['user_id']})
    return render_template('edit_creature.html', user=user, tvcreature=creature)


@app.route('/edit/process/<int:id>', methods=['POST'])
def process_edit(id):
    if 'user_id' not in session:
        return redirect('/login')
    if not Creature.validate_creature(request.form):
        return redirect(f'/edit/{id}')
    data = {
        'id': id,
        'creature_name': request.form['creature_name']
    }
    print(request.form)
    Creature.update_creature(data)
    return redirect('/dashboard')
###################################################################


@app.route('/creature/delete/<int:id>')
def delete(id):
    data={
        'id':id
    }
    Creature.delete(data)
    return redirect('/dashboard')