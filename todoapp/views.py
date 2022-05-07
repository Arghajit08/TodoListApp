from django.shortcuts import render
#we will create login api in which base user model will be used to create payload and then in view api we will do user=Todo.objects.filter(username=payload['username']).all() and pass into serializer and then return json data
#we will create update api in  which we will do user=Todo.objects.get(username=payload['username'],id=request.id).update(title=request.title,completed=request.completed) and then return json data
#we will crete delete api in which we will do user=Todo.objects.get(username=payload['username'],id=request.id).delete() and then return json data
# Create your views here.
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import *
import jwt
import datetime
from django.contrib.auth.models import User

#User login Api to login userss
class CreateView(APIView):
    def post(self, request):
        username = request.data['username']
        password=request.data['password']
        user = User.objects.filter(username=username).first()
        if user is None:
            serializer = UserSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        user = User.objects.filter(username=username).first()

       
        payload = {
            'id': user.id,
            'username': user.username,
            'password':user.password,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow(),
        }

        #token includes user id and level
        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        time = datetime.datetime.utcnow() + datetime.timedelta(seconds=120)
        response.data = {
            'jwt': token,
            'time': time
        }

        return response

class LoginView(APIView):
    def post(self,request):
        token=request.data['token']
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token Expired! Log in again.')

        response = Response()
        username=request.data['username']
        password=request.data['password']
        if(payload['username']==username and payload['password']==password):
            user=Todo.objects.filter(username=payload['username']).all()
            if user is None:
                print(1)
                return Response({'message':'Login Successful'})
            else:
                serializer=TodoSerializers(data=user,many=True)
                if serializer.is_valid():
                    serializer.save()
                return Response({'tasks':serializer.data})
        else:
            return Response({'message':'Login Failed'})

class UpdateView(APIView):
    def get(self,request):
        token=request.data['token']
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token Expired! Log in again.')

        response = Response()
        username=request.data['username']
        id=request.data['id']
        completed=request.data['status']
        if(payload['username']==username):
            user=Todo.objects.filter(username=payload['username'],id=id).first()
            user.completed=completed
            user.save()
            return Response({'message':'Task Updated'})
        else:
            return Response({'message':'Not Updated'})
    
    def post(self, request):
        username = request.data['username']#used name and level for signup and login
        token=request.data['token']
        count=0
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token Expired! Log in again.')

        response = Response()
        if(payload['username']==username):
            user = Todo.objects.filter(username=username).first()
            serializer = TodoSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            count=1
        user = Todo.objects.filter(username=username).first()
        user.save()
        return Response({'message':'Task Added','count':count})


class DeleteView(APIView):
    def get(self,request):
        token=request.data['token']
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token Expired! Log in again.')

        response = Response()
        username=request.data['username']
        id=request.data['id']
        if(payload['username']==username):
            user=Todo.objects.filter(username=payload['username'],id=id).delete()
            return Response({'message':'Task Deleted'})
        else:
            return Response({'message':'Couldnot delete'})


        