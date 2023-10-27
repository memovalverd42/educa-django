from django.shortcuts import get_object_or_404
from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from ..models import Subject, Course
from .serializers import SubjectSerializer, CourseSerializer, \
    CourseWithContentsSerializer
from .permissions import IsEnrolled


class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    
class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    
# class CourseListView(generics.ListAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer
    
class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
    @action(detail=True,
            methods=['post'],
            authentication_classes=[IsAuthenticated],
            permission_classes=[IsAuthenticated])
    def enroll(self, request: HttpRequest, *args, **kwargs):
        course = self.get_object()
        course.students.add(request.user)
        return Response({
            'enrolled': True
        })
        
    @action(detail=True,
            methods=['get'],
            serializer_class=CourseWithContentsSerializer,
            authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated, IsEnrolled])
    def contents(self, request: HttpRequest, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class CourseEnrollView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request: HttpRequest, pk: int, format=None):
        course = get_object_or_404(Course, pk=pk)
        course.students.add(request.user)
        return Response({
            'enrolled': True
        })