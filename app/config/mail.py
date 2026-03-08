from fastapi_mail import ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME="yerson7897@gmail.com",
    MAIL_PASSWORD="CREAR CONTRASEÑA DE APLICACIÓN EN GMAIL",
    MAIL_FROM="yerson7897@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)