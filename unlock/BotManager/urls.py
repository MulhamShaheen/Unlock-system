from django.urls import path, include
from .views import *
from .models import *
from rest_framework import routers, viewsets


class VotingViewSet(viewsets.ModelViewSet):
    queryset = Voting.objects.all()
    serializer_class = PollSerializer


class QRViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QASerializer


class PromocodeViewSet(viewsets.ModelViewSet):
    queryset = Promocode.objects.all()
    serializer_class = PromocodeSerializer


class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrySerializer


router = routers.DefaultRouter()
router.register(r'polls', VotingViewSet)
router.register(r'questions', QRViewSet)
router.register(r'promocodes', PromocodeViewSet)
router.register(r'registration', RegistrationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('functions/', FunctionView.as_view(), name='index'),
    path('id/', BotConnector.as_view()),
    path('answer/', AnswersController.as_view()), # /bot/answer/
    path('promo/upload/', PromoCSV.as_view()), # /bot/answer/
]
