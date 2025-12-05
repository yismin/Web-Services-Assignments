# resources/user.py
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)
from db import db
from models.user import UserModel
from schemas import UserSchema
from flask import jsonify

blp = Blueprint("users", __name__, description="Operations on users")

# Development blocklist for revoked token JTIs
# Export this so app.py can import and check it in JWT callbacks
jwt_blocklist = set()

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        """Register a new user"""
        if UserModel.query.filter_by(username=user_data["username"]).first():
            abort(409, message="A user with that username already exists.")

        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )

        db.session.add(user)
        db.session.commit()

        return user

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        """Login and get JWT tokens (access + refresh)"""
        user = UserModel.query.filter_by(username=user_data["username"]).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))
            return {"access_token": access_token, "refresh_token": refresh_token}, 200


        abort(401, message="Invalid username or password.")

@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        """Use refresh token to get a new access token"""
        user_id = get_jwt_identity()
        new_access = create_access_token(identity=user_id)
        return {"access_token": new_access}, 200

@blp.route("/logout_access")
class LogoutAccess(MethodView):
    @jwt_required()
    def delete(self):
        """Revoke current access token"""
        jti = get_jwt()["jti"]
        jwt_blocklist.add(jti)
        return jsonify({"msg": "access token revoked"}), 200

@blp.route("/logout_refresh")
class LogoutRefresh(MethodView):
    @jwt_required(refresh=True)
    def delete(self):
        """Revoke current refresh token"""
        jti = get_jwt()["jti"]
        jwt_blocklist.add(jti)
        return jsonify({"msg": "refresh token revoked"}), 200

@blp.route("/user")
class UserInfo(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self):
        """Get current user info (requires JWT)"""
        user_id = get_jwt_identity()
        user = UserModel.query.get_or_404(user_id)
        return user
