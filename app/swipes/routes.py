from flask import redirect, render_template, url_for
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField

from app import db
from app.models import Preference, Thing, User
from app.swipes import bp


class SwipeForm(FlaskForm):
    thing = StringField()
    value = SelectField('Like it?',
                        choices=[(-1, 'No'), (0, 'Neutral'), (1, 'Yes')])
    submit = SubmitField('Submit')


@bp.route('/')
@login_required
def home():
    return render_template('base.html')


@bp.route('/swipe', methods=['GET', 'POST'])
@login_required
def swipe():
    """A page for swiping things."""
    thing = (db.session.query(Thing).filter(~Thing.preferences.any(
        Preference.user_id.in_([current_user.id]))).first())
    if thing is None:
        return render_template('swipes/swiped_out.html')
    form = SwipeForm()
    form.thing.data = thing.id
    if form.validate_on_submit():
        pref = Preference(value=int(form.value.data),
                          thing_id=thing.id,
                          user_id=current_user.id)
        db.session.add(pref)
        db.session.commit()
        return redirect(url_for('swipes.swipe'))
    return render_template('swipes/swipe.html', form=form, thing=thing)


@bp.route('/matches/<int:userid>')
@login_required
def matches(userid):
    """A page for seeing matched things with another user."""
    things = Thing.query.filter(
        Thing.preferences.any(Preference.user_id == current_user.id),
        Thing.preferences.any(Preference.user_id == userid)).all()
    return render_template('swipes/matches.html',
                           things=things,
                           otheruser=User.query.get(userid),
                           currentuser=current_user)


@bp.route('/users')
@login_required
def users():
    """A page for seeing other users."""
    users = User.query.all()
    return render_template('swipes/users.html', users=users)
