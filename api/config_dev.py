# Definindo as configurações do ambiente de Desenvolvimento

# Configurações do banco de dados
conf_database = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'duplexsoft',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost', 
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET time_zone = '-03:00'",
        },
    }
}

# Indica se o debug está ativo ou não
conf_debug = True

# Definindo hosts permitidos
config_allowed_hosts = ['localhost', '127.0.0.1']

# Configurando a secret_key
config_secret_key = 'django-insecure-0g1jrsu4_x4+8qa$4**q(id2or=cu^()hg!i@23o&+3l1o8qh+'

# Origens permitidas pelo CORS
config_cors_allowed_origins = [
    "http://localhost:4200", 
]

# Configurando url para reset de senha
config_front_url = 'http://localhost:3000'

# Configurando envio de email
config_email_user = 'admin@duplexsoft.com.br'
config_email_password = 'D305125x'