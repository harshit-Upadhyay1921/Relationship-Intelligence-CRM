from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import GoogleLoginSerializer
from .services import GoogleAuthService


class GoogleLoginView(APIView):

    permission_classes = []

    def post(self, request):
        serializer = GoogleLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = GoogleAuthService.authenticate_google_user(
            serializer.validated_data["id_token"],
            serializer.validated_data["access_token"],
        )
        if user is None:
            return Response(
                {"detail": "Invalid Google token."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )
    

# Google ID Token:
# Used only once to verify the user's identity during login.
#
# Google Access Token:
# Stored for calling Google APIs (e.g. Google People API for contact sync).
#
# JWT Access/Refresh Tokens:
# Issued by our backend and used for authenticating all CRM API requests.


# Google-specific data is stored separately from the User model.
# This keeps authentication independent from third-party integrations and
# makes it easy to support additional providers (Microsoft, LinkedIn, etc.)
# without modifying the User schema.