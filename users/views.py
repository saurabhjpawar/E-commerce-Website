from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer

@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response({
            "message": "User registered successfully",
            "token": token.key
        })

    return Response(serializer.errors, status=400)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({"error": "Invalid credentials"}, status=400)

    token, created = Token.objects.get_or_create(user=user)

    return Response({
        "message": "Login successful",
        "token": token.key
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def profile(request):
    return Response({
        "username": request.user.username,
        "email": request.user.email
    })

