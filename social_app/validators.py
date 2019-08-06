from django.conf import settings
from django.contrib.auth.hashers import identify_hasher
from django.contrib.auth.password_validation import validate_password, get_password_validators
from django.core.exceptions import ValidationError
from django.utils.encoding import force_text


def password_hashed(password):
    """
    To check if the password is hashed
    """
    # FIXME
    try:
        validate_password(password, password_validators=get_password_validators(settings.AUTH_PASSWORD_VALIDATORS))
    except ValidationError:
        raise

    try:
        hasher = identify_hasher(password)
        if hasher:
            return True
    except ValueError:
        return False
    return False

