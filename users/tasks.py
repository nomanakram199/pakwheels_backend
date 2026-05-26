import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def send_email_task(
    to_email: str,
    subject: str,
    template_name: str,
    context: dict | None = None,
) -> int:
    context = context or {}
    html = render_to_string(template_name, context)

    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body="",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email],
        )
        email.attach_alternative(html, "text/html")
        return email.send(fail_silently=False)
    except Exception as e:
        logger.exception(
            "Email sending failed",
            extra={"to_email": to_email, "error": str(e)},
        )
        raise
