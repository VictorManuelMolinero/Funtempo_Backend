import json

from django.db import IntegrityError
from api.models import User
from rest_framework import status
from api.serializers import UserSerializer
from rest_framework.views import APIView
from django.http.response import JsonResponse
import pdb
from django.views.decorators.csrf import csrf_exempt

class UserController(APIView):

    '''Method to retrieve all the users from the database.
    It wasn't used, but i added it because it's a default CRUD method'''
    def getAll(self, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    #Method to create or retrieve a user from the database
    def post(self, request, format=None):

        #Saves the recieved user data
        data = json.loads(request.body)
        email = data.get('email')

        '''The email is ONLY necessary when the user is gonna
        create an account.
        If it's included, they're trying to create a new one,
        if not, they're gonna login with a preexisting one'''
        if email is not None:
            username = data.get('username')
            try:
                user = User.objects.get(username=username)
            #If the username is not already taken, save the new account
            except User.DoesNotExist:
                #Serialize it so it can be saved in the database
                serializer = UserSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
            return JsonResponse({"error": "User already exists"}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                '''Search the user and the password in the database,
                and return them if they've been found
                '''
                data = json.loads(request.body)
                password = data['password']
                username = data['username']
                user = User.objects.get(username=username, password=password)
            except User.DoesNotExist:
                return JsonResponse({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
            serializer = UserSerializer(user)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        
        return JsonResponse(serializer.errors, status=status.HTTP_200_OK, safe=False)

    #Method to edit a user from the database
    def put(self, request, username, format=None):
        #Try to get the user filtering with it's primary key
        try:
            user = User.objects.get(pk=username)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        #Serialize it so it can be updated in the database
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
            except IntegrityError as e:
                return JsonResponse({"error": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)
        
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)
    
    #Method to delete a user from the database
    def delete(self, request, username, format=None):
        #Search the user using it's username
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        user.delete()
        return JsonResponse({"success": "User deleted"}, status=status.HTTP_200_OK, safe=False)
