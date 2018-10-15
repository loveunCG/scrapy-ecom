from rest_framework.viewsets import ModelViewSet
from .serializers import *
from .models import Checkout, Profile, Task, GmailAccount, Proxies, ShopifyUrl
from rest_framework.decorators import detail_route, authentication_classes,\
    permission_classes
from rest_framework.authentication import BasicAuthentication
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


class CreateListMixin:
    """Allows bulk creation of a resource."""
    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True

        return super().get_serializer(*args, **kwargs)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @csrf_exempt
    def perform_login(self, request, format=None):
        print('Step 2')
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

        


class CheckoutViewSet(ModelViewSet):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer
    
    
class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer    
    
    
class TaskViewSet(CreateListMixin, ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer  
    
    
class GmailAccountViewSet(ModelViewSet):
    queryset = GmailAccount.objects.all()
    serializer_class = GmailAccountSerializer    
    
    
class ProxiesViewSet(ModelViewSet):
    queryset = Proxies.objects.all()
    serializer_class = ProxiesSerializer
    
    
        
class ShopifyUrlViewSet(ModelViewSet):
    queryset = ShopifyUrl.objects.all()
    serializer_class = ShopifySerializer
    
    
        
                
