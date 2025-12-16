from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vendors.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

db = SQLAlchemy(app)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database Models
class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    education = db.Column(db.String(50))
    contact = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100))
    stall_location = db.Column(db.String(200), nullable=False)
    food_type = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(200))
    
    # Hygiene Practices
    has_gloves = db.Column(db.Boolean, default=False)
    has_apron = db.Column(db.Boolean, default=False)
    washes_hands = db.Column(db.Boolean, default=False)
    uses_trash_bin = db.Column(db.Boolean, default=False)
    has_refrigerator = db.Column(db.Boolean, default=False)
    cleans_utensils = db.Column(db.Boolean, default=False)
    
    # Status
    is_approved = db.Column(db.Boolean, default=False)
    hygiene_score = db.Column(db.Integer, default=0)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(200))
    
    def calculate_hygiene_score(self):
        score = 0
        if self.has_gloves: score += 15
        if self.has_apron: score += 15
        if self.washes_hands: score += 25
        if self.uses_trash_bin: score += 15
        if self.has_refrigerator: score += 15
        if self.cleans_utensils: score += 15
        self.hygiene_score = score
        return score

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

# Create database tables
with app.app_context():
    db.create_all()
    # Create default admin if doesn't exist
    if not Admin.query.filter_by(username='admin').first():
        admin = Admin(username='admin', password_hash=generate_password_hash('admin123'))
        db.session.add(admin)
        db.session.commit()

# Routes
@app.route('/')
def index():
    """Dashboard with statistics"""
    total_vendors = Vendor.query.count()
    approved_vendors = Vendor.query.filter_by(is_approved=True).count()
    pending_vendors = total_vendors - approved_vendors
    avg_hygiene = db.session.query(db.func.avg(Vendor.hygiene_score)).scalar() or 0
    
    return render_template('index.html', 
                         total_vendors=total_vendors,
                         approved_vendors=approved_vendors,
                         pending_vendors=pending_vendors,
                         avg_hygiene=round(avg_hygiene, 1))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Vendor registration form"""
    if request.method == 'POST':
        # Generate unique vendor ID
        vendor_count = Vendor.query.count()
        vendor_id = f"VEN{datetime.now().year}{vendor_count + 1:04d}"
        
        # Handle file upload
        photo_filename = None
        if 'photo' in request.files:
            file = request.files['photo']
            if file.filename:
                photo_filename = secure_filename(f"{vendor_id}_{file.filename}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))
        
        # Create vendor
        vendor = Vendor(
            vendor_id=vendor_id,
            name=request.form['name'],
            age=int(request.form['age']),
            gender=request.form['gender'],
            education=request.form.get('education', ''),
            contact=request.form['contact'],
            email=request.form.get('email', ''),
            stall_location=request.form['stall_location'],
            food_type=request.form['food_type'],
            photo=photo_filename,
            has_gloves=request.form.get('has_gloves') == 'on',
            has_apron=request.form.get('has_apron') == 'on',
            washes_hands=request.form.get('washes_hands') == 'on',
            uses_trash_bin=request.form.get('uses_trash_bin') == 'on',
            has_refrigerator=request.form.get('has_refrigerator') == 'on',
            cleans_utensils=request.form.get('cleans_utensils') == 'on',
            password_hash=generate_password_hash(request.form['password'])
        )
        
        vendor.calculate_hygiene_score()
        db.session.add(vendor)
        db.session.commit()
        
        flash(f'Registration successful! Your Vendor ID is: {vendor_id}', 'success')
        return redirect(url_for('vendor_login'))
    
    return render_template('register.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and check_password_hash(admin.password_hash, password):
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    vendors = Vendor.query.order_by(Vendor.registration_date.desc()).all()
    return render_template('admin.html', vendors=vendors)

@app.route('/admin/approve/<int:vendor_id>')
def approve_vendor(vendor_id):
    """Approve vendor"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    vendor = Vendor.query.get_or_404(vendor_id)
    vendor.is_approved = True
    db.session.commit()
    flash(f'Vendor {vendor.name} approved!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete/<int:vendor_id>')
def delete_vendor(vendor_id):
    """Delete vendor"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    vendor = Vendor.query.get_or_404(vendor_id)
    db.session.delete(vendor)
    db.session.commit()
    flash(f'Vendor {vendor.name} deleted!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/vendor/login', methods=['GET', 'POST'])
def vendor_login():
    """Vendor login portal"""
    if request.method == 'POST':
        vendor_id = request.form['vendor_id']
        password = request.form['password']
        vendor = Vendor.query.filter_by(vendor_id=vendor_id).first()
        
        if vendor and check_password_hash(vendor.password_hash, password):
            session['vendor_id'] = vendor.id
            return redirect(url_for('vendor_portal'))
        else:
            flash('Invalid Vendor ID or password', 'danger')
    
    return render_template('vendor_login.html')

@app.route('/vendor/portal')
def vendor_portal():
    """Vendor personal portal"""
    if not session.get('vendor_id'):
        return redirect(url_for('vendor_login'))
    
    vendor = Vendor.query.get_or_404(session['vendor_id'])
    return render_template('vendor_portal.html', vendor=vendor)

@app.route('/vendors')
def vendor_list():
    """Public vendor directory"""
    location = request.args.get('location', '')
    if location:
        vendors = Vendor.query.filter_by(is_approved=True).filter(Vendor.stall_location.contains(location)).all()
    else:
        vendors = Vendor.query.filter_by(is_approved=True).all()
    
    return render_template('vendor_list.html', vendors=vendors)

@app.route('/logout')
def logout():
    """Logout"""
    session.clear()
    return redirect(url_for('index'))

# API Endpoints for AJAX
@app.route('/api/vendors')
def api_vendors():
    """Get all vendors as JSON"""
    vendors = Vendor.query.all()
    return jsonify([{
        'id': v.id,
        'vendor_id': v.vendor_id,
        'name': v.name,
        'location': v.stall_location,
        'hygiene_score': v.hygiene_score,
        'is_approved': v.is_approved
    } for v in vendors])

if __name__ == '__main__':
    app.run(debug=True)
