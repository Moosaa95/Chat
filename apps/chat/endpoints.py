from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password
import uuid
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from django.utils import timezone
from rest_framework import permissions




# third
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer,
    ChatSerializer
)
from .models import User, Token, Chat
from .authentication import TokenAuthentication

class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'User registered successfully.'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            try:
                user = User.objects.get(username=username)
                if check_password(password, user.password):
                    token, created = Token.objects.get_or_create(user=user)
                    if not created:
                        token.key = uuid.uuid4().hex
                        token.save()
                    return Response({'token': token.key}, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {'error': 'Invalid credentials.'},
                        status=status.HTTP_401_UNAUTHORIZED
                    )
            except User.DoesNotExist:
                return Response(
                    {'error': 'Invalid credentials.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            message = serializer.validated_data['message']

            if user.tokens < 100:
                return Response(
                    {'error': 'Insufficient tokens.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            # Deduct tokens
            user.tokens -= 100
            user.save()

            # Generate dummy response
            response = f"Echo: {message}" 

            # Save chat history
            Chat.objects.create(
                user=user,
                message=message,
                response=response,
                timestamp=timezone.now()
            )

            return Response(
                {'response': response, 'remaining_tokens': user.tokens},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenBalanceView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({"tokens": user.tokens}, status=status.HTTP_200_OK)