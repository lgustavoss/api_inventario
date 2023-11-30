import re
from django.core.exceptions import ValidationError
from validate_docbr import CNPJ


# Aplicando a máscara no CNPJ
def formatar_cnpj(value):
    # Removendo caracteres não numéricos do valor
    cleaned_value = re.sub(r'[^0-9]', '', value)

    if len(cleaned_value) == 14:
        return '{}.{}.{}/{}-{}'.format(cleaned_value[:2], cleaned_value[2:5], cleaned_value[5:8], cleaned_value[8:12], cleaned_value[12:])
    else:
        raise ValidationError('Favor informar um CNPJ válido')

# Validando CNPJ com a máscara
def validar_cnpj(value):
    # Formate o valor com a máscara
    value = formatar_cnpj(value)
    
    # Remova a máscara para validação
    cleaned_value = re.sub(r'[^0-9]', '', value)

    # Verifique se o número pertence a um CNPJ
    if len(cleaned_value) == 14:
        cnpj_instance = CNPJ()
        if not cnpj_instance.validate(cleaned_value):
            raise ValidationError('CNPJ inválido')
    else:
        raise ValidationError('Favor informar um CNPJ válido')