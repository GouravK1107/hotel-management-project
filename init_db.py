from app import app, db
from models import User

with app.app_context():
    db.create_all()
    # create default admin if not exists
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', password='admin')  # plain text; use hash in production
        db.session.add(admin)
        db.session.commit()
        print("Admin created: username=admin, password=admin")
    print("Database initialized.")