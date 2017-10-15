from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .methods import run_user_loading
from rest_framework import status


@api_view(['GET', 'POST'])
def update(request):
    run_user_loading(request.user)
    return Response()


@api_view(['GET', 'POST'])
def trips(request):
    data = request.user.profile.data
    if data is None:
        return Response(status=status.HTTP_402_PAYMENT_REQUIRED)
    return Response(data)
