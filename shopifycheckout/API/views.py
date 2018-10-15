from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
from rest_framework.filters import SearchFilter, OrderingFilter
#from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated,\
    IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework import status
from django.core import serializers
from API.models import *
from API.serializers import *
import json
#from API.permissions import AllowOptionsAuthentication 
from django.contrib.auth.models import User



class Login(APIView):
    
    print('Step 1 in direct view.')
    #permission_classes = AllowOptionsAuthentication
    queryset = User.objects.all()
    @csrf_exempt
    def post(self, request, format=None):
        
        print('I am here.')
        # import pdb
        # pdb.set_trace()
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            token = Token.objects.get_or_create(user=user)
            return Response(
        	{
            'status': 'success',
            'statusCode': status.HTTP_201_CREATED,
            'message': 'Login successfully',
            'token': token[0].key,
            "id": user.id,
        }, status=status.HTTP_201_CREATED)
        else:
            return Response({
            'status': 'unauthorized',
            'statusCode': status.HTTP_401_UNAUTHORIZED,
            'message': 'Username or password is invalid'
        }, status=status.HTTP_401_UNAUTHORIZED)


class UserManagement(APIView):

    def post(self, request,format=None):
        
        
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)
        firstname = data.get('firstname',None)
        lastname = data.get('lastname',None)
        email = data.get('email',None)
        phone_number = data.get('phoneNumber',None)
        if username and  password and firstname and lastname and  email and phone_number:
            user = User.objects.create_user(username=username,
                                 email=email,
                                 password=password,
                                 last_name=lastname,
                                 first_name=firstname
                                )
            Profile.objects.create(user=user,phone_number=phone_number)

            return Response(
            {
                'status': 'success',
                'statusCode': status.HTTP_201_CREATED,
                'message':'successfully UserCreated',
                
            }, status=status.HTTP_201_CREATED)

        else:
            return Response({
            'status': 'Failed',
            'statusCode': status.HTTP_401_UNAUTHORIZED,
            'message': 'Please Provide username and password firstname and lastname and email and phoneNumber'
        }, status=status.HTTP_401_UNAUTHORIZED)


# class Profilecheckout(APIView):
# 
#     def post(self, request, format=None):
#         rec = request.data
#         # print("++++++++++++",data)
#         # data_json = json.loads(data)
#         # print("---",data["first_name"])
#         # print(data.get('first_name', None))
#         # print(data.get('zip', None))
#         if len(rec) > 0 :
#             # for rec in data:
#             print(rec)
#             first_name = rec.get('first_name', None)
#             last_name = rec.get('last_name', None)
#             address1 = rec.get('address_1', None)
#             address2 = rec.get('address_2', None)
# 
#             city = rec.get('city', None)
#             state = rec.get('state', None)
#             zip_val = rec.get('zipcode', None)
#             email = rec.get('email', None)
# 
#             phone = rec.get('phone', None)
#             card_num = rec.get('card', None)
#             card_cvv = rec.get('cvv', None)
# 
#             # card_expired_month = rec.get('expiryDate', None)
#             # card_expired_year = rec.get('expiryDate', None)
#             card_expired_date = rec.get('expiryDate', None)
#             # card_expired_month = 23
#             # card_expired_year = 24
#             paypal_use = rec.get('isPaypal', None)
#             paypal_email = rec.get('paypalEmail', None)
#             paypal_pw = rec.get('paypalPassword', None)
#             if (first_name!=None and last_name!=None and address1!=None and address2!=None and city!=None\
#                 and  state!=None and zip_val!=None and email!=None and phone!=None and card_num!=None and \
#                 card_cvv!=None and card_expired_date!=None and\
#                 paypal_use!=None and paypal_email!=None and paypal_pw!=None):
#                 print("++++")
#                 Checkout.objects.create(first_name=first_name,last_name=last_name,
#                                         address1=address1,address2=address1,city=city,
#                                         state=state,zipcode=zip_val,email=email,phone=phone,
#                                         card_num=card_num,card_cvv=card_cvv,paypal_use=paypal_use,
#                                         card_expired_date=card_expired_date,paypal_email=paypal_email,
#                                         paypal_pw=paypal_pw
#                                         )
# 
#             else:
#                 print("----")
#                 return Response({
#                     'message': 'Invalid Data'
#                     },status=status.HTTP_401_UNAUTHORIZED)
# 
#             return Response({
#                 'stat': 'success',
#                 'statusCode': status.HTTP_201_CREATED,
#                 'message':'successfully Checkout Record created',
# 
#             }, status=status.HTTP_201_CREATED)
#             
#                 
#         else:
#             return Response({
#             'message': 'Unauthorized request'
#             },status=status.HTTP_401_UNAUTHORIZED)
# 
#                 
#         
#         # auth = request.META.get('HTTP_AUTHORIZATION', b'')
#         # token = auth.split(" ")
#         # print (token)
#         # token_validate = Token.objects.filter(key=token[1])[0]
#         
#         # if token_validate:
#         #     print("hiii",token_validate)
#         
#         # else:
#         #     return Response({
#         #     'message': 'Username or password is invalid'
#         # }, status=status.HTTP_401_UNAUTHORIZED)


class Createtask(APIView):
    def post(self, request, format=None):
        rec = request.data
        print(rec)
        if len(rec) > 0:
            # for rec in data:
            print(rec)
            billing_profile = rec.get('billingProfile', None)
            checkout_type = rec.get('checkoutType', None)
            type = rec.get('type', None)
            size = rec.get('size', None)

            proxy = rec.get('proxy', None)
            quantity = rec.get('quantity', None)
            site = rec.get('site', None)

            if (checkout_type != None and type != None and size != None and proxy != None and quantity != None \
                        and site != None):
                Task.objects.create(billing_profile=billing_profile, checkout_type=checkout_type,
                                    type=type, size=size, proxy=proxy,
                                    quantity=quantity, site=site)

            else:
                print("----")
                return Response({
                    'message': 'Invalid Data'
                }, status=status.HTTP_401_UNAUTHORIZED)

            return Response({
                'stat': 'success',
                'statusCode': status.HTTP_201_CREATED,
                'message': 'successfully Checkout Record created',

            }, status=status.HTTP_201_CREATED)


        else:
            return Response({
                'message': 'Unauthorized request'
            }, status=status.HTTP_401_UNAUTHORIZED)
    def get(self,request):
        queryset = Task.objects.all()
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)

class Savegmail(APIView):
    def post(self, request, format=None):
        rec = request.data
        if len(rec) > 0:
            # for rec in data:
            print(rec)
            GmailAccount.objects.all().delete()
            for rec_one in rec:
                email_address = rec_one.get('email',None)
                password = rec_one.get('password',None)
                if (email_address != None and password != None):
                    GmailAccount.objects.create(email=email_address,password=password)
                else:
                    print("----")
                    return Response({
                        'message': 'Invalid Data'
                    }, status=status.HTTP_401_UNAUTHORIZED)
            return Response({
                'stat': 'success',
                'statusCode': status.HTTP_201_CREATED,
                'message': 'successfully Checkout Record created',

            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'message': 'Unauthorized request'
            }, status=status.HTTP_401_UNAUTHORIZED)
    def get(self,request):
        queryset = GmailAccount.objects.all()
        serializer = GmailAccountSerializer(queryset, many=True)
        return Response(serializer.data)

class Proxy(APIView):
    def post(self, request, format=None):
        rec = request.data
        if len(rec) > 0:
            # for rec in data:
            print(rec)
            Proxies.objects.all().delete()
            for rec_one in rec:
                ip = rec_one.get('ip',None)
                port = rec_one.get('port',None)
                if (ip != None and port != None):
                    Proxies.objects.create(ip=ip,port=port)
                else:
                    return Response({
                        'message': 'Invalid Data'
                    }, status=status.HTTP_401_UNAUTHORIZED)
            return Response({
                'stat': 'success',
                'statusCode': status.HTTP_201_CREATED,
                'message': 'successfully Checkout Record created',

            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'message': 'Unauthorized request'
            }, status=status.HTTP_401_UNAUTHORIZED)
    def get(self,request):
        queryset = Proxies.objects.all()
        serializer = ProxySerializer(queryset, many=True)
        return Response(serializer.data)


class ShopifyURL(APIView):
    def post(self, request, format=None):
        rec = request.data
        if len(rec) > 0:
            # for rec in data:
            ShopifyUrl.objects.all().delete()
            for rec_one in rec:
                url = rec_one.get('url',None)
                if (url != None):
                    ShopifyUrl.objects.create(url=url)
                else:
                    return Response({
                        'message': 'Invalid Data'
                    }, status=status.HTTP_401_UNAUTHORIZED)
            return Response({
                'stat': 'success',
                'statusCode': status.HTTP_201_CREATED,
                'message': 'successfully Checkout Record created',

            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'message': 'Unauthorized request'
            }, status=status.HTTP_401_UNAUTHORIZED)
    def get(self,request):
        queryset = ShopifyUrl.objects.all()
        # res=[obj.url for obj in queryset]
        # return HttpResponse(json.dumps(res), content_type='application/json')
        serializer = ShopifySerializer(queryset, many=True)
        return Response(serializer.data)

