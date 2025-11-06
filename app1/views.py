from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .serializers import RegisterSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny

class ListCreateView(APIView):


    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        return [IsAuthenticated()]
    
    
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({
            'users': serializer.data,
        })
    

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
            'message': 'User Created Successfully.',
            'user': serializer.data,
        }, status=201)

        return Response({
            'error': serializer.errors,
        }, status=400)

class LoginView(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = User.objects.filter(username= username).first()

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)

            return Response({
                "message": "Login Successfully.",
                "userId": user.id,
                "refresh": str(refresh), 
                "access": str(refresh.access_token), 
            })
        
        return Response({
            'message': "Invalid Cerdentials.",
        }, status=400)
    

class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user = RegisterSerializer(user)
        return Response({"user" : user.data})
