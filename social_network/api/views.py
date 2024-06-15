from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer, UserSerializer
from rest_framework.decorators import api_view, permission_classes
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.throttling import UserRateThrottle

User = get_user_model()


class FriendRequestRateThrottle(UserRateThrottle):
    rate = '1000/minute'


class SignupView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email is already in use.'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=email, email=email, password=password)
        return Response({'message': 'User created successfully.'}, status=status.HTTP_201_CREATED)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key})


class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if '@' in query:
            return User.objects.filter(email__iexact=query)
        return User.objects.filter(
            Q(username__icontains=query) | 
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query)
        )

class FriendRequestListView(APIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [FriendRequestRateThrottle]
    
    def get(self, request):
        return Response(FriendRequest.objects.filter(
        Q(from_user=self.request.user) | Q(to_user=self.request.user)
    ))

    def post(self, request):
        to_user = request.data.get("to_user")
        
        print(to_user)
        if FriendRequest.objects.filter(from_user=self.request.user, to_user=to_user).exists():
            return Response("Friend request alreasy sent")  
        
        # FriendRequest.objects.filter(from_user=self.request.user, to_user=to_user).save()
        to_user = User.objects.get(id=to_user)
        friend_request =  FriendRequest(from_user=self.request.user, to_user=to_user)
        friend_request.save()
        return Response("Sent")

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_friend_request(request, pk):
    try:
        friend_request = FriendRequest.objects.get(pk=pk, to_user=request.user)
        friend_request.accepted = True
        friend_request.save()
        return Response(status=status.HTTP_200_OK)
    except FriendRequest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_friend_request(request, pk):
    try:
        friend_request = FriendRequest.objects.get(pk=pk, to_user=request.user)
        friend_request.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except FriendRequest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

class FriendsListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(
            Q(sent_requests__to_user=self.request.user, sent_requests__accepted=True) |
            Q(received_requests__from_user=self.request.user, received_requests__accepted=True)
        )

class PendingFriendRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, accepted=False)
