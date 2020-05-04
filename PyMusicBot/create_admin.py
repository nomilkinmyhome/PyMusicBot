from app import db
from models import User


new_admin = User(name='root')
new_admin.set_password('toor')

db.session.add(new_admin)
db.session.commit()
