# Create your views here.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils import generate_secretkey,authenticate_key
from .serializers import UserSerializers
from .models import User


class GetUser(APIView):


    def get(self,request,*args,**kwargs):
        if kwargs['key'] is not None or kwargs['key'] is  None  :
            obj = User.objects.all()
            serializer = UserSerializers(obj, many=True)
        return Response(serializer.data)


    def post(self,request,*args,**kwargs):
        if kwargs['key'] is not None and kwargs['key'] != "":
            if authenticate_key(kwargs['key']):
                referal = User.objects.get(email= authenticate_key(kwargs['key']))
                if referal:
                    User.objects.filter(id=referal.id).update(is_bonus=True)
                    user = User.objects.create(email=request.data['email'], first_name=request.data['first_name'],refered_by_id=referal.id,is_bonus=True)
                    user.set_password(request.data['password'])
                    user.save()
                    return Response({'data': "sign up sucessfull with referance"}, status=status.HTTP_200_OK)
                else:
                    return Response({'data':"fake referance id"}, status=status.HTTP_200_OK)
            else:
                return Response({'data': "fake referance id"}, status=status.HTTP_200_OK)


        else:
            serializer =UserSerializers(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                url_key =generate_secretkey(serializer.data['email'])
                referal_url = str(request.get_host())+str(request.get_full_path())+str(url_key)
                return Response({'data':referal_url}, status=status.HTTP_200_OK)
            else:
                return Response({'data':serializer.errors}, status=status.HTTP_200_OK)

get_user = GetUser.as_view()

