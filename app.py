from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'    # Makes project.db in your folder
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class WastePicker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    location = db.Column(db.String(120))

class Truck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    license_plate = db.Column(db.String(20))
    driver_name = db.Column(db.String(80))

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))

class Pickup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wastepicker_id = db.Column(db.Integer, db.ForeignKey('waste_picker.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    date = db.Column(db.String(50))
    volume = db.Column(db.Float)

with app.app_context():
    db.create_all()

# Create a waste picker (POST)
@app.route('/api/wastepickers', methods=['POST'])
def add_wastepicker():
    data = request.json
    picker = WastePicker(name=data['name'], location=data['location'])
    db.session.add(picker)
    db.session.commit()
    return jsonify({'id': picker.id, 'name': picker.name, 'location': picker.location}), 201

# Read all waste pickers (GET)
@app.route('/api/wastepickers', methods=['GET'])
def get_wastepickers():
    pickers = WastePicker.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'location': p.location} for p in pickers])

# Update a waste picker (PUT)
@app.route('/api/wastepickers/<int:picker_id>', methods=['PUT'])
def update_wastepicker(picker_id):
    picker = WastePicker.query.get(picker_id)
    if not picker:
        return jsonify({'error': 'Not found'}), 404
    data = request.json
    picker.name = data.get('name', picker.name)
    picker.location = data.get('location', picker.location)
    db.session.commit()
    return jsonify({'id': picker.id, 'name': picker.name, 'location': picker.location})

# Create a truck (POST)
@app.route('/api/trucks', methods=['POST'])
def add_truck():
    data = request.json
    truck = Truck(license_plate=data['license_plate'], driver_name=data['driver_name'])
    db.session.add(truck)
    db.session.commit()
    return jsonify({'id': truck.id, 'license_plate': truck.license_plate, 'driver_name': truck.driver_name}), 201

# Read all trucks (GET)
@app.route('/api/trucks', methods=['GET'])
def get_trucks():
    trucks = Truck.query.all()
    return jsonify([{'id': t.id, 'license_plate': t.license_plate, 'driver_name': t.driver_name} for t in trucks])

# Update a truck (PUT)
@app.route('/api/trucks/<int:truck_id>', methods=['PUT'])
def update_truck(truck_id):
    truck = Truck.query.get(truck_id)
    if not truck:
        return jsonify({'error': 'Not found'}), 404
    data = request.json
    truck.license_plate = data.get('license_plate', truck.license_plate)
    truck.driver_name = data.get('driver_name', truck.driver_name)
    db.session.commit()
    return jsonify({'id': truck.id, 'license_plate': truck.license_plate, 'driver_name': truck.driver_name})


# Create a location (POST)
@app.route('/api/locations', methods=['POST'])
def add_location():
    data = request.json
    loc = Location(name=data['name'], address=data['address'])
    db.session.add(loc)
    db.session.commit()
    return jsonify({'id': loc.id, 'name': loc.name, 'address': loc.address}), 201

# Read all locations (GET)
@app.route('/api/locations', methods=['GET'])
def get_locations():
    locations = Location.query.all()
    return jsonify([{'id': l.id, 'name': l.name, 'address': l.address} for l in locations])

# Update a location (PUT)
@app.route('/api/locations/<int:loc_id>', methods=['PUT'])
def update_location(loc_id):
    loc = Location.query.get(loc_id)
    if not loc:
        return jsonify({'error': 'Not found'}), 404
    data = request.json
    loc.name = data.get('name', loc.name)
    loc.address = data.get('address', loc.address)
    db.session.commit()
    return jsonify({'id': loc.id, 'name': loc.name, 'address': loc.address})

# Create a pickup (POST)
@app.route('/api/pickups', methods=['POST'])
def add_pickup():
    data = request.json
    pickup = Pickup(
        wastepicker_id=data['wastepicker_id'],
        location_id=data['location_id'],
        date=data['date'],
        volume=data['volume']
    )
    db.session.add(pickup)
    db.session.commit()
    return jsonify({
        'id': pickup.id,
        'wastepicker_id': pickup.wastepicker_id,
        'location_id': pickup.location_id,
        'date': pickup.date,
        'volume': pickup.volume
    }), 201

# Read all pickups (GET)
@app.route('/api/pickups', methods=['GET'])
def get_pickups():
    pickups = Pickup.query.all()
    return jsonify([{
        'id': p.id,
        'wastepicker_id': p.wastepicker_id,
        'location_id': p.location_id,
        'date': p.date,
        'volume': p.volume
    } for p in pickups])

# Update a pickup (PUT)
@app.route('/api/pickups/<int:pickup_id>', methods=['PUT'])
def update_pickup(pickup_id):
    pickup = Pickup.query.get(pickup_id)
    if not pickup:
        return jsonify({'error': 'Not found'}), 404
    data = request.json
    pickup.wastepicker_id = data.get('wastepicker_id', pickup.wastepicker_id)
    pickup.location_id = data.get('location_id', pickup.location_id)
    pickup.date = data.get('date', pickup.date)
    pickup.volume = data.get('volume', pickup.volume)
    db.session.commit()
    return jsonify({
        'id': pickup.id,
        'wastepicker_id': pickup.wastepicker_id,
        'location_id': pickup.location_id,
        'date': pickup.date,
        'volume': pickup.volume
    })

@app.route('/api/kpi', methods=['GET'])
def get_kpi():
    wastepickers = WastePicker.query.count()
    trucks = Truck.query.count()
    locations = Location.query.count()
    pickups = Pickup.query.count()
    return jsonify({
        'total_wastepickers': wastepickers,
        'total_trucks': trucks,
        'total_locations': locations,
        'total_pickups': pickups
    })

if __name__ == "__main__":
    app.run(debug=True)
