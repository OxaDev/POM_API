from .models import *
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .encryption.encryptionPassword import encrypt_message
from .encryption.jwtToken import *
import jwt, sys, secrets, datetime, re

class UtilsUsers():
  pubkey_filename = "./users/encryption/public.pem"
  privjwt_filename = "./users/encryption/jwt_secret.tok"

  def usernameAlreadyExist(pUsername):
    return len(User.objects.filter(Q(username=pUsername) ).values()) == 1
  
  def checkPassword(pPassword):
    return len(pPassword)<12 or not re.search("[a-z]", pPassword) or not re.search("[A-Z]", pPassword) or not re.search("[A-Z]", pPassword) or not re.search("[0-9]", pPassword) or not re.search("[%€_@$^)(=+£*-/.~&\\|#!?;,:\{\}]" , pPassword)

  def emailAlreadyExist(pEmail):
    return len(User.objects.filter(Q(email=pEmail) ).values()) == 1
  
  def isTokenSignatureValid(pToken, pivate_tokenkey_filename):
    with open(pivate_tokenkey_filename, mode='rb') as privatefile:
        secret_key = privatefile.read().decode()
    
    try:
      jwt_decoded = jwt.decode(pToken,secret_key, algorithms='HS256')
      return jwt_decoded
    except jwt.exceptions.InvalidSignatureError:
      return False
    except jwt.exceptions.DecodeError:
      return False
    
  def checkTokenAuth(pToken, userEmail):
    returnResp={
      "code":[],
      "message":[]   
    }
    
    tempToken = UtilsUsers.isTokenSignatureValid(pToken, UtilsUsers.privjwt_filename)

    # Si le token JWT est invalide (signature non valide)
    if( UtilsUsers.isTokenSignatureValid(pToken, UtilsUsers.privjwt_filename) ==  False ):
      returnResp["code"].append("463")
      returnResp["message"].append("Invalid Auth Token")
      # Pas besoin d'aller à la suite, le token est illisible
      return returnResp
    if(tempToken["email"] != userEmail):
      returnResp["code"].append("470")
      returnResp["message"].append("Auth Token doesn't match email provided in request")
      # Pas besoin d'aller à la suite, le token est illisible
      return returnResp

    # Verifier si le token est expiré
    # Format des dates : 22:06:07 14-04-3940
    list_date_str = tempToken["expire_date"].split(" ")
    second = int(list_date_str[0].split(":")[2])
    minute = int(list_date_str[0].split(":")[1])
    hour = int(list_date_str[0].split(":")[0])
    day = int(list_date_str[1].split("-")[0])
    month = int(list_date_str[1].split("-")[1])
    year = int(list_date_str[1].split("-")[2])

    expired_date = datetime.datetime(year, month, day, hour, minute, second)
    if(datetime.datetime.utcnow() > expired_date):
      # Token périmé, il faut en regénérer un autre
      returnResp["code"].append("463")
      returnResp["message"].append("Expired Auth Token")
    
    # Si le returnResp n'a pas été modifié, il n'y a aucun problème avec le token
    return returnResp
    
  def getUserFromEmail(pEmail):
    try:
      tempUser = User.objects.filter(email=pEmail).get()
      return tempUser
    except User.DoesNotExist:
      return None
    
  def getUserFromUsername(pUsername):
    try:
      tempUser = User.objects.filter(username=pUsername).get()
      return tempUser
    except User.DoesNotExist:
      return None
  
  def getJsonOfUserDetailed(pUser):
    return {"username":pUser.username,"email":pUser.email, "joined_date": pUser.joined_date, "password": pUser.password}

class ManageUsers(APIView):
  serializer_class = UserSerializer
  pubkey_filename = UtilsUsers.pubkey_filename

  def get(self, request, format=None):
    if("email" not in request.data.keys()):
      return Response( [{"username":user.username,"email":user.email} for user in User.objects.all()] )
    
    returnResp={
      "code":[],
      "message":[]   
    }

    # Si la recherche se basait uniquement sur l'email
    search_email = request.data["email"]
    userFromEmail = UtilsUsers.getUserFromEmail(search_email)
    if(userFromEmail == None):
      returnResp["code"].append("465")
      returnResp["message"].append("No user found with this email")
    else:
      returnResp["code"].append("200")
      returnResp["message"].append("User found from email")
      returnResp["user"] = []
      returnResp["user"].append( UtilsUsers.getJsonOfUserDetailed(userFromEmail) )


    return Response(returnResp)

  def createUser(self, userData):
    returnResp={
      "code":[],
      "message":[]   
    }
    currentDate=datetime.datetime.utcnow().strftime("%d-%m-%Y")
    tempUser = User(email = userData["email"], username= userData["username"], password = userData["password"], joined_date=currentDate)
    alreadyInEmail = UtilsUsers.emailAlreadyExist(tempUser.email)
    alreadyInUsername = UtilsUsers.usernameAlreadyExist(tempUser.username)
    passwordIsValid = not UtilsUsers.checkPassword(tempUser.password)

    # Check s'il existe déjà
    if( alreadyInEmail ):
      # E-mail déjà présente dans la DB
      #print("E-mail déjà présente dans la DB")

      returnResp["code"].append("460")
      returnResp["message"].append("Email already taken")
      
    if( alreadyInUsername ): 
      # Username déjà présente dans la DB
      #print("Username déjà présent dans la DB")

      returnResp["code"].append("461")
      returnResp["message"].append("Username already taken")
    
    if( not passwordIsValid ): 
      # Check si le mot de passe est valide (assez fort)
      #print("Username déjà présent dans la DB")

      returnResp["code"].append("462")
      returnResp["message"].append("Password is too weak, must be at least 12 characters, at least one number, at least one capital letter, at lease one lowercase letter, at least one symbol")
      
    if (not alreadyInEmail and not alreadyInUsername and passwordIsValid ):
      # On peut créer le User dans la DB

      # encodage du password avec la clé publique
      tempUser.password = encrypt_message(tempUser.password,self.pubkey_filename)
      
      tempUser.save()
      returnResp["code"].append("200")
      returnResp["message"].append("User created successfully")
      returnResp["message"].append("User encoded password : " + tempUser.password)
    
    return returnResp
    
  def editUser(self, requestData, tokenAuth):
    returnResp={
      "code":[],
      "message":[]   
    }

    passwordIsValid = UtilsUsers.checkPassword(requestData["password"])
    tokenIsValid = UtilsUsers.checkTokenAuth(tokenAuth,requestData["email"])
    alreadyInEmail = UtilsUsers.emailAlreadyExist(requestData["email"])

    if( passwordIsValid ): 
      # Check si le mot de passe est valide (assez fort)
      returnResp["code"].append("462")
      returnResp["message"].append("Password is too weak, must be at least 12 characters, at least one number, at least one capital letter, at lease one lowercase letter, at least one symbol")
    
    if ( len(tokenIsValid["code"]) != 0 ):
      return tokenIsValid
    
    if ( not alreadyInEmail ):
      returnResp["code"].append("464")
      returnResp["message"].append("The user with this email was not found in the DB")

    # Si aucune erreur n'a été trouvée pour modifier le mot de passe
    if(len(returnResp["code"]) == 0):
      tempUser = User.objects.filter(email=requestData["email"])
      tempUser.password= encrypt_message(requestData["password"],self.pubkey_filename)
      tempUser.update()

      returnResp["code"].append("200")
      returnResp["message"].append("User's password successfully edited")

    return returnResp
    
  def post(self, request, format=None):
    return Response(self.createUser(request.data))

  def put(self, request, format=None):
    return Response(self.editUser(request.data, request.headers['Auth-Token']))

  def delete(self, request, format=None):
    userData = request.data
    return Response({})


class ManageToken(APIView):
  privjwt_filename = UtilsUsers.privjwt_filename

  def generateJWT(self,requestData, tempUser):

    returnResp={
      "code":[],
      "message":[]   
    }
    option_expire={
      "10 seconds":datetime.timedelta(seconds=10),
      "1 minute":datetime.timedelta(minutes=1),
      "1 hour":datetime.timedelta(hours=1),
      "24 hours":datetime.timedelta(days=1),
      "48 hours":datetime.timedelta(days=2),
      "15 days":datetime.timedelta(days=15),
      "30 days":datetime.timedelta(days=30),
      "90 days":datetime.timedelta(days=90),
      "1 year":datetime.timedelta(days=365),
      "never":datetime.timedelta(weeks=99999),
    }

    if( "expire" not in requestData.keys() ):
      # Token non précisé dans le body de la requête
      returnResp["code"].append("466")
      returnResp["message"].append("No date of expiration specified in request")
      
    elif(requestData["expire"] not in option_expire.keys() ):
      # Token non valide dans le body de la requête
      returnResp["code"].append("467")
      returnResp["message"].append("Invalid date of expiration")

    # Si aucune erreur n'a été notifiée
    if( len(returnResp["code"]) == 0 ):
      # Création du payload
      datenow = datetime.datetime.utcnow()
      expire_date = datenow + option_expire[requestData["expire"] ]

      payload = {
          'username': tempUser.username,
          'email': tempUser.email,
          'expire_date': (expire_date).strftime("%H:%M:%S %d-%m-%Y")
      }

      token = encrypt_jwt(payload, self.privjwt_filename)

      returnResp["code"].append("200")
      returnResp["message"].append("Token generated !")
      returnResp["token"] = token

    return returnResp

  # Récupérer le token d'authentification en donnant l'email et le mdp (encodé et crypté)
  def get(self, request, format=None):
    userData = request.data
    alreadyInEmail = UtilsUsers.emailAlreadyExist(userData["email"])
    returnResp={
      "code":[],
      "message":[]   
    }

    if(not alreadyInEmail):
      # Email non présente parmis les users
      returnResp["code"].append("464")
      returnResp["message"].append("The user with this email was not found")
      return Response(returnResp)
    
    # Email présente, on peut récupérer l'user
    tempUser =UtilsUsers.getUserFromEmail(userData["email"])

    # On vérifie si le mot de passe est valide
    if(tempUser.password == userData["password"] ):
      returnResp = self.generateJWT(userData,tempUser)
    else:
      returnResp["code"].append("468")
      returnResp["message"].append("Invalid password")
    
    return Response(returnResp)
