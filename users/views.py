from .models import User
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
import re
import sys

class ManageUsers(APIView):
    serializer_class = UserSerializer

    def emailAlreadyExist(self,pEmail):
        return len(User.objects.filter(Q(email=pEmail) ).values()) == 1
    
    def usernameAlreadyExist(self,pUsername):
        return len(User.objects.filter(Q(username=pUsername) ).values()) == 1
    
    def checkPassword(self,pPassword):
        return len(pPassword)<12 or not re.search("[a-z]", pPassword) or not re.search("[A-Z]", pPassword) or not re.search("[A-Z]", pPassword) or not re.search("[0-9]", pPassword) or not re.search("[%€_@$^)(=+£*-/.~&\\|#!?;,:\{\}]" , pPassword)

    def get(self, request, format=None):
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)
    
    def post(self, request, format=None):
        userData = request.data
        tempUser = User(email = userData["email"], username= userData["username"], password = userData["password"], joined_date=userData["joined_date"])

        returnResp={
           "code":[],
           "message":[]   
        }

        alreadyInEmail = self.emailAlreadyExist(tempUser.email)
        alreadyInUsername = self.usernameAlreadyExist(tempUser.username)
        passwordIsValid = self.checkPassword(tempUser.password)

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
        
        if( passwordIsValid ): 
          # Check si le mot de passe est valide (assez fort)
          #print("Username déjà présent dans la DB")

          returnResp["code"].append("462")
          returnResp["message"].append("Password is too weak, must be at least 12 characters, at least one number, at least one capital letter, at lease one lowercase letter, at least one symbol")
          
        if (not alreadyInEmail and not alreadyInUsername and not passwordIsValid ):
          # On peut créer le User dans la DB

          # encodage du password avec la clé publique
          newMdp = tempUser.password
          
          tempUser.save()
          returnResp["code"].append("200")
          returnResp["message"].append("User created successfully")

        return Response(returnResp)