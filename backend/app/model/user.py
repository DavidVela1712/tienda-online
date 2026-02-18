from datetime import datetime
from app.extensions import db, bcrypt

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(5), default="user")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, raw_password):
        self.password = bcrypt.generate_password_hash(raw_password).decode("utf-8")
    
    def c(self, raw_password):
        return bcrypt.check_password_hash(self.password, raw_password)