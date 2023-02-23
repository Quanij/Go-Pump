from flask import Blueprint, redirect, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Pressure, User
from . import db
import json


views = Blueprint('views', __name__)


@views.route('/my-tire', methods=['GET', 'POST'])
@login_required
def my_tire():
    if request.method == 'POST':
        psi =  request.form.get('psi')
        temperature = request.form.get('temperature')
        
        if psi < 0:
            flash('Pressure Cannot Be Negative', category='error')
        else:
            new_pressure = Pressure(psi=psi, temperture=temperature, user_id=current_user.id)
            db.session.add(new_pressure)
            db.session.commit()
            flash('Tire Pressure Added!', category='success')
    
    return render_template("my_tire.html", user=current_user)


@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)


@views.route('/about-us', methods=['GET', 'POST'])
def about_us():
    return render_template("about_us.html", user=current_user)

