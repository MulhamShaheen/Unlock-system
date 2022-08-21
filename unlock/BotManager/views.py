import csv

from django.shortcuts import render
import csv
from io import StringIO
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework import serializers
from .models import *
from ScoreManager.models import BonusLog
from ScoreManager.views import PersonSerializer


class FunctionSerializer(serializers.ModelSerializer):
    voting = 1

    class Meta:
        model = Function
        fields = ['time', 'date', 'voting']


class PollSerializer(serializers.ModelSerializer):
    choices = serializers.StringRelatedField(
        read_only=True,
        many=True,
    )

    class Meta:
        model = Voting
        fields = ['id', 'title', 'choices', 'time', 'date', 'TYPE']


class QASerializer(serializers.ModelSerializer):
    type = 2

    class Meta:
        model = Question
        fields = ['id', 'title', 'text', 'time', 'date', 'TYPE']


class PromocodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promocode
        fields = ['id', 'title', 'code', 'answer', 'photo', 'time', 'date', 'TYPE']


class RegistrySerializer(serializers.ModelSerializer):
    options = serializers.SlugRelatedField(
        read_only=True,
        many=True,
        slug_field="bot_view",
    )

    class Meta:
        model = Registration
        fields = ['id', 'title', 'text', 'options', 'time', 'date', 'TYPE']


class FunctionView(APIView):
    parser_classes = [JSONParser]

    def get(self, request):
        # print(request.GET)
        functions = Function.objects.all()
        data = []
        for fun in functions:
            if fun.TYPE == 1:  # promocode
                serializer = PromocodeSerializer(fun)
                promocode = serializer.data
                data.append(promocode)

            elif fun.TYPE == 2:  # question
                serializer = QASerializer(fun)
                question = serializer.data
                data.append(question)

            elif fun.TYPE == 3:  # poll
                serializer = PollSerializer(fun)
                question = serializer.data
                data.append(question)

            elif fun.TYPE == 4:  # registry
                serializer = RegistrySerializer(fun)
                question = serializer.data
                data.append(question)

        # serializer = PersonSerializer(person)
        # data = serializer.data
        return Response({"data": data})


class BotConnector(APIView):
    parser_classes = [JSONParser]

    def get(self, request):

        if request.GET['username'] != "":
            username = request.GET['username']
            try:
                person = Person.objects.get(telegram=username)
                serializer = PersonSerializer(person)
                data = serializer.data
                return Response({"data": data})

            except Person.DoesNotExist:
                pass

        if request.GET['deeplink'] != "":
            deeplink = request.GET['deeplink']

            try:
                person = Person.objects.get(deeplink=deeplink)
                serializer = PersonSerializer(person)
                data = serializer.data
                person.deeplink = None

                person.save()
                return Response({"data": data})

            except Person.DoesNotExist:
                pass

        return Response({'msg': 'Участник не найден'}, status=404)


class PromoCSV(APIView):
    parser_classes = [MultiPartParser]

    def put(self, request):
        file_obj = request.data['file']
        if file_obj.content_type == "text/csv":

            file = file_obj.read().decode('utf_8')
            csv_data = csv.DictReader(StringIO(file), delimiter=',')
            count = 0
            err_arr = []
            for row in csv_data:
                title = row['Title']
                event = row['Event']
                code = row['Code']
                answer = row['Answer']

                if Promocode.objects.filter(code=code, ):
                    pass
                else:
                    try:
                        promo = Promocode(
                            title=title,
                            event=event,
                            code=code,
                            answer=answer
                        )
                        promo.save()
                    except:
                        err_arr.append(row['name'])
                    count += 1
            return Response({"added": count, "err list": err_arr})

        return Response(status=400)


class AnswersController(APIView):
    parser_classes = [JSONParser]

    def post(self, request):

        if request.data["type"] == 1:
            id = request.data["id"]
            code = request.data["function_id"]
            person = Person.objects.get(id=id)
            function = Function.objects.get(id=code)
            if function.temporary and PromoLog.objects.filter(function=function):
                return Response({"msg": f"Промокод уже неактивен", "success": False})
            else:
                if function.bonus:
                    bonuslog = BonusLog(person=person, bonus=function.bonus)
                    bonuslog.save()
                log = PromoLog(person=person, function=function)
                log.save()

            return Response({"msg": f"", "success": True})

        elif request.data["type"] == 2:
            id = request.data["id"]
            function = request.data["function_id"]
            text = request.data["answer"]

            question = Question.objects.get(id=function)
            person = Person.objects.get(id=id)

            if QuestionLog.objects.filter(person=person, function=function):
                return Response({"msg": f"Вы уже ответили на этот вопрос", "success": False})

            log = QuestionLog(person=person, function=question, answer=text)
            log.save()

            return Response({"msg": f"Спасибо за ответ!", "success": True})
        #
        elif request.data["type"] == 3:
            id = request.data["id"]
            function = request.data["function_id"]
            text = request.data["answer"]

            person = Person.objects.get(id=id)
            choice = Choice.objects.get(title=text, voting=function)

            # function = Function.objects.get(id=function)

            if person.team == choice.team and choice.team:
                return Response({"msg": f"Вы не можете голосовать за своих", "success": False})

            # if ChoiceLog.objects.filter(person=person, function=function):
            #     return Response({"msg": f"Вы можете голосовать один раз", "success": False})

            # log = ChoiceLog(person=person, function=function, choice=choice)
            # log.save()
            choice.count += 1
            choice.save()
            return Response({"msg": f"Вы голосовали за {choice.title}", "success": True})

        elif request.data["type"] == 4:
            id = request.data["id"]
            function = request.data["function_id"]
            text = request.data["answer"]

            try:
                option = Options.objects.get(registration=function, title=text)
                person = Person.objects.get(id=id)
                function = Function.objects.get(id=function)

                if option.count >= option.max:
                    return Response({"msg": f"Уже все на <b>{option.title}</b> места забиты :(", "success": False})

                option.count += 1
                option.save()

                log = RegistryLog(person=person, function=function, option=option)
                log.save()

            except Options.DoesNotExist:
                pass
                return Response({"msg": f"", "success": False}, status=404)

            return Response({"msg": f"Вы записались на мероприятие <b>{option.title}</b>", "success": True})

        return Response({"data": request.data, "success": False})
