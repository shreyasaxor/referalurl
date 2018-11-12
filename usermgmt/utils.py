from itsdangerous import URLSafeSerializer

from keyaith import settings


def generate_secretkey(email):
    s = URLSafeSerializer(settings.SECRET_KEY)
    secretkey = s.dumps(email,salt=settings.SALT)
    return secretkey


def authenticate_key(secretkey):
    s = URLSafeSerializer(settings.SECRET_KEY)
    try:
        return s.loads(secretkey,salt=settings.SALT)
    except:
        return False