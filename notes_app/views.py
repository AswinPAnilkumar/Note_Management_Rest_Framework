from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from notes_app.serializers import RegisterSerializer,NoteSerializer,TaskSerializer
from django.contrib.auth.models import User
from notes_app.models import NoteDb,TaskDb
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.
class RegisterView(APIView):
    def post(self,request):
        form_data = request.data
        serializer_instance = RegisterSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({"Message":"User Registered Successfully"})
        else:
            return Response(data=serializer_instance.errors)

class UserView(APIView):
    def get(self,request):
        users = User.objects.all()
        serializer_instance = RegisterSerializer(users,many=True)
        return Response(data=serializer_instance.data)

class NoteListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request):
        notes = NoteDb.objects.filter(user=request.user)
        serializer_instance = NoteSerializer(notes,many=True)
        return Response(data=serializer_instance.data)
    
    def post(self,request):
        serializer_instance = NoteSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save(user=request.user)
            return Response({"Message":"Note Added Successfully","Note Details":serializer_instance.data})
        else:
            return Response(data=serializer_instance.errors)

class NoteRetriveUpdateDeleteView(APIView):

    permission_classes = [IsAuthenticated]
        
    def get(self,request,note_id):
        note = get_object_or_404(NoteDb,id=note_id)
        if note.user != request.user:
            raise PermissionDenied('You dont have access to this note')
        else:
            serializer_instance = NoteSerializer(note)
            return Response(data=serializer_instance.data)
    
    def put(self,request,note_id):
        note = get_object_or_404(NoteDb,id=note_id)
        if note.user != request.user:
            raise PermissionDenied('You dont have access to this note')
        else:
            serializer_instance = NoteSerializer(data=request.data,instance=note)
            if serializer_instance.is_valid():
                serializer_instance.save()
                return Response({"Message":"Note Updated Successfully"})
            else:
                return Response(data=serializer_instance.errors)
    
    def delete(self,request,note_id):
        note = get_object_or_404(NoteDb,id=note_id)
        if note.user != request.user:
            raise PermissionDenied('You dont have access to this note')
        else:
            note.delete()
            return Response({"Message":"Note Deleted Successfully"})

class TaskListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request):
        task = TaskDb.objects.filter(user=request.user)
        serializer_instance = TaskSerializer(task,many=True)
        return Response(data=serializer_instance.data)

    def post(self,request):
        serializer_instance = TaskSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save(user=request.user)
            return Response({"Message":"Task Successfully Added",
                            "Task Details":serializer_instance.data})
        else:
            return Response(data=serializer_instance.errors)

class TaskRetriveUpdateDeleteView(APIView):

    permission_classes = [IsAuthenticated]

    def get_task(self,request,task_id):
        return get_object_or_404(TaskDb,id=task_id,user=request.user)

    def get(self,request,task_id):
        # task = get_object_or_404(TaskDb,id=task_id)
        # if task.user != request.user:
        #     raise PermissionDenied('You dont have access')
        # else:
        task = self.get_task(request,task_id)
        serializer_instance = TaskSerializer(task)
        return Response(data=serializer_instance.data)

    def put(self,request,task_id):
        # task = get_object_or_404(TaskDb,id=task_id)
        # if task.user != request.user:
        #     raise PermissionDenied('You dont have access')
        # else:
        task = self.get_task(request,task_id)
        serializer_instance = TaskSerializer(data=request.data,instance=task)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({"Message":"Task Updated Successfully"})
        else:
            return Response(data=serializer_instance.errors)
    
    def delete(self,request,task_id):
        # task = get_object_or_404(TaskDb,id=task_id)
        # if task.user != request.user:
        #     raise PermissionDenied('You cant access this task')
        # else:
        task = self.get_task(request,task_id)
        task.delete()
        return Response({"Message":"Task Deleted Successfully"})
        
class Jwt_Logout(APIView):
    def post(self,request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"Message":"Successfully logout"})
        except Exception:
            return Response({"Error":"Invalid Token"})