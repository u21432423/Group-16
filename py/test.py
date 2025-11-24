from flask import Flask, request, jsonify, render_template_string
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ====================== MODELS (MATCH YOUR SQL EXACTLY) ======================

class Municipality(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(50), nullable=False)

class WastePicker(db.Model):
    __tablename__ = 'waste_pickers'
    SAWPRS_id = db.Column(db.Integer, primary_key=True)
    registration_status = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserAuth(db.Model):
    __tablename__ = 'user_auth'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email_address = db.Column(db.String(100), nullable=False)  # Fixed length to 100
    waste_pickers_SAWPRS_id = db.Column(db.Integer, db.ForeignKey('waste_pickers.SAWPRS_id'))
    truck_drivers_id = db.Column(db.Integer, db.ForeignKey('truck_drivers.truck_drivers_id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TruckDriver(db.Model):
    __tablename__ = 'truck_drivers'
    truck_drivers_id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(40), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    truck_number_plate = db.Column(db.String(12))
    weight_kg = db.Column(db.Float)
    volume_cm3 = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class OperatingArea(db.Model):
    __tablename__ = 'operating_area'
    Area_id = db.Column(db.Integer, primary_key=True)
    municipality_id = db.Column(db.Integer, db.ForeignKey('municipality.id'))
    sorting_location = db.Column(db.String(40), nullable=False)
    waste_picker_SAWPRS_id = db.Column(db.Integer, db.ForeignKey('waste_pickers.SAWPRS_id'))
    truck_drivers_id = db.Column(db.Integer, db.ForeignKey('truck_drivers.truck_drivers_id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Create tables
with app.app_context():
    db.create_all()

# ====================== ROUTES ======================

# Home route (optional)
@app.route('/')
def home():
    return "Waste Management System API Running!"

# === WASTE PICKER REGISTRATION (wastepickers.html) ===
@app.route('/register/wastepicker', methods=['POST'])
def register_wastepicker():
    data = request.form

    # Create waste picker entry
    sawprs_id = data.get('sawprs-id')
    if sawprs_id:
        picker = WastePicker(SAWPRS_id=int(sawprs_id), registration_status=True)
        db.session.add(picker)
        db.session.commit()
    else:
        picker = WastePicker(registration_status=True)
        db.session.add(picker)
        db.session.commit()
        sawprs_id = picker.SAWPRS_id

    # Create user_auth entry
    user = UserAuth(
        name=data['name'],
        surname=data['surname'],
        email_address=data['email'],
        waste_pickers_SAWPRS_id=sawprs_id,
        truck_drivers_id=None
    )
    db.session.add(user)
    db.session.commit()

    return "<h2>Success! Waste Picker Registered.</h2><a href='wastepickers.html'>Go Back</a>"

# === TRUCK COMPANY REGISTRATION (collectiontrucks.html) ===
@app.route('/register/truckcompany', methods=['POST'])
def register_truckcompany():
    data = request.form

    company_name = data['companyName']
    email = data['emailAddress']
    location = data.get('locationSelect', 'Unknown Location')

    # Handle multiple trucks (even if only one is filled)
    plates = request.form.getlist('truckNumberPlate[]')
    weights = request.form.getlist('truckWeight[]')
    volumes = request.form.getlist('truckVolume[]')

    created_truck_ids = []

    for i in range(len(plates)):
        if not plates[i].strip():
            continue
        truck = TruckDriver(
            company_name=company_name,
            truck_number_plate=plates[i],
            weight_kg=float(weights[i]) if weights[i] else None,
            volume_cm3=float(volumes[i]) if volumes[i] else None,
            vehicle_id=1001  # placeholder
        )
        db.session.add(truck)
        db.session.commit()
        created_truck_ids.append(truck.truck_drivers_id)

    # Link to user_auth
    user = UserAuth(
        name=company_name,
        surname="Company",
        email_address=email,
        waste_pickers_SAWPRS_id=None,
        truck_drivers_id=created_truck_ids[0] if created_truck_ids else None
    )
    db.session.add(user)
    db.session.commit()

    # Optional: Save operating area
    if created_truck_ids:
        area = OperatingArea(
            municipality_id=10,
            sorting_location=location,
            waste_picker_SAWPRS_id=None,
            truck_drivers_id=created_truck_ids[0]
        )
        db.session.add(area)
        db.session.commit()

    return "<h2>Success! Truck Company & Trucks Registered.</h2><a href='collectiontrucks.html'>Go Back</a>"

# === KPI / Stats ===
@app.route('/api/stats')
def stats():
    return jsonify({
        "total_wastepickers": WastePicker.query.count(),
        "total_truck_companies": TruckDriver.query.distinct(TruckDriver.company_name).__len__(),
        "total_trucks": TruckDriver.query.count(),
        "total_users": UserAuth.query.count()
    })

# === Debug: See all data ===
@app.route('/debug')
def debug():
    html = "<h1>Database Contents</h1>"
    html += "<h2>User Auth</h2><pre>" + str([u.__dict__ for u in UserAuth.query.all()]) + "</pre>"
    html += "<h2>Trucks</h2><pre>" + str([t.__dict__ for t in TruckDriver.query.all()]) + "</pre>"
    html += "<h2>Waste Pickers</h2><pre>" + str([p.__dict__ for p in WastePicker.query.all()]) + "</pre>"
    return html

if __name__ == '__main__':
    app.run(debug=True, port=5000)