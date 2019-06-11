import json
import yaml
from django import forms
from django.contrib.postgres.fields import JSONField
from django.utils.translation import gettext_lazy as _

from django.contrib.postgres.forms.jsonb import InvalidJSONInput
from easy_thumbnails.fields import ThumbnailerImageField
from yaml.parser import ParserError
from yaml.scanner import ScannerError


class JSONFormField(forms.CharField):
    default_error_messages = {
        'invalid': _("'%(value)s' value must be valid JSON."),
    }

    def __init__(self, **kwargs):
        kwargs.setdefault('widget', forms.Textarea)
        super(JSONFormField, self).__init__(**kwargs)

    def to_python(self, value):
        if self.disabled:
            return value
        if value in self.empty_values:
            return None
        try:
            return yaml.safe_load(value)
        except (ValueError, ScannerError, ParserError):
            return json.loads(value)
        except ValueError:
            raise forms.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )
        except:  # FIXME
            raise  # uncomment me later

    def bound_data(self, data, initial):
        if self.disabled:
            return initial
        try:
            return yaml.safe_load(data)
        except (ValueError, ScannerError, ParserError):
            return json.loads(data)
        except ValueError:
            return InvalidJSONInput(data)

    def prepare_value(self, value):
        if isinstance(value, InvalidJSONInput):
            return value
        # json.loads dumps to unicode, yaml dumps to whatever the original encoding was in
        if isinstance(value, dict):
            return str(value)
        if value:
            value = yaml.safe_load(value)
        else:
            return {}
        if isinstance(value, dict):
            return str(value)


class SizeRestrictedThumbnailerField(ThumbnailerImageField):
    """
    Custom ImageField to restrict the maximum size of the image file.

    2.5MB - 2621440
    5MB - 5242880
    10MB - 10485760
    20MB - 20971520
    50MB - 5242880
    100MB 104857600
    250MB - 214958080
    500MB - 429916160

    required: max_upload_size
    """
    def __init__(self, *args, **kwargs):
        self.max_upload_size = kwargs.pop("max_upload_size", None)  # MB

        super(SizeRestrictedThumbnailerField, self).__init__(*args, **kwargs)

    def clean(self, value, model_instance):
        data = super(SizeRestrictedThumbnailerField, self).clean(value=value, model_instance=model_instance)

        uploaded_file = data.file
        try:
            if uploaded_file._size > self.max_upload_size:
                raise forms.ValidationError("Uploaded file size is {}. Size Limit: {}"
                                            .format(uploaded_file._size, self.max_upload_size))
        except AttributeError:
            pass
        return data


class CustomJsonField(JSONField):
    def formfield(self, **kwargs):
        defaults = {'form_class': JSONFormField}
        defaults.update(kwargs)
        return super(CustomJsonField, self).formfield(**defaults)
