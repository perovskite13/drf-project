from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status, permissions
from django.http import Http404
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from .models import Echo, Pledge
from .serializers import EchoSerializer, PledgeSerializer,EchoDetailSerializer
from .permissions import IsOwnerOrReadOnly

#configure to view all projects
class ProjectList(APIView): #APIView
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self,request):
        projects = Echo.objects.all()
        serializer = EchoSerializer(projects, many = True)
        return Response(serializer.data)

    def post(self,request):
        serializer = EchoSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#configure to view specific project
class ProjectDetail(APIView): #APIView
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    # def get_object(self,pk):
    #     try:
    #         return Echo.objects.get(pk=pk)
    #     except Echo.DoesNotExist:
    #         raise Http404

    def get_object(self, pk):
        try:
            project = Echo.objects.get(pk=pk)
            self.check_object_permissions(self.request, project)
            return project
        except Echo.DoesNotExist:
            raise Http404

    def get(self,request,pk):
        project = self.get_object(pk)
        serializer = EchoDetailSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk):
        project = self.get_object(pk)
        data = request.data
        serializer = EchoDetailSerializer(
            instance=project,
            data=data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        project = self.objects.get(pk=pk)
        self.check_object_permissions(self.request, project)
        #project = self.get_object(pk)
        #how to add condition so that only owner can delete its own project, and if there are no supporters
        project.delete()
        return Response(status=status.HTTP_200_OK)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#configure to view all pledges
class PledgeList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self,request):
        pledges = Pledge.objects.all()
        serializer = PledgeSerializer(pledges, many = True)
        return Response(serializer.data)

    def post(self,request):
        serializer = PledgeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(supporter=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#configure to view specific pledge
class PledgeDetail(generics.RetrieveAPIView):
    # def get_object(self,pk):
    #     try:
    #         return Pledge.objects.get(pk=pk)
    #     except Pledge.DoesNotExist:
    #         raise Http404
    def get_object(self, pk):
        try:
            pledge = Pledge.objects.get(pk=pk)
            self.check_object_permissions(self.request, pledge)
            return pledge
        except Pledge.DoesNotExist:
            raise Http404

    def get(self,request,pk):
        pledge = self.get_object(pk)
        serializer = PledgeSerializer(pledge)
        return Response(serializer.data)
