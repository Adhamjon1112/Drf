import json

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from app_main.models import Note
from .serializers import NoteSerializer, UserSerializer

User = get_user_model()


@api_view(['GET', 'POST'])
def notes(request):
    if request.method == 'POST':
        owner_id = request.data.get('owner')
        title = request.data.get('title')
        body = request.data.get('body')

        errors = []

        if not owner_id:
            errors.append({"owner": "Note should have an owner"})

        if not title:
            errors.append({"title": "Note should have a title"})

        if errors:
            return Response(data=json.dumps(errors), status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=owner_id)
        note = Note.objects.create(owner=user, title=title, body=body)
        note.save()
        return Response(data="Created", status=status.HTTP_201_CREATED)
    notes = Note.objects.all()  # QuerySet[<Note object>, ...]
    serialized_data = NoteSerializer(instance=notes, many=True)
    return Response(data=serialized_data.data)


@api_view(['GET', 'POST'])
def users(request):
    if request.method == 'POST':
        username = request.data.get('username')
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        password = request.data.get('password')

        if username and password:
            user = User.objects.create(
                username=username,
            )
            user.set_password(password)

            if first_name:
                user.first_name = first_name

            if last_name:
                user.last_name = last_name

            if email:
                user.email = email

            user.save()
            user = UserSerializer(instance=user, many=False).data
            return Response(data=user)
        else:
            return Response(data={"detail": "Username and Password are required"}, status=status.HTTP_400_BAD_REQUEST)

    users = User.objects.all()
    serialized_data = UserSerializer(
        instance=users, many=True)
    return Response(data=serialized_data.data)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def note(request, id):
    try:
        note = Note.objects.get(id=id)
    except:
        note = None

    if not note:
        return Response(data={"detail": "No such note with this ID"})

    if request.method == 'GET':
        note = NoteSerializer(instance=note, many=False).data
        return Response(data=note)

    elif request.method == 'PUT':
        ...

    elif request.method == 'PATCH':
        title = request.data.get('title') or None
        body = request.data.get('body') or None

        if title:
            note.title = title

        if body:
            note.body = body

        note.save()
        note = NoteSerializer(instance=note, many=False).data

        return Response(data=note)

    elif request.method == 'DELETE':
        note.delete()
        return Response(data='Deleted', status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def user(request, id):
    try:
        user = User.objects.get(id=id)
    except:
        user = None

    if not user:
        return Response(data={"detail": "No such user with this ID"})

    if request.method == 'GET':
        user = UserSerializer(instance=user, many=False).data
        return Response(data=user)

    elif request.method == 'PUT':
        ...

    elif request.method == 'PATCH':
        username = request.data.get('username')
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        password = request.data.get('password')

        if username.strip() and len(User.objects.filter(username=username)) == 0:
            user.username = username
        else:
            return Response(data={"detail": "User with this username already exists"},
                            status=status.HTTP_400_BAD_REQUEST)

        if email:
            user.email = email

        if first_name:
            user.first_name = first_name

        if last_name:
            user.last_name = last_name

        if password.strip():
            user.set_password(password)

        user.save()
        user = UserSerializer(instance=user, many=False).data

        return Response(data=user)

    elif request.method == 'DELETE':
        user.delete()
        return Response(data='Deleted', status=status.HTTP_204_NO_CONTENT)