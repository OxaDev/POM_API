import jwt, secrets, datetime

def save_secret_token_key(secret_key, secretkey_filename):
	pubHandle = open(secretkey_filename, 'wb')
	pubHandle.write(secret_key.encode())
	pubHandle.close()


def decrypt_jwt(pJwt, secretkey_filename):
    with open(secretkey_filename, mode='rb') as privatefile:
        secret_key = privatefile.read().decode()
    return jwt.decode(pJwt,secret_key, algorithms='HS256')

def encrypt_jwt(payload, secretkey_filename):
    with open(secretkey_filename, mode='rb') as privatefile:
        secret_key = privatefile.read().decode()
    return jwt.encode(payload, secret_key, algorithm='HS256')

"""
# Générer le token
secret_key = secrets.token_urlsafe(256)
secret_key_filename= "./users/encryption/jwt_secret.tok"
print(secret_key)
# Sauvegarder le token
#save_secret_token_key(secret_key, secret_key_filename)

# Générer un payload de test
payload = {
    'username': "toto",
    'email': "toto@il.com",
    'expire_date': datetime.datetime.utcnow().strftime("%H:%M:%S %d-%m-%Y")
}

token = encrypt_jwt(payload, secret_key_filename)
print(token)
print(decrypt_jwt(token, secret_key_filename))

"""