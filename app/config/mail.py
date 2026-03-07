from fastapi_mail import ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME="tucorreo@gmail.com",
    MAIL_PASSWORD="tu_password_app",
    MAIL_FROM="tucorreo@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)