from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.

from users.serializers import UserSerializer, CustomTokenObtainPairSerializer
from users.models import User

from rest_framework_simplejwt.views import TokenObtainPairView

# custom view to populate JWT tokens with extra user info (username, email, is_staff)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# get profile (user) / verify authentication view
@api_view(["GET"])
@authentication_classes([JWTAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_profile(request):
    return Response({
        'user_id': request.user.id,
        'username': request.user.username,
        'email': request.user.email,
        'is_staff': request.user.is_staff
    })

# signup view
@api_view(["POST"])
def signup(request):
    serializer = UserSerializer(data={**request.data, "is_staff": False, "is_superuser": False})
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(email=request.data['email'])
        user.set_password(request.data['password'])
        user.save()
        return Response({"detail": "Your account has been created."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
