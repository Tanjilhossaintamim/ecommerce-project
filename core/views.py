from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import LoginSerializer

# Create your views here.

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = LoginSerializer

###########################################################

# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         username = serializer.validated_data['username']
#         user = User.objects.get(username=username)
#         response = super().post(request, *args, **kwargs)
#         response.data['user'] = user.username # Add username to response data
#         return response