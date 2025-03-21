from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer,PostSerializer,PetPalSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import Post,PetPal,Doctor, Appointment,PostLike,UserInformations
from rest_framework import viewsets
from .permissions import IsReviewUserorReadoOnly,IsAdminorReadOnly,IsAuthenticatedOrReadOnly
from rest_framework import permissions
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.shortcuts import redirect
from rest_framework_simplejwt.views import TokenObtainPairView
# Create your views here.
from .serializers import DoctorSerializer, AppointmentSerializer, UserSerializer, UserInformationsSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.contrib.auth.models import User

import random
from rest_framework.pagination import PageNumberPagination
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
class CustomPagination(PageNumberPagination):
    page_size = 5

class PostListCreate(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset().order_by('?')  # Shuffle the queryset
        return queryset

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)
            
   

class PostDetailView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    def  get_queryset(self):
        pk = self.kwargs.get('pk')
        # user=self.request.user
        return Post.objects.filter(id=pk)
    
class UserInformationView(generics.ListCreateAPIView):
    serializer_class = UserInformationsSerializer
    queryset = UserInformations.objects.all()
    permission_classes = [AllowAny]

class ProfileUpdateView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        # Return the user object of the currently authenticated user
        return self.request.user

    def update(self, request, *args, **kwargs):
        # Update the current user profile
        return super().update(request, *args, **kwargs)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = request.user
        if user.is_authenticated:
            if Doctor.objects.filter(user=user).exists():
                return redirect('/doc/')
            return redirect('/home/')  # Redirect to home or wherever for non-doctors
        return response

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    # print(queryset)
    

# class PostListCreate(generics.ListCreateAPIView):
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthenticated]
#     queryset = Post.objects.all()
    # def get_queryset(self):
    #     user = self.request.user
    #     # return Post.objects.all()
    #     # print(Post.objects.filter(author=user))
    #     return Post.objects.filter(author=user)
    
    # def perform_create(self,serializer):
    #     if serializer.is_valid():
    #         serializer.save(author=self.request.user)
    #     else:
    #         print(serializer.errors)
            
class PostDelete(generics.DestroyAPIView):
    # queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    
    def  get_queryset(self):
        user = self.request.user
        # return Post.objects.all()
        return Post.objects.filter(author=user)
    
        
    
class PetPalAV(generics.ListCreateAPIView):
    queryset = PetPal.objects.all()
    serializer_class = PetPalSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_create(self,serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)
    
class PetPalDeleteAV(generics.RetrieveUpdateDestroyAPIView):
    # queryset = PetPal.objects.filter(author=)
    serializer_class = PetPalSerializer
    permission_classes = [IsAuthenticated,IsReviewUserorReadoOnly]
    
    def get_queryset(self):
        
        return PetPal.objects.filter(author=self.request.user)
    
    
class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            return Doctor.objects.filter(user=user).exists()
        return False

@api_view(['GET'])
def check_doctor_status(request):
    if Doctor.objects.filter(user=request.user).exists():
        return Response({'status': 'Doctor'})
    return Response({'status': 'Not a Doctor'})

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = DoctorSerializer
class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentSerializer
    def create(self, request, *args, **kwargs):
        try:
            print("Incoming request data:", request.data)  # Log request data
            return super().create(request, *args, **kwargs)
        except Exception as e:
            print(e)


# @method_decorator(csrf_exempt, name='dispatch')  # Disables CSRF for this view
# class AppointmentAPIView(APIView):
#     permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access

#     def get(self, request):
#         appointments = Appointment.objects.all()
#         serializer = AppointmentSerializer(appointments, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = AppointmentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)  # Associate appointment with user
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)
    
class GetInfo(generics.ListCreateAPIView):
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        return Doctor.objects.filter(user=user)
    
    
class GetUserById(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return User.objects.filter(id=pk)
    
class GetDoc(generics.ListCreateAPIView):
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]
    queryset = Doctor.objects.all()
    def get_queryset(self):
        return Doctor.objects.filter(id=self.request.user.id)
    

class GetUserInfo(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Returns the current authenticated user"""
        users = User.objects.values("id", "username") 
        print(users+"users")# Fetch all users' IDs and usernames
        return Response(users)

     
     
#  Like and unlike the posts

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'detail': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        like = PostLike.objects.get(post=post, user=request.user)
        # If the like already exists, unlike it
        like.delete()
        return Response({'detail': 'Post unliked'}, status=status.HTTP_204_NO_CONTENT)
    except PostLike.DoesNotExist:
        # If the like does not exist, create it
        PostLike.objects.create(post=post, user=request.user)
        return Response({'detail': 'Post liked'}, status=status.HTTP_201_CREATED)








from rest_framework.views import APIView

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    print("profile view")
    def get(self, request, format=None):
        # print("hi")
        user = request.user
        print("user is ",user)
        # print("Email is ",user.email)

        
            # Get the UserInformations for the authenticated user
        user_info = UserInformations.objects.get(username=user)
        # print("usdrinfo ",user_info)
        user_serializer = UserSerializer(user)
        user_info_serializer = UserInformationsSerializer(user_info)
        # print ("INFO",user_info_serializer)
        combined_data = {**user_serializer.data, **user_info_serializer.data}
        return Response(combined_data, status=status.HTTP_200_OK)
        # except UserInformations.DoesNotExist:
        #     return Response({'detail': 'User information not found.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, format=None):
        user = request.user

        try:
            # Get the UserInformations for the authenticated user
            user_info = UserInformations.objects.get(username=user)
        except UserInformations.DoesNotExist:
            return Response({'detail': 'User information not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Partial update for user and user_info
        # user_serializer = UserSerializer(user, data=request.data, partial=True)
        user_info_serializer = UserInformationsSerializer(user_info, data=request.data, partial=True)

        if  user_info_serializer.is_valid():
            
            user_info_serializer.save()
            return Response(user_info_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({
                
                'user_info_errors': user_info_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
            
            
from django.core.mail import send_mail
from django.core.mail import EmailMessage



@api_view(['POST'])
def send_email(request):
    data = request.data
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    # Send email
    subject = f"New message from {name}"
    body = f"Message: {message}\n\nFrom: {email} \n\n WhiskerWag Service"

    email_msg = EmailMessage(
        subject,
        body,
        'your-email@gmail.com',  # Your email (sender)
        ['kulkarnichaitanya001@gmail.com'],  # Recipient(s)
        reply_to=[email],  # This will set the user's email as the reply-to
    )

    email_msg.send()

    return Response({'message': 'Email sent successfully!'})



class checkUsername(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        username = request.query_params.get('username')
        if not username:
            return Response({'msg': 'Username parameter is required'}, status=400)
        
        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            return Response({'msg': 'Username already taken'}, status=200)
        else:
            return Response({'msg': 'Username available'}, status=200)