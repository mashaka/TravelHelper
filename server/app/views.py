from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .methods import run_user_loading

@api_view(['GET', 'POST'])
def update(request):
    run_user_loading(request.user)
    return Response()


@api_view(['GET', 'POST'])
def trips(request):
    return Response(request.user.profile.data)
