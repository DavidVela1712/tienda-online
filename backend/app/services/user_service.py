from app.extensions import db
from app.model.user import User
from flask_jwt_extended import create_access_token

def register_user(data):
    if User.query.filter_by(email=data.get("email")).first():
        raise ValueError("email ya registrado")
    
    user = User(
        name=data.get("name"),
        email=data.get("email"),
        role="user"
    )

    user.set_password(data.get("password"))

    db.session.add(user)
    db.session.commit()

    return user

def login_user(data):
    user = User.query.filter_by(email=data.get("email")).first()

    if not user or not user.check_password(data.get("password")):
        raise ValueError("Credenciales incorrectas")
    access_token = create_access_token(
        identity=user.id,
        additional_claims={"role": user.role}
    )

    return access_token
