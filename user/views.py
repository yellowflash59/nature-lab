from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer, AdvisorBookingSerializer, DetailedBookingSerializer
from .models import User, AdvisorBooking
from rest_framework import status
import jwt
import datetime
from rest_framework.decorators import api_view
from advisor.models import Advisor
from advisor.serializers import AdvisorSerializer


# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret',
                           algorithm='HS256').decode('utf-8')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response


class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response


@api_view(['POST'])
def appointment_create(request, user_id, id):
    advisor = Advisor.objects.filter(id=id).first()
    if request.method == 'POST':
        serializer = AdvisorBookingSerializer(data=request.data)
        data = {}
        if serializer.is_valid(raise_exception=True):
            serializer.save(advisor=advisor, user=user_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


def get_user(request):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    try:
        payload = jwt.decode(token, 'secret', algorithm=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')

    user = User.objects.filter(id=payload['id']).first()
    return user.id


# @api_view(['Get'])
# def booking_list(request):
#     booking = AdvisorBooking.objects.all()

#     if request.method == "GET":
#         serializer = AdvisorBookingSerializer(booking, many=True)
#         return Response(serializer.data)


@api_view(['Get'])
def advisor_list(request, user_id):
    advisor = Advisor.objects.all()

    if request.method == "GET":
        serializer = AdvisorSerializer(advisor, many=True)
        return Response(serializer.data)


@api_view(['Get'])
def booking_list(request, user_id):
    user = User.objects.get(id=user_id)
    booking = AdvisorBooking.objects.filter(user=user)

    if request.method == "GET":
        serializer = DetailedBookingSerializer(booking, many=True)
        return Response(serializer.data)
