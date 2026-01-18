from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

# ================= CONFIG =================

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tracelt.db'
app.secret_key = 'change_this_to_a_random_secret_key'
db = SQLAlchemy(app)

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ================= MODELS =================

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    type = db.Column(db.String(20), nullable=False)  # Lost, Found, Sale
    image = db.Column(db.String(100))
    place = db.Column(db.String(100))
    date = db.Column(db.String(20))
    contact = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float)
    condition = db.Column(db.String(20))
    status = db.Column(db.String(20), default='Available')
    meet_time = db.Column(db.String(50))
    meet_place = db.Column(db.String(100))

# Create database if missing
with app.app_context():
    db.create_all()

# ================= HELPERS =================

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ================= ROUTES =================

@app.route('/')
def home():
    items = Item.query.order_by(Item.id.desc()).all()
    return render_template('index.html', items=items)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        type = request.form.get('type')
        place = request.form.get('place')
        date = request.form.get('date')
        contact = request.form.get('contact')
        price_str = request.form.get('price')
        price = float(price_str) if price_str else None
        condition = request.form.get('condition')
        meet_time = request.form.get('meet_time')
        meet_place = request.form.get('meet_place')
        posted_by = request.form.get('posted_by', 'Anonymous')  # Default if not provided

        # Image upload
        image = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image = filename

        new_item = Item(
            title=title,
            description=description,
            type=type,
            place=place,
            date=date,
            contact=contact,
            price=price,
            condition=condition,
            meet_time=meet_time,
            meet_place=meet_place,
            image=image
        )
        db.session.add(new_item)
        db.session.commit()
        flash('Item added successfully!')
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route('/item/<int:id>')
def item_details(id):
    item = Item.query.get_or_404(id)
    return render_template('details.html', item=item)

@app.route('/update_status/<int:id>', methods=['POST'])
def update_status(id):
    item = Item.query.get_or_404(id)
    item.status = request.form.get('status')
    db.session.commit()
    flash('Status updated!')
    return redirect(url_for('item_details', id=id))

@app.route('/search')
def search():
    query = request.args.get('q', '')
    type = request.args.get('type', '')
    status_filter = request.args.get('status', '')

    items_query = Item.query
    if query:
        items_query = items_query.filter(
            (Item.title.contains(query)) | (Item.description.contains(query))
        )
    if type:
        items_query = items_query.filter_by(type=type)
    if status_filter:
        items_query = items_query.filter_by(status=status_filter)

    items = items_query.order_by(Item.id.desc()).all()
    return render_template('search.html', items=items, query=query, type=type, status=status_filter)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
