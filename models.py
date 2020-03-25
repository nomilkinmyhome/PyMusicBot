from app import db
from datetime import datetime
from sqlalchemy_utils import URLType


class Music(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    url = db.Column(URLType, nullable=False)
    pub_date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<Music id: {self.id}, title: {self.title}'
