
import rsa
from base64 import b64encode, b64decode

# Sauvegarder la clé privée dans un fichier
def save_private_key(privateKey, filename):
	privHandle = open(filename, 'wb')
	privHandle.write( rsa.PrivateKey.save_pkcs1(privateKey) )
	privHandle.close()

# Sauvegarder la clé publique dans un fichier
def save_public_key(publicKey, filename):
	pubHandle = open(filename, 'wb')
	pubHandle.write(rsa.PublicKey.save_pkcs1(publicKey) )
	pubHandle.close()

# Retourne le message (message) encrypté avec la public key, présente dans un fichier (filename), message est au format base64 decodé (donc en non bytes, lisible comme un hash)
# Etapes d'encryptage : encoder le str en bytes => encrypter les bytes avec la clé RSA => encoder les bytes cryptés dans la base 64 => décoder les bytes base 64 en str
def encrypt_message(message, pubkey_filename):
	with open(pubkey_filename, mode='rb') as publicfile:
		keydata = publicfile.read()
	pubKey = rsa.PublicKey.load_pkcs1(keydata)
	crypted_message= rsa.encrypt(message.encode(), pubKey)
	return b64encode(crypted_message).decode()

# Retourne le message crypté (encrypted_message) décrypté avec la private key, présente dans un fichier (filename)
# Etapes de decryptage : encoder le str base64 en bytes base64 => decoder les bytes base64 dans la base 64 => decrypter les bytes avec la clé RSA => decoder les bytes decryptés en str
def decrypt_message(encrypted_message, privkey_filename):
	with open(privkey_filename, mode='rb') as privatefile:
		keydata = privatefile.read()
	privkey = rsa.PrivateKey.load_pkcs1(keydata)
	b64_encrypted_message = b64decode(encrypted_message.encode())
	return rsa.decrypt(b64_encrypted_message, privkey).decode()

"""
pubkey_filename="public.pem"
privkey_filename="private.pem"

# Génère une clé RSA en 4096 (2048 est recommendé par NITS depuis 2015 mais on prends de l'avance, en 2030 on devra etre sur 4096)

publicKey, privateKey = rsa.newkeys(4096)
save_public_key(publicKey, pubkey_filename)
save_private_key(privateKey, privkey_filename)


message = "Je fais un test d'encryptage 4096"
encrypted_message = encrypt_message(message, pubkey_filename)
decrypted_message = decrypt_message(encrypted_message, privkey_filename)

print("Start : " + message)
print("Encrypted : " + encrypted_message )
print("Decrypted : " + decrypted_message)
"""