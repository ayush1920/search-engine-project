import jwt
from django.conf import settings
import datetime
import time
from django.contrib.auth import logout as dj_logout, login as dj_login
from django.shortcuts import redirect
from .models import AuthToken

UNAUTHENTICATED_REDIRECT = '/'

def generate_jwt_token(user, time_interval = 30):
    primary_key = user.id
    dt = datetime.datetime.utcnow() + datetime.timedelta(minutes=time_interval)

    token = jwt.encode({
        'id': primary_key,
        'exp': dt,
    }, settings.SECRET_KEY, algorithm='HS256')

    AuthToken.objects.update_or_create(user = user, auth_token = token)
    return token, dt

def checkTokenValidity(token, user):
    token_details =  jwt.decode(token, settings.SECRET_KEY, algorithms='HS256', options= { "verify_signature": False })
    is_valid_user = token_details['id'] == user.id
    is_not_expired = token_details['exp'] -  time.time() > 0
    exists_in_db = bool(AuthToken.objects.filter(user = user))
    return is_valid_user and is_not_expired and exists_in_db
        

def logout(request, redirect_url):
    if not request.user:
        return

    response = redirect(redirect_url)
    response.delete_cookie('token')
    AuthToken.objects.filter(user =  request.user).delete()
    dj_logout(request)
    return response

def login(request, user, redirect_link):
    dj_login(request, user)
    # update cookie with new token
    response = redirect(redirect_link)
    value, expires = generate_jwt_token(user)
    print(expires)
    response.set_cookie('token', value, expires= expires)
    return response

def is_authenticated(request):
    user = request.user
    jwt_token = request.COOKIES.get('token', None)
    if not (user and jwt_token):
        return False
    return request.user.is_authenticated and checkTokenValidity(jwt_token, user)

def needs_authentication(function):
    def wrapper(request):
        if not is_authenticated(request):
            return redirect(UNAUTHENTICATED_REDIRECT)

        return function(request)
    return wrapper
