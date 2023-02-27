from flask import Blueprint, redirect, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Pressure, User
from . import db
import json


endpoints = Blueprint('endpoints', __name__)

# Endpoint to receive tire pressure data via HTTP POST
@endpoints.route('/pressure-data', methods=['POST'])
@login_required
def receive_pressure_data():
    data = request.get_json()
    if data:
        psi = data['psi']
        temperature = data['temperature']
        user_id = user_id=current_user.id

        # Create a new Pressure object with the provided data and the user_id
        new_pressure = Pressure(psi=psi, temperature=temperature, user_id=user_id)

        # Add the new Pressure object to the database session and commit the changes
        db.session.add(new_pressure)
        db.session.commit()

        return jsonify({'message': 'Pressure data saved successfully.'}), 201
    else:
        return jsonify({'message': 'No pressure data received.'})
