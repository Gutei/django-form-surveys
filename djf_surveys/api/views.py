from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from djf_surveys.models import Survey, UserAnswer, Answer, Question

from .serializers import SurveySerializer, AnswerSerializer, UserAnswerSerializer

class SurveyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer

    def get_queryset(self):
        '''
        for param query format follow url --> answers/?param
        in question we can using split by comma (,) if want filter list question
        date format by datefield django <year-month-date> ex:2025-08-17
        '''
        queryset = Survey.objects.all()
        slug = self.request.query_params.get('slug')

        if slug:
            queryset = queryset.filter(slug=slug)

        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = SurveySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        survey = get_object_or_404(queryset, pk=pk)
        serializer = SurveySerializer(survey)
        return Response(serializer.data)


class AnswerViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AnswerSerializer

    def get_queryset(self):
        '''
        for param query format follow url --> answers/?param
        in question we can using split by comma (,) if want filter list question
        date format by datefield django <year-month-date> ex:2025-08-17
        '''
        queryset = Answer.objects.all()
        survey = self.request.query_params.get('survey')
        question = self.request.query_params.get('questions')
        value = self.request.query_params.get('values')
        date = self.request.query_params.get('date')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')


        question_list = question.split(",") if question else None
        value_list = value.split(",") if value else None


        if survey:
            queryset = queryset.filter(user_answer__survey__slug=survey)

        if question:
            queryset = queryset.filter(question__key__in=question_list).distinct()
        
        if value:
            queryset = queryset.filter(value__in=value_list).distinct()
        
        if start_date and  end_date:
            queryset = queryset.filter(created_at__date__range=[start_date, end_date]).distinct()

        if date:
            queryset = queryset.filter(created_at__date=date).distinct()

        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = AnswerSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        answer = get_object_or_404(queryset, pk=pk)
        serializer = AnswerSerializer(answer)
        return Response(serializer.data)


class UserAnswerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer

    def list(self, request):
        serializer = UserAnswerSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        survey = get_object_or_404(self.queryset, pk=pk)
        serializer = UserAnswerSerializer(survey)
        return Response(serializer.data)
