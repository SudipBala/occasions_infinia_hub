import os
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validate_file_extensions(value):
    accepted_extensions = ['.pdf', '.jpg', '.png', '.gif', '.jpeg']
    ext = os.path.splitext(value.name)[1]
    if not ext.lower() in accepted_extensions:
        raise ValidationError("File extension not supported. Supported extensions: {0}".
                              format(', '.join(accepted_extensions)))


PHONE_REGEX = RegexValidator(regex=r'^\+?1?\d{7,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. "
                                         "Up to 15 digits allowed.")
