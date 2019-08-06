from django import forms

from social_app.pipeline import is_proper_password
from .models import OccasionUser, ShippingAddress


class SignupForm(forms.ModelForm):
    class Meta:
        model = OccasionUser
        fields = ['email', 'password', 'username']

    def clean_password(self):
        password = self.cleaned_data.get("password")
        is_proper_password(self.cleaned_data.get('password'))
        return password

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        exclude = []
