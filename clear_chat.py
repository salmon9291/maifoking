from models import db, Message
from server import app

with app.app_context():
    Message.query.delete()
    db.session.commit()
    print("All messages have been deleted.")
    