from django.http import Http404
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import CustomUserSerializer, ChangePasswordSerializer
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.generics import (ListCreateAPIView,RetrieveUpdateDestroyAPIView,)
#from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly


class CustomUserList(APIView):
    queryset=CustomUser.objects.all()
    serializer_class=CustomUserSerializer
    permission_classes=[]

    def get(self, request):
          users = CustomUser.objects.all()
          serializer = CustomUserSerializer(users, many=True)
          return Response(serializer.data)
          
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=CustomUser.objects.all()
    serializer_class=CustomUserSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)

    def get_object(self, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
            self.check_object_permissions(self.request, user)
            return user
        except user.DoesNotExist:
            raise Http404
            
    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        data = request.data
        serializer = CustomUserSerializer(
            instance=user,
            data=data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        if user:
            user.delete()
            return Response({"status":"ok"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeView(APIView):
    def get(self, request):
        user = self.request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)


# class CreateAccountView(ListCreateAPIView):
#     queryset=CustomUser.objects.all()
#     serializer_class=CustomUserSerializer
#     #permission_classes=[IsAuthenticated]

    # def perform_create(self, serializer):
    #     user=self.request.user
    #     serializer.save(user=user)
        
    #def post(self,request): #send verification email to activate user account
    #     user=request.data
    #     serializer=self.serializer_class(data=user)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     user_data = serializer.data #
    #     user=CustomUser.objects.get(email=user_data['email'])
    #     token=RefreshToken.for_user(user).access_token #
    #     current_site=get_current_site(request).domain#
    #     relativeLink=reverse('email-verify')#
    #     absurl='http://'+current_site+relativeLink+"?token="+str(token)#
    #     email_body='Hi '+user.username+' Use link below to verify your email \n'+ absurl#
    #     data={'email_body':email_body,'to_email':user.email,'subject':'Verify your email'}#
    #     Util.send_email(data)#

class VerifyEmail(generics.GenericAPIView):
    def get(self):
        pass

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = CustomUser
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)