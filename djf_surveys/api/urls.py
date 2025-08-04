from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r'surveys', views.SurveyViewSet, basename='surveys')
router.register(r'answers', views.AnswerViewSet, basename='answers')
router.register(r'user-answers', views.UserAnswerViewSet, basename='user_answers')


urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += router.urls
