from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError, IntegrityError


class SocialAppConfig(AppConfig):
    name = 'social_app'

    def ready(self):
        from actstream.registry import register
        register(self.get_model("OccasionUser"))

        OccasionUser = self.get_model("OccasionUser")
        from oauth2_provider.generators import generate_client_id, generate_client_secret
        from oauth2_provider.models import Application
        try:
            if True:
                user = OccasionUser.objects.filter(email="sudipbala01@gmail.com")
                if not user:
                    user = OccasionUser(email="sudipbala01@gmail.com", username="sudip")
                    user.set_password("12345")
                    user.is_staff = True
                    user.save()
                else:
                    user = user[0]

                app = Application.objects.filter(name="Occasions")
                if not app:
                    client_id = generate_client_id()
                    client_secret = generate_client_secret()
                    app = Application(
                        client_id=client_id,
                        client_secret=client_secret,
                        client_type="confidential",
                        authorization_grant_type="password",
                        name="Occasions", user=user)
                    app.save()
        except (OperationalError, ProgrammingError, IntegrityError):
            # programmingError, when using psql as backend
            # IntegrityError for when user already exists in the database, .. you will see
            pass
