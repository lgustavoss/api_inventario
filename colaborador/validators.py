import re
from django.core.exceptions import ValidationError
from validate_docbr import CPF


# Aplicando a máscara no CPF ou CNPJ
def formatar_cpf(value):
    # Removendo caracteres não numéricos do valor
    cleaned_value = re.sub(r'[^0-9]', '', value)

    if len(cleaned_value) == 11:
        return '{}.{}.{}-{}'.format(cleaned_value[:3], cleaned_value[3:6], cleaned_value[6:9], cleaned_value[9:])
    else:
        raise ValidationError('Favor informar um CPF ou CNPJ válido')

# Validando CPF ou CNPJ com a máscara
def validar_cpf(value):
    # Formate o valor com a máscara
    value = formatar_cpf(value)
    
    # Remova a máscara para validação
    cleaned_value = re.sub(r'[^0-9]', '', value)

    # Verifique se o número pertence a um CPF
    if len(cleaned_value) == 11:
        cpf_instance = CPF()
        if not cpf_instance.validate(cleaned_value):
            raise ValidationError('CPF inválido')
    else:
        raise ValidationError('Favor informar um CPF válido')