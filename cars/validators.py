import datetime
from django.core.exceptions import ValidationError

def validate_car_year(value):
    current_year = datetime.date.today().year
    if value < 1886 or value > current_year + 1:
        raise ValidationError(
            f"Year must be between 1886 and {current_year + 1}."
        )
