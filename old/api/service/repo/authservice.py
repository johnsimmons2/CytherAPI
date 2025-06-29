import base64
import os
import hashlib
from api.model.user import Role, User, UserRequest, UserRole
import api.service.jwthelper as jwth
from datetime import datetime, timedelta
from uuid import uuid4
from api.loghandler.logger import Logger
from sqlalchemy.orm import Query
from sqlalchemy import desc, func
from flask_mail import Message
from flask import current_app
from extensions import db


class AuthService:
    # Adds the current lowest level Role to the user if they have no roles.
    @classmethod
    def addDefaultRole(cls, user):
        roles = Query(UserRole, db.session).filter_by(userId=user.id).all()
        if roles is None or roles == []:
            user.roles.append(
                Query(Role, db.session).order_by(desc(Role.level)).first()
            )
            db.session.commit()

    @classmethod
    def adminResetPassword(cls, id: int, newPrd: str):
        user: User = Query(User, db.session).filter_by(id=id).first()
        if user is None:
            return False
        user.password = AuthService._hash_password(newPrd, user.salt)
        db.session.commit()
        return True

    @classmethod
    def resetPasswordManual(cls, id: int, oldPwd: str, newPrd: str):
        user: User = Query(User, db.session).filter_by(id=id).first()
        if user is None:
            return False
        if AuthService._hash_password(oldPwd, user.salt) == user.password:
            user.password = AuthService._hash_password(newPrd, user.salt)
            db.session.commit()
            return True
        else:
            return False

    @classmethod
    def resetPassword(cls, user: User, resetToken: str, newPassword: str):
        usersecret = os.getenv("USER_SECRET")
        requests: list[UserRequest] = Query(UserRequest, db.session).filter_by(userId=user.id).all()
        foundValidRequest = False
        foundRequest = None

        if requests is None or requests == []:
            Logger.error("No requests found")
            raise Exception("The URL provided was invalid or expired.")

        for req in requests:
            if req.expiry >= datetime.now():
                sha = hashlib.sha256()
                Logger.debug(f"{req.content} {user.email} {usersecret}")
                sha.update(req.content.encode('utf-8'))
                sha.update(str(user.email).encode('utf-8'))
                sha.update(str(usersecret).encode('utf-8'))
                compareToken = sha.hexdigest()
                Logger.debug(f"{compareToken} =?= {resetToken}")
                Logger.debug(f"{compareToken == resetToken}")
                if compareToken == resetToken:
                    Logger.debug(f"Validated the resetToken")
                    foundValidRequest = True
                    foundRequest = req
            else:
                Logger.debug(f"Request expired: {req.expiry}")

        if not foundValidRequest:
            raise Exception("The URL provided was invalid or expired.")

        salt = str(uuid4())
        user.salt = salt
        user.password = cls._hash_password(newPassword, salt)
        db.session.delete(foundRequest)
        db.session.commit()

    @classmethod
    def createResetLink(cls, user: User) -> str | None:
        usersecret = os.getenv("USER_SECRET")
        resetToken = ''
        try:
            key = base64.b64encode(str(uuid4()).encode('utf-8'))

            oldRequests = Query(UserRequest, db.session).filter_by(userId=user.id).all()
            for req in oldRequests:
                # Delete old requests so no tokens are dangling
                db.session.delete(req)
                db.session.commit()

            request = UserRequest()
            request.expiry = datetime.now() + timedelta(minutes=15)
            request.content = key
            request.userId = user.id

            db.session.add(request)
            db.session.commit()

            Logger.debug(f"Created a password reset key for {user.username}: {request.content}")
            Logger.debug(f"Token expires {request.expiry}")

            sha = hashlib.sha256()
            sha.update(str(request.content).encode('utf-8'))
            sha.update(str(user.email).encode('utf-8'))
            sha.update(str(usersecret).encode('utf-8'))
            resetToken = sha.hexdigest()
            Logger.debug(f"Token: {resetToken}")
        except Exception as error:
            Logger.error(error)
            return None

        URL = "https://cyther.online/reset-password?t=" + resetToken + "&u=" + user.username
        return URL

    @classmethod
    def sendPasswordResetEmail(cls, user: User) -> bool:
        usersecret = os.getenv("USER_SECRET")
        resetToken = ''
        try:
            key = base64.b64encode(str(uuid4()).encode('utf-8'))

            oldRequests = Query(UserRequest, db.session).filter_by(userId=user.id).all()
            for req in oldRequests:
                # Delete old requests so no tokens are dangling
                db.session.delete(req)
                db.session.commit()

            request = UserRequest()
            request.expiry = datetime.now() + timedelta(minutes=15)
            request.content = key
            request.userId = user.id

            db.session.add(request)
            db.session.commit()

            Logger.debug(f"Created a password reset key for {user.username}: {request.content}")
            Logger.debug(f"Token expires {request.expiry}")

            sha = hashlib.sha256()
            sha.update(str(request.content).encode('utf-8'))
            sha.update(str(user.email).encode('utf-8'))
            sha.update(str(usersecret).encode('utf-8'))
            resetToken = sha.hexdigest()
            Logger.debug(f"Token: {resetToken}")
        except Exception as error:
            Logger.error(error)
            return False

        URL = "https://cyther.online/reset-password?t=" + resetToken + "&u=" + user.username
        
        message_receiver = str(user.email)
        message_subject = f"[CYTHER.ONLINE] Password Reset Request for {user.username}."
        message_body = f"""
            <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Password Reset</title>
                </head>
                <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
                    <div style="max-width: 600px; margin: 50px auto; background-color: #ffffff; padding: 20px; border-radius: 5px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                        <h2 style="color: #333333;">Password Reset Request</h2>
                        <p>Hello,</p>
                        <p>We received a request to reset your password. Click the button below to reset your password:</p>
                        <a href="{URL}" style="display: inline-block; padding: 10px 20px; font-size: 16px; color: #ffffff; background-color: #007bff; border-radius: 5px; text-decoration: none; margin-bottom: 20px;">Reset Password</a>
                        <p>If the button above doesn't work, you can copy and paste the following link into your browser:</p>
                        <p style="word-wrap: break-word; color: #007bff;">{URL}</p>
                        <p>If you did not request a password reset, please ignore this email.</p>
                        <p>Thank you!</p>
                    </div>
                </body>
            </html>
        """
        
        message = Message(subject=message_subject, recipients=[message_receiver], html=message_body, sender=(os.getenv("ADMIN_EMAIL_NAME"), os.getenv("ADMIN_EMAIL")))
        success = False
        try:
            current_app.extensions['mail'].send(message)
            Logger.debug("Sent password reset email to " + user.email)
            success = True
        except Exception as exception:
            Logger.error("Failed to send password reset email to " + user.email)
            Logger.error(exception)
            import traceback as tb
            Logger.error(tb.format_exc())
        return success

    @classmethod
    def register_user(cls, user: User):
        salt = str(uuid4())
        nUser = User()
        nUser.salt = salt
        nUser.password = cls._hash_password(user.password, salt)
        nUser.username = user.username

        nUser.email = user.email
        nUser.fName = user.fName
        nUser.lName = user.lName

        nUser.created = datetime.now()
        nUser.lastOnline = datetime.now()

        db.session.add(nUser)
        cls.addDefaultRole(nUser)
        db.session.commit()
        return nUser

    @classmethod
    def _hash_password(cls, password: str, salt: str) -> str:
        usersecret = os.getenv("USER_SECRET")
        try:
            sha = hashlib.sha256()
            sha.update(password.encode(encoding="UTF-8", errors="strict"))
            sha.update(":".encode(encoding="UTF-8"))
            sha.update(salt.encode(encoding="UTF-8", errors="strict"))
            sha.update(usersecret.encode(encoding="UTF-8", errors="strict"))
            return sha.hexdigest()
        except Exception as error:
            Logger.error(error)
        return None

    @classmethod
    def authenticate_user(cls, inputUser: User) -> User | None:
        query = Query(User, db.session)
        user = None
        secret = inputUser.password
        if inputUser.username is not None:
            user = query.filter(func.lower(User.username) == func.lower(inputUser.username)).first()

        if not user:
            Logger.error("no user")
            return None

        if AuthService._hash_password(secret, user.salt) == user.password:
            Logger.debug("The token is being made")
            user.lastOnline = datetime.now()
            cls.addDefaultRole(user)
            db.session.commit()
            return jwth.create_token(user)
        else:
            Logger.error("Incorrect password!")
            return None
    
    @classmethod
    def refresh_token(cls, token: str) -> str | None:
        try:
            decoded = jwth.decode_token(token)
            Logger.debug(decoded)
            user = Query(User, db.session).filter_by(username=decoded["username"]).first()
            if user is not None:
                return jwth.create_token(user)
        except Exception as error:
            Logger.error(error)
        return None