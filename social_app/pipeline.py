# this is what usual facebook response looks like
# {
#     'username': 'foobar',
#     'access_token': 'CAAD...',
#     'first_name': 'Foo',
#     'last_name': 'Bar',
#     'verified': True,
#     'name': 'Foo Bar',
#     'locale': 'en_US',
#     'gender': 'male',
#     'expires': '5183999',
#     'email': 'foo@bar.com',
#     'updated_time': '2014-01-14T15:58:35+0000',
#     'link': 'https://www.facebook.com/foobar',
#     'timezone': -3,
#     'id': '100000126636010',
# }
import requests
from django.contrib.auth.password_validation import get_password_validators, validate_password
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.validators import validate_email
from requests import HTTPError
from social_core.exceptions import AuthException, AuthAlreadyAssociated, AuthCanceled
from social_core.pipeline.social_auth import associate_by_email as social_associate_by_email
from social_core.pipeline.user import USER_FIELDS
from django.conf import settings

from social_app.models import OccasionUser, update_user_image_path, update_user_thumbnail_path


def is_proper_password(password):
    if not password:
        raise ValidationError("Password is None")
    try:
        validate_password(password, password_validators=get_password_validators(settings.AUTH_PASSWORD_VALIDATORS))
        return True
    except ValidationError:
        raise


def is_proper_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError as e:
        return False


def check_existing_user(backend, uid, user=None, *args, **kwargs):
    provider = backend.name
    email = None
    request = kwargs.get('request', None)
    if request:
        email = request.get('email', None)
    if email:
        if not is_proper_email(email):
            raise AuthCanceled(
                backend,
                "Invalid Credentials Email"
            )
        try:
            OccasionUser.objects.get(email__iexact=email)
            msg = 'This {0} account is already in use.'.format(provider)
            # raise CustomAuthException(provider, msg)
            raise AuthAlreadyAssociated(backend, msg)
        except OccasionUser.DoesNotExist:
            pass
    return {}


def check_password(backend, uid, user=None, *args, **kwargs):
    provider = backend.name
    if provider == 'email':
        password = None
        request = kwargs.get('request', None)
        if request:
            password = request.get('password', None)
        try:
            is_proper_password(password)
        except ValidationError as e:
            raise AuthCanceled(
                backend,
                e.messages
            )
    return {}


def add_backend(strategy, details, user=None, *args, **kwargs):
    if kwargs['is_new']:
        if user and not user.backend:
            if 'backend' in kwargs:
                user.backend = kwargs['backend'].name
                user.save()


def save_profile_image(backend, user, response, *args, **kwargs):
    # if kwargs['is_new']:  # todo
    if backend.name == 'email':
        return
    if backend.name == 'google-oauth2':
        url = response['image'].get('url')
        try:
            response_large_image = requests.get(url + '&sz=500')
            response_small_image = requests.get(url)
            response_large_image.raise_for_status()
        except HTTPError:
            return
        image_name = str(user.id) + "_google.png"
    elif backend.name == 'facebook':
        url = "http://graph.facebook.com/{}/picture".format(response['id'])
        try:
            response_small_image = requests.get(url)
            response_large_image = requests.get(url, params={'type': 'large'})
            response_large_image.raise_for_status()
        except HTTPError:
            return
        image_name = str(user.id) + "_fb.png"

    user.thumbnail.save(image_name, ContentFile(response_small_image.content))
    user.image.save(image_name, ContentFile(response_large_image.content))
    user.save()


# social_core.pipeline.user.create_user
def create_user(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}

    fields = dict((name, kwargs.get(name, details.get(name, kwargs['response'].get(name)[0] if
    isinstance(kwargs['response'].get(name), list) else kwargs['response'].get(name, None))))
                  for name in backend.setting('USER_FIELDS', USER_FIELDS))

    if not fields:
        return

    return {
        'is_new': True,
        'user': strategy.create_user(**fields)
    }


# def user_password(strategy, user, is_new=False, *args, **kwargs):
#     """
#     the create_user part of the pipeline does not grab password field. So `user_password`
#     BUT ADDED FIX TO THE `create_user` NOW.
#     """
#     backend = kwargs.get('backend')
#     if backend:
#         if backend.name != 'email':
#             return
#
#         password = strategy.request_data().get('password', None)
#         kwargs['_not_password_'] = password
#         if not is_proper_password(password):
#             password = kwargs['response'].get('password')[0] if 0 < len(kwargs['response'].get('password')) else None
#             if not is_proper_password(password):
#                 raise AuthException(backend, "Invalid Credentials.")
#
#         if is_new:
#             user.set_password(password)
#             user.save()
#         elif not user.check_password(password):
#             # pass
#             raise AuthException(backend, "Invalid Credentials")


def associate_by_email(backend, details, user=None, *args, **kwargs):
    # social_core app already implemented this method
    if user:
        return None

    if backend.name == "email":
        email = backend.data.get("email")
        password = backend.data.get('password')
        if not is_proper_email(email):
            email = details.get('email', None)
            if not is_proper_email(email):
                raise AuthException(
                    backend,
                    "Invalid Credentials Email"
                )

        if not is_proper_password(password):
            password = kwargs['response'].get('password', None)
            if not is_proper_password(password):
                raise AuthException(
                    backend,
                    "Invalid Credentials Email"
                )
        return social_associate_by_email(backend, details, user, *args, **kwargs)
