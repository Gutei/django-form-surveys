from rest_framework import serializers
from djf_surveys.models import Survey, UserAnswer, Answer, Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['key', 'label', 'choices', 'required']


class SurveySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Survey
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    survey = serializers.CharField(source='question.survey.name')
    question = serializers.CharField(source='question.label')
    user = serializers.SerializerMethodField('get_user')

    def get_user(self, obj):
         return f'{obj.user_answer.user.username}' if obj.user_answer.user else 'AnonymousUser'

    class Meta:
        model = Answer
        fields = ['user', 'survey', 'question', 'value', 'created_at']


class UserAnswerSerializer(serializers.ModelSerializer):
    survey = serializers.CharField(source='survey.name')
    user = serializers.SerializerMethodField('get_user')
    answer_set = AnswerSerializer(many=True, read_only=True)

    def get_user(self, obj):
         return f'{obj.user.username}' if obj.user else 'AnonymousUser'

    class Meta:
        model = UserAnswer
        fields = ['survey', 'user', 'created_at', 'answer_set']
