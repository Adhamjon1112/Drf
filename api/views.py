import json, uuid

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet
from django.contrib.auth import get_user_model

from app_main.models import Note
from .serializers import NoteSerializer, UserSerializer

User = get_user_model()


# @api_view(['GET', 'POST'])
# def notes(request):
#     if request.method == 'POST':
#         owner_id = request.data.get('owner')
#         title = request.data.get('title')
#         body = request.data.get('body')

#         errors = []

#         if not owner_id:
#             errors.append({"owner": "Note should have an owner"})

#         if not title:
#             errors.append({"title": "Note should have a title"})

#         if errors:
#             return Response(data=json.dumps(errors), status=status.HTTP_400_BAD_REQUEST)

#         user = User.objects.get(id=owner_id)
#         note = Note.objects.create(owner=user, title=title, body=body)
#         note.save()
#         return Response(data="Created", status=status.HTTP_201_CREATED)
#     notes = Note.objects.all()  # QuerySet[<Note object>, ...]
#     serialized_data = NoteSerializer(instance=notes, many=True)
#     return Response(data=serialized_data.data)


# @api_view(['GET', 'POST'])
# def users(request):
#     if request.method == 'POST':
#         username = request.data.get('username')
#         email = request.data.get('email')
#         first_name = request.data.get('first_name')
#         last_name = request.data.get('last_name')
#         password = request.data.get('password')

#         if username and password:
#             user = User.objects.create(
#                 username=username,
#             )
#             user.set_password(password)

#             if first_name:
#                 user.first_name = first_name

#             if last_name:
#                 user.last_name = last_name

#             if email:
#                 user.email = email

#             user.save()
#             user = UserSerializer(instance=user, many=False).data
#             return Response(data=user)
#         else:
#             return Response(data={"detail": "Username and Password are required"}, status=status.HTTP_400_BAD_REQUEST)

#     users = User.objects.all()
#     serialized_data = UserSerializer(
#         instance=users, many=True)
#     return Response(data=serialized_data.data)


# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# def note(request, id):
#     try:
#         note = Note.objects.get(id=id)
#     except:
#         note = None

#     if not note:
#         return Response(data={"detail": "No such note with this ID"})

#     if request.method == 'GET':
#         note = NoteSerializer(instance=note, many=False).data
#         return Response(data=note)

#     elif request.method == 'PUT':
#         ...

#     elif request.method == 'PATCH':
#         title = request.data.get('title') or None
#         body = request.data.get('body') or None

#         if title:
#             note.title = title

#         if body:
#             note.body = body

#         note.save()
#         note = NoteSerializer(instance=note, many=False).data

#         return Response(data=note)

#     elif request.method == 'DELETE':
#         note.delete()
#         return Response(data='Deleted', status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# def user(request, id):
#     try:
#         user = User.objects.get(id=id)
#     except:
#         user = None

#     if not user:
#         return Response(data={"detail": "No such user with this ID"})

#     if request.method == 'GET':
#         user = UserSerializer(instance=user, many=False).data
#         return Response(data=user)

#     elif request.method == 'PUT':
#         ...

#     elif request.method == 'PATCH':
#         username = request.data.get('username')
#         email = request.data.get('email')
#         first_name = request.data.get('first_name')
#         last_name = request.data.get('last_name')
#         password = request.data.get('password')

#         if username.strip() and len(User.objects.filter(username=username)) == 0:
#             user.username = username
#         else:
#             return Response(data={"detail": "User with this username already exists"},
#                             status=status.HTTP_400_BAD_REQUEST)

#         if email:
#             user.email = email

#         if first_name:
#             user.first_name = first_name

#         if last_name:
#             user.last_name = last_name

#         if password.strip():
#             user.set_password(password)

#         user.save()
#         user = UserSerializer(instance=user, many=False).data

#         return Response(data=user)

#     elif request.method == 'DELETE':
#         user.delete()
#         return Response(data='Deleted', status=status.HTTP_204_NO_CONTENT)



class UserViewSet(ViewSet):
    queryset = User.objects.all()

    @staticmethod
    def get_user(pk) -> User | None:
        try:
            user = User.objects.get(id=pk)
        except:
            user = None
        return user

    def list(self, request):
        serializer = UserSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        username = request.data.username
        password = request.data.password

        if username and password:
            user = User.objects.create(username=username)
            user.set_password(password)
            user.save()
            serializer = UserSerializer(instance=user, many=False)
            return Response(serializer.data)
        else:
            return Response({"message": "Username and Password are required to create a user"})

    def retrieve(self, request, pk):
        user = self.get_user(pk)

        if not user:
            return Response({"detail": "User not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(instance=user, many=False)
        return Response(serializer.data)

    def update(self, request, pk):
        user = self.get_user(pk)

        if user:
            username = request.data.get('username')
            password = request.data.get('password')

            if username and password:
                user.username = username
                user.set_password(password)
                user.save()
                serializer = UserSerializer(instance=user, many=False)
                return Response(serializer.data)
            else:
                return Response({"detail": "Username and Password are required"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk):
        user = self.get_user(pk)

        if user:
            username = request.data.get('username')
            password = request.data.get('password')

            if username and password:
                user.username = username
                user.set_password(password)
                user.save()
                serializer = UserSerializer(instance=user, many=False)
                return Response(serializer.data)
            else:
                return Response({"detail": "Username and Password are required"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except:
            user = None

        if not user:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class NoteViewSet(ViewSet):
    queryset = Note.objects.all()

    @staticmethod
    def get_note(pk) -> Note | None:
        try:
            note = Note.objects.get(id=pk)
        except Note.DoesNotExist:
            note = None
        return note

    def list(self, request):
        serializer = NoteSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        owner_id = request.data.get('owner')
        title = request.data.get('title')
        body = request.data.get('body')

        if owner_id and title:
            try:
                owner = User.objects.get(id=owner_id)
                note = Note.objects.create(owner=owner, title=title, body=body)
                note.save()
                serializer = NoteSerializer(instance=note, many=False)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except User.DoesNotExist:
                return Response({"detail": "Owner not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Owner and Title are required to create a note"}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        note = self.get_note(pk)

        if not note:
            return Response({"detail": "Note not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = NoteSerializer(instance=note, many=False)
        return Response(serializer.data)

    def update(self, request, pk):
        note = self.get_note(pk)

        if note:
            title = request.data.get('title')
            body = request.data.get('body')

            if title:
                note.title = title
            if body:
                note.body = body
            note.save()
            serializer = NoteSerializer(instance=note, many=False)
            return Response(serializer.data)
        else:
            return Response({"detail": "Note not found"}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk):
        note = self.get_note(pk)

        if note:
            title = request.data.get('title')
            body = request.data.get('body')

            if title:
                note.title = title
            if body:
                note.body = body
            note.save()
            serializer = NoteSerializer(instance=note, many=False)
            return Response(serializer.data)
        else:
            return Response({"detail": "Note not found"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk):
        note = self.get_note(pk)

        if not note:
            return Response({"detail": "Note not found"}, status=status.HTTP_404_NOT_FOUND)

        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)