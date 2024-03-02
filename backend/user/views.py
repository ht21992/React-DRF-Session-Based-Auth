from .serializers import CustomUserSerializer
from user.models import CustomUser
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.contrib import auth
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed
import logging

logger = logging.getLogger(__name__)

# Get All Routes


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def getRoutes(request):
    """
    Get a list of available API routes and their corresponding methods.
    """
    routes = [
        {"url": "/api/signup/", "method": "POST"},
        {"url": "/api/login/", "method": "POST"},
        {"url": "/api/is_authenticated/", "method": "GET"},
        {"url": "/api/csrf_cookie/", "method": "GET"},
        {"url": "/api/logout/", "method": "POST"},
    ]
    return Response(routes)


@method_decorator(csrf_protect, name="dispatch")
class LoginView(APIView):
    """
    View for user authentication.

    This view handles user login by authenticating the provided credentials.
    If successful, it logs in the user and returns user details.

    Permissions:
        - AllowAny: Anyone can access this view.

    Methods:
        - POST: Authenticate user with provided credentials.

    Returns:
        - Success (200): {"success": True, "user": SerializedUser}
        - Authentication Failure (401): {"error": "Invalid credentials"}
        - Internal Server Error (500): {"error": "Something went wrong when logging in"}
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        """
        Authenticate user with provided credentials.

        Args:
            request (Request): The HTTP request object.
            format (str, optional): The requested format. Defaults to None.

        Returns:
            Response: The authentication result.
        """
        try:
            data = request.data
            email = data.get("email")
            password = data.get("password")

            user = auth.authenticate(username=email.lower(), password=password)

            if user is not None:
                auth.login(request, user)
                serializer = CustomUserSerializer(user)
                return Response({"success": True, "user": serializer.data})
            else:
                raise AuthenticationFailed("Invalid credentials")

        except AuthenticationFailed as e:
            logger.error(f"Authentication failed for user {email}: {e}")
            return Response({"error": "Invalid credentials"}, status=401)

        except Exception as e:
            logger.error(f"LoginView error: {e}")
            return Response({"error": "Something went wrong when logging in"}, status=500)


@method_decorator(ensure_csrf_cookie, name="dispatch")
class GetCSRFToken(APIView):
    """
    Obtain a CSRF token and set it in a cookie.
    """
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        """
        Get CSRF token and set it in a cookie.

        Returns:
            Response: {"success": "CSRF cookie set"}
        """
        return Response({"success": "CSRF cookie set"})


@method_decorator(csrf_protect, name="dispatch")
class LogoutView(APIView):
    """
    View for user logout.

    This view handles user logout and returns a success message upon successful logout.

    Methods:
        - POST: Logout the user.

    Returns:
        - Success (200): {"success": "Successfully logged out"}
        - Internal Server Error (500): {"error": "Something went wrong when logging out"}
    """

    def post(self, request, format=None):
        """
        Logout the user.

        Args:
            request (Request): The HTTP request object.
            format (str, optional): The requested format. Defaults to None.

        Returns:
            Response: The logout result.
        """
        try:
            auth.logout(request)
            return Response({"success": "Successfully logged out"}, status=200)
        except Exception as e:
            logger.error(f"LogoutView error: {e}")
            return Response({"error": "Something went wrong when logging out"}, status=500)


@method_decorator(csrf_protect, name="dispatch")
class CheckAuthenticatedView(APIView):
    """
    View for checking user authentication status.

    This view checks whether the user is authenticated or not.

    Permissions:
        - AllowAny: Anyone can access this view.

    Methods:
        - GET: Check the authentication status of the user.

    Returns:
        - Authenticated (200): {"isAuthenticated": True, "user": SerializedUser}
        - Not Authenticated (200): {"isAuthenticated": False, "user": {}}
        - Internal Server Error (500): {"error": "Something went wrong when checking the user's authentication status"}
    """
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        """
        Check the authentication status of the user.

        Args:
            request (Request): The HTTP request object.
            format (str, optional): The requested format. Defaults to None.

        Returns:
            Response: The authentication status result.
        """
        user = request.user
        try:
            if user.is_authenticated:
                serializer = CustomUserSerializer(user)
                return Response({"isAuthenticated": True, "user": serializer.data}, 200)
            return Response({"isAuthenticated": False, "user": {}}, 200)

        except Exception as e:
            logger.error(f"CheckAuthenticatedView error: {e}")
            return Response({"error": "Something went wrong when checking the user's authentication status"}, status=500)


@method_decorator(csrf_protect, name='dispatch')
class SignUpView(APIView):
    """
    View for user registration.

    This view handles user registration, including password validation.

    Permissions:
        - AllowAny: Anyone can access this view.

    Methods:
        - POST: Register a new user.

    Returns:
        - Success (201): {"success": True, "user": SerializedUser}
        - Password Validation Error (400): {"error": "Password validation failed: <error_message>"}
        - Passwords Do Not Match (400): {"error": "Passwords do not match"}
        - Internal Server Error (500): {"error": "Something went wrong when registering the account"}
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        """
        Register a new user.

        Args:
            request (Request): The HTTP request object.
            format (str, optional): The requested format. Defaults to None.

        Returns:
            Response: The registration result.
        """
        data = request.data
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get("password", '').strip()
        password2 = data.get('password2', '').strip()

        try:
            if not all([username, email, password, password2]):
                return Response({'error': f'Please fill all fields'}, status=400)

            if password == password2:
                try:
                    validate_password(password)
                    if CustomUser.objects.filter(email=email).exists():
                        return Response({'error': f'Email already exisits'}, status=400)
                    user = CustomUser.objects.create_user(
                        email=email, username=username, password=password)
                    auth.login(request, user)
                    serializer = CustomUserSerializer(user)
                    return Response({"success": True, "user": serializer.data}, status=201)
                except ValidationError as e:
                    error_messages = ' '.join(e.messages)
                    return Response({'error': f'{error_messages}'}, status=400)
            else:
                return Response({'error': "Passwords do not match"}, status=400)
        except Exception as e:
            logger.error(f"SignUpView error: {e}")
            return Response({'error': 'Something went wrong when registering the account'}, status=500)
