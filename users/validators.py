import re

from django.core.exceptions import ValidationError


class ComplexPasswordValidator:
    """Exige no mínimo 8 caracteres, 1 maiúscula, 1 minúscula e 1 caractere especial."""

    def validate(self, password, user=None):
        errors = []
        if len(password) < 8:
            errors.append('A senha deve ter no mínimo 8 caracteres.')
        if not re.search(r'[A-Z]', password):
            errors.append('A senha deve ter ao menos uma letra maiúscula.')
        if not re.search(r'[a-z]', password):
            errors.append('A senha deve ter ao menos uma letra minúscula.')
        if not re.search(r'[^A-Za-z0-9]', password):
            errors.append('A senha deve ter ao menos um caractere especial.')

        if errors:
            raise ValidationError(errors)

    def get_help_text(self):
        return (
            'A senha deve ter no mínimo 8 caracteres, incluindo letra '
            'maiúscula, letra minúscula e caractere especial.'
        )
