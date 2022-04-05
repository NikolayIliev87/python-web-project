from django.core.exceptions import ValidationError

VALIDATE_MESSAGE_LETTERS = 'Ensure this field contains only letters!'
VALIDATE_MESSAGE_PLUS_SIGN = 'Ensure this field starts with + !'
VALIDATE_MESSAGE_DIGITS = 'Ensure this field contains only digits after + !'


def validate_letters(value):
    for n in value:
        if not n.isalpha():
            raise ValidationError(VALIDATE_MESSAGE_LETTERS)


def validate_phone_number(value):
    if value[0] == "+":
        for n in value[1::]:
            if not n.isdigit():
                raise ValidationError(VALIDATE_MESSAGE_DIGITS)
    else:
        raise ValidationError(VALIDATE_MESSAGE_PLUS_SIGN)

