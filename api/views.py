from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

from app_main.models import Note
from .serializers import NotesSerializer, UserSerializer





@api_view(['GET'])
def get_notes(request):
    notes = Note.objects.all()
    serialized_data = NotesSerializer(instance=notes, many=True)
    return Response(data=serialized_data.data)


@api_view(['POST'])
def create_note(request):
    if request.method == 'POST':
        owner_id = request.data['owner']
        title = request.data['title']
        body = request.data['body']

        user = User.objects.get(id=owner_id)
        note = Note.objects.create(owner=user, title=title, body=body)
        note.save()
        return Response(data="Created", status=status.HTTP_201_CREATED)
    
    return Response()


@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
    serialized_data = UserSerializer(users, many=True)
    return Response(data=serialized_data.data)

@api_view(['POST'])
def create_user(request):
    username = request.data['username']
    password = request.data['password']
    email = request.data.get('email', '')
    first_name = request.data.get('first_name', '')
    last_name = request.data.get('last_name', '')

    user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
    user.save()
    return Response(data="User Created", status=status.HTTP_201_CREATED)