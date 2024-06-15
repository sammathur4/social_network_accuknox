from django.urls import path
from .views import (
    UserSearchView, FriendRequestListView, accept_friend_request, reject_friend_request, 
    FriendsListView, PendingFriendRequestsView,
    SignupView, CustomAuthToken
)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('friend-requests/', FriendRequestListView.as_view(), name='friend-request-list'),
    path('friend-requests/<int:pk>/accept/', accept_friend_request, name='accept-friend-request'),
    path('friend-requests/<int:pk>/reject/', reject_friend_request, name='reject-friend-request'),
    path('friends/', FriendsListView.as_view(), name='friends-list'),
    path('friend-requests/pending/', PendingFriendRequestsView.as_view(), name='pending-friend-requests'),
]
