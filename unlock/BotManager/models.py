from django.db import models
from ScoreManager.models import Event, Person, Team, Bonus
from django.db.models.signals import post_save, pre_save

from polymorphic.models import PolymorphicModel


class Function(PolymorphicModel):
    TYPE = 0
    title = models.CharField(max_length=20,  default="-", null=True)
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING, null=True, blank=True)
    time = models.TimeField(auto_now=False, null=True, blank=True)
    date = models.DateField(auto_now=False, null=True, blank=True)


    def __str__(self):
        return f"{str(self.date)} {self.title}"


class Promocode(Function):
    TYPE = 1

    code = models.CharField(max_length=20, default="00000")
    answer = models.TextField(max_length=400)
    photo = models.CharField(max_length=100, null=True, blank=True)
    temporary = models.BooleanField(default=True)

    bonus = models.ForeignKey(Bonus, null=True, blank=True, on_delete=models.CASCADE)


class Question(Function):
    TYPE = 2

    text = models.TextField(max_length=400)


class Voting(Function):
    TYPE = 3

    def __str__(self):
        return self.title


class Choice(models.Model):
    voting = models.ForeignKey(Voting, related_name='choices', on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=400)
    count = models.IntegerField(default=0)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class Registration(Function):
    TYPE = 4
    text = models.TextField(max_length=500)


class Options(models.Model):
    registration = models.ForeignKey(Registration, related_name='options', on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=200)
    count = models.IntegerField(default=0)
    max = models.IntegerField(null=True, blank=True)

    @property
    def bot_view(self):
        return {"title": self.title, "count": self.count, "max": self.max}

    def __str__(self):
        return f"{str(self.registration)} | {self.title}"


class Answer(PolymorphicModel):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PromoLog(Answer):
    function = models.ForeignKey(Promocode, on_delete=models.CASCADE)

    @property
    def code(self):
        return self.function.code

    def __str__(self):
        return f"{str(self.function)} | {str(self.person)}"


def on_promolog_save(sender, instance, **kwargs):
    if kwargs['created'] or kwargs['update_fields']:  # just on creation (not update)

        if instance.function:
            function = instance.function
            # if function.bonus:

            person = instance.person
            person.score += 5
            person.save()

            team = person.team
            team.score += 5 / team.count * 10
            team.save()


post_save.connect(on_promolog_save, sender=PromoLog)


class QuestionLog(Answer):
    function = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)

    def __str__(self):
        return f"{str(self.function)} | {str(self.person)}"


class RegistryLog(Answer):
    function = models.ForeignKey(Registration, on_delete=models.CASCADE, null=True, blank=True)
    option = models.ForeignKey(Options, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{str(self.function)} | {str(self.option)} | {str(self.person)}"
