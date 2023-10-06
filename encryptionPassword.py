from Crypto.PublicKey import RSA


#creation d´un couple de clés
key = RSA.generate(1024)

#chiffrage
public_key = key.publickey()
enc_data = public_key.encrypt(b"""bonjour c'est un message secret""", 32)

#dechiffrage
x = key.decrypt(enc_data)
x = x.decode('utf-8')

#afficher ses clés:
k = key.exportKey('PEM')
p = key.publickey().exportKey('PEM')

#sauvegarder ses clés dans des fichiers:
with open('private.pem','w') as kf:
	kf.write(k.decode())
	kf.close()

with open('public.pem','w') as pf:
	pf.write(p.decode())
	pf.close()

#importer des clés à partir d'un fichier
with open('private.pem','r') as fk:
	priv = fk.read()
	fk.close()

with open('public.pem','r') as fp:
	pub = fp.read()
	fp.close()

privat = RSA.importKey(priv)
public = RSA.importKey(pub)