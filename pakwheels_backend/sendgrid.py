from decouple import config

SENDGRID_API_KEY = config("SENDGRID_API_KEY", default="")

if SENDGRID_API_KEY:
    EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
