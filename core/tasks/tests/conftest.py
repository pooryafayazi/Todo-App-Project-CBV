import pytest
from django.conf import settings


@pytest.fixture(scope="session", autouse=True)
def configure_django_settings():
    settings.configure(
        DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
        REST_FRAMEWORK={
            # authentication settings
            "DEFAULT_AUTHENTICATION_CLASSES": [
                "rest_framework.authentication.BasicAuthentication",
                "rest_framework.authentication.SessionAuthentication",
                "rest_framework.authentication.TokenAuthentication",
                "rest_framework_simplejwt.authentication.JWTAuthentication",
            ],
            # coreapi settings
            "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
        },
    )
