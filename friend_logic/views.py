from rest_framework import generics, status
from rest_framework.response import Response

from django.utils import timezone
from datetime import timedelta

from friend_logic.serializers import FriendRequestSerializer

from user_auth.models import User

from friend_logic.models import FriendRequest

from friend_logic.models import FriendList

from search_user.serializers import UserSerializer

from social_media_app.custome_decorator import validate_registered_user_uuid

from social_media_app.utils import CustomPageNumberPagination

from friend_logic.constants import RequestAction,RECEIVER_EMAIL_ID,SENDER_EMAIL_ID

from social_media_app.constants import USER_ID

from social_media_app.custom_exception import SocialMediaAppException


class FriendRequestView(generics.CreateAPIView):
    """
    Class for sending Friend Request
    """
    serializer_class = FriendRequestSerializer

    @validate_registered_user_uuid
    def create(self, request, *args, **kwargs):
        sender_id = kwargs.get(USER_ID)
        # as there is none other thing than email also user id here doesn't make any sense
        receiver_id = request.data.get(RECEIVER_EMAIL_ID)
        try:
            receiver = User.objects.get(email=receiver_id)

            if receiver.id == sender_id:
                return Response({'error': "You can't send request to yourself"},
                                status=status.HTTP_400_BAD_REQUEST)

            # Check if the user has sent more than 3 requests in the last minute
            one_minute_ago = timezone.now() - timedelta(minutes=1)
            sender = User.objects.get(id=sender_id)
            recent_requests = FriendRequest.objects.filter(sender=sender, timestamp__gte=one_minute_ago).count()
            if recent_requests >= 3:
                return Response({'error': 'More than 3 request can be sent in a minute.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
            # Check if a friend request already exists
            if FriendRequest.objects.filter(sender=sender, receiver=receiver):
                return Response({'error': 'Friend request already sent.'}, status=status.HTTP_400_BAD_REQUEST)

            friend_request = FriendRequest(sender=sender, receiver=receiver)
            friend_request.save()
            return Response("Request Sent", status=status.HTTP_201_CREATED)

        except Exception as err:
            raise SocialMediaAppException(message=f'Some error occurred: {err}')



class FriendRequestActionView(generics.GenericAPIView):
    """
    Accept or Reject Friend Request
    """

    @validate_registered_user_uuid
    def post(self,request, *args, **kwargs):

        receiver_id = kwargs.get(USER_ID)
        sender_id = request.data.get(SENDER_EMAIL_ID)
        try:
            receiver = User.objects.get(id=receiver_id)
            sender = User.objects.get(email=sender_id)
            try:
                friend_request = FriendRequest.objects.get(sender=sender, receiver=receiver)
            except FriendRequest.DoesNotExist:
                return Response({'error': 'Friend request not found.'}, status=status.HTTP_404_NOT_FOUND)

            action = request.data.get('action')
            if action == RequestAction.ACCEPT.value:
                friend_request.status = 'accepted'
                # Get or create FriendList objects for sender and receiver
                sender_friend_list, _ = FriendList.objects.get_or_create(user=friend_request.sender)
                receiver_friend_list, _ = FriendList.objects.get_or_create(user=friend_request.receiver)

                # Add each other as friends
                sender_friend_list.add_friend(friend_request.receiver)
                receiver_friend_list.add_friend(friend_request.sender)
                response = "Accepted"

            elif action == RequestAction.REJECT.value:
                friend_request.status = 'rejected'
                response = "Rejected"
            else:
                return Response({'error': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)

            friend_request.save()
            return Response(f"{response} Friend Request", status=status.HTTP_200_OK)

        except Exception as err:
            raise SocialMediaAppException(message=f'Some error occurred: {err}')


class FriendsListView(generics.ListAPIView):
    """
    List all the Friends.
    """
    serializer_class = UserSerializer
    pagination_class = CustomPageNumberPagination

    @validate_registered_user_uuid
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        try:
            user = self.kwargs.get(USER_ID)
            friend_list = FriendList.objects.get(user=user)
            return friend_list.friends.all()
        except Exception as err:
            raise SocialMediaAppException(message=f'Some error occurred: {err}')


class PendingFriendRequestsView(generics.ListAPIView):
    """
    List all the request which are still pending.
    """
    serializer_class = FriendRequestSerializer
    pagination_class = CustomPageNumberPagination


    @validate_registered_user_uuid
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        user = self.kwargs.get(USER_ID)
        return FriendRequest.objects.filter(receiver=user, status='sent')

    def get(self, request, *args, **kwargs):
        """
        Override the GET method to filter response data.
        """
        response = super().get(request, *args, **kwargs)
        data = response.data

        # Process the results to include only sender's email and name
        filtered_results = []

        for result in data.get('results', []):

            sender = result['sender']
            sender_user = User.objects.get(id=sender)
            filtered_result = {

                    'name': sender_user.name,
                    'email': sender_user.email

            }
            filtered_results.append(filtered_result)

        # Replace the original results with filtered results
        data['results'] = filtered_results

        return Response(data)

