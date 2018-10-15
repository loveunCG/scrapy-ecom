from .models import ShopifyUrl
from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User


class ShopifySerializer(serializers.ModelSerializer):
	class Meta:
		model = ShopifyUrl
		fields = ( 'id', 'url')

class ProxiesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Proxies
		fields = ('id', 'ip', 'port')

class GmailAccountSerializer(serializers.ModelSerializer):
	class Meta:
		model = GmailAccount
		fields = ('id', 'email', 'password')

class CheckoutSerializer(serializers.ModelSerializer):
	class Meta:
		model = Checkout
		fields = ('id', 'first_name', 'last_name', 'address1', 'address2','city','state','zipcode','email','phone','card_num','card_cvv','card_expired_date','paypal_use','paypal_email','paypal_pw')



class TaskSerializer(serializers.ModelSerializer):
    #site = serializers.PrimaryKeyRelatedField(read_only=True)
    #proxy = serializers.PrimaryKeyRelatedField(read_only=True)
    #checkout =  serializers.PrimaryKeyRelatedField(read_only=True)

	site = ShopifySerializer(read_only=True)
	proxy = ProxiesSerializer(read_only=True)
	checkout = CheckoutSerializer(read_only=True)
    

	class Meta:
		model = Task
		fields = ('id','size' ,'product', 'start_time', 'quantity','completed_date' , 'keyword', 'checkout_type','status','action', 'checkout', 'proxy', 'site')



class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = ( 'user', 'phone_number', 'profile_image')
		
		
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User	
		fields = '__all__'	



