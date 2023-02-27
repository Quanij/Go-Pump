from flask import Blueprint, redirect, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Pressure, User
from . import db
import json


views = Blueprint('views', __name__)


@views.route('/my-tire', methods=['GET', 'POST'])
@login_required
def my_tire():
    # Get all the pressure data from the database
    data = Pressure.query.filter_by(user_id=current_user.id).all()
    return render_template('my_tire.html', data=data, user=current_user)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)


@views.route('/about-us', methods=['GET', 'POST'])
def about_us():
    return render_template("about_us.html", user=current_user)

