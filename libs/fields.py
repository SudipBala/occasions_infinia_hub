from django import forms
from easy_thumbnails.fields import ThumbnailerImageField


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
