from flask import Flask, request, render_template_string, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ==================== MODELS ====================
# (Keep all your models exactly as before - they are correct)

class TruckDriver(db.Model):
    __tablename__ = 'truck_drivers'
    truck_drivers_id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(40), nullable=False)
    truck_number_plate = db.Column(db.String(12))
    weight_kg = db.Column(db.Float)
    volume_cm3 = db.Column(db.Float)

class WastePicker(db.Model):
    __tablename__ = 'waste_pickers'
    SAWPRS_id = db.Column(db.Integer, primary_key=True)

# Add other models if needed...

with app.app_context():
    db.create_all()

# ==================== LIVE STATS ====================
def get_live_stats():
    total_trucks = TruckDriver.query.count()
    total_companies = len({t.company_name for t in TruckDriver.query.all() if t.company_name})
    total_waste_kg = sum(t.weight_kg or 0 for t in TruckDriver.query.all())
    avg_load = round(total_waste_kg / total_trucks, 1) if total_trucks > 0 else 0
    total_pickers = WastePicker.query.count()
    updated = datetime.now().strftime("%d %B %Y at %H:%M")

    return {
        'total_trucks': total_trucks,
        'total_companies': total_companies,
        'total_waste_kg': f"{int(total_waste_kg):,} kg",
        'avg_per_truck': f"{avg_load} kg",
        'total_pickers': total_pickers,
        'updated': updated
    }

# ==================== STATIC FILES ====================
@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_file(f"html/css/{filename}")

@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_file(f"html/images/{filename}")

# ==================== HTML WITH STATS ====================
@app.route('/html/<filename>')
def serve_html_with_stats(filename):
    stats = get_live_stats()
    try:
        with open(f"html/{filename}", "r", encoding="utf-8") as f:
            content = f.read()

        replacements = {
            "{{total_trucks}}": str(stats['total_trucks']),
            "{{total_companies}}": str(stats['total_companies']),
            "{{total_waste_kg}}": stats['total_waste_kg'],
            "{{avg_per_truck}}": stats['avg_per_truck'],
            "{{total_pickers}}": str(stats['total_pickers']),
            "{{updated}}": stats['updated']
        }

        for key, val in replacements.items():
            content = content.replace(key, val)

        return render_template_string(content)
    except FileNotFoundError:
        return f"<h2>File html/{filename} not found!</h2>", 404

# ==================== REGISTRATION ROUTE ====================
@app.route('/register/truckcompany', methods=['POST'])
def register_truckcompany():
    # (Your existing working registration code)
    # Keep exactly as you had it - it works!
    return "<h2>Success! Registered.</h2><a href='/html/collectiontrucks.html'>Back</a>"

if __name__ == '__main__':
    app.run(debug=True, port=5000)