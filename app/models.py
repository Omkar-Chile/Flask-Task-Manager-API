from datetime import datetime
from . import db
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
