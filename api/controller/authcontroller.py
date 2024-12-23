from flask import Blueprint, request
from api.controller import OK, BadRequest, Posted
from api.controller.controller import Conflict, NotFound, UnAuthorized
from api.decorator.auth.authdecorators import isAuthorized, isAdmin
from api.loghandler.logger import Logger
from api.model.user import User
from api.service.dbservice import AuthService, UserService
import api.service.jwthelper as jwth
import json
import os


auth = Blueprint('auth', __name__)
mailSender = {
    'email': os.getenv('ADMIN_EMAIL'),
    'name': os.getenv('ADMIN_EMAIL_NAME')
}
mailToken = os.getenv('MAILTRAP_TOKEN')
mailEndpoint = os.getenv('https://send.api.mailtrap.io/')


@auth.route("/auth", methods = ['GET'])
@isAuthorized
def checkAuth():
    return OK(UserService.getCurrentUserRoles())

@auth.route("/auth/email-password-request", methods = ['POST'])
def passwordResetEmail():
    if request.get_json() is None:
        return BadRequest('No user was provided or the input was invalid.')
    email = json.loads(request.data)['email']

    foundUser = UserService.getByEmail(email)
    if foundUser is None:
        return NotFound('No user was found with that email.')
    Logger.debug(f'({foundUser.username}) with email {email} requested a password reset.')

    success = AuthService.sendPasswordResetEmail(foundUser)
    if not success:
        return BadRequest('Email could not be sent.')
    return OK("Password reset email sent.")

@auth.route("/auth/reset-password/manual-request", methods = ['POST'])
def passwordResetManual():
    if request.get_json() is None:
        return BadRequest('No user was provided or the input was invalid.')
    data = request.get_json()
    old = data.get('old_secret')
    new = data.get('new_secret')
    userId = data.get('id')
    
    if old is None or new is None or userId is None:
        return NotFound('Request supplied was invalid.')

    try:
        AuthService.resetPasswordManual(userId, old, new)
    except:
        return UnAuthorized("Token was invalid or expired")

    return OK("Gotcha!")

@isAdmin
@auth.route("/auth/reset-password", methods = ['POST'])
def passwordReset():
    resetToken = request.args.get('resetToken')
    if resetToken == None:
        return BadRequest('Query param ?resetToken was not provided.')

    if request.get_json() is None:
        return BadRequest('No user was provided or the input was invalid.')
    user = User(**json.loads(request.data))
    foundUser = UserService.getByUsername(user.username)

    if foundUser is None or foundUser.email == None:
        return NotFound('No user was found with that email.')

    try:
        AuthService.resetPassword(foundUser, resetToken, user.password)
    except:
        return UnAuthorized("Token was invalid or expired")

    return OK("Password reset succeeded")

@auth.route("/auth/force-password-reset", methods = ['POST'])
def adminPasswordReset():
    if request.get_json() is None:
        return BadRequest('No user was provided or the input was invalid.')
    user = User(**json.loads(request.data))
    foundUser = UserService.getByUsername(user.username)

    if foundUser is None or foundUser.email == None:
        return NotFound('No user was found with that email.')

    try:
        AuthService.adminResetPassword(foundUser, user.password)
    except:
        return BadRequest("Something went wrong!")

    return OK("Admin has forced the password to reset")

@auth.route("/auth/token", methods = ['POST'])
def authenticate():
    if request.get_json() is None:
        return BadRequest('User was not provided or something was wrong with the input fields.')

    user = User(**json.loads(request.data))
    if user.password is None:
        return BadRequest('No password was provided.')
    if user.username is None and user.email is None:
        return BadRequest('No username or email was provided.')
    authenticated = AuthService.authenticate_user(user)
    if authenticated is not None:
        return OK(dict({"token": str(authenticated)}))
    else:
        return UnAuthorized("Authentication failed")

@auth.route("/auth/register", methods = ['POST'])
def post():
    if request.get_json() is None:
        return BadRequest('No user was provided or the input was invalid.')

    user = User(**json.loads(request.data))
    if user.password is None:
        return BadRequest('No password was provided.')

    if user.username is None and user.email is None:
        return BadRequest('No username or email was provided.')

    if UserService.exists(user):
        return Conflict('User already exists with that email or username.')

    user = AuthService.register_user(user)
    if user is None:
        return BadRequest('User could not be created.')

    token = jwth.create_token(user)
    if token is None:
        return BadRequest('User could not be authenticated.')

    return Posted(token)