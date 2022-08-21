from django.db import models
from django.db.models.signals import post_save, pre_save
from polymorphic.models import PolymorphicModel


class Team(models.Model):
    title = models.CharField(max_length=50)
    mentor = models.CharField(max_length=50)
    score = models.IntegerField()
    count = models.IntegerField(default=8)

    def __str__(self):
        return self.title


class Person(models.Model):
    first = models.CharField(max_length=50)
    second = models.CharField(max_length=50)
    middle = models.CharField(max_length=50, blank=True)
    score = models.IntegerField(default=0, )
    telegram = models.CharField(max_length=50, null=True, blank=True)
    deeplink = models.CharField(max_length=100, null=True, blank=True)
    qr = models.CharField(max_length=15, unique=True, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.second + " " + self.first + " " + self.middle


class Event(PolymorphicModel):
    """
    данный класс - наследник класс а polymorphic.models.PolymorphicModel, которые упрощает работу с полиморфными классами
    """
    title = models.CharField(max_length=100)
    max_point = models.IntegerField(default=1, null=True)
    type = models.IntegerField(null=True)
    attendance = models.ManyToManyField(Person, through='ScoreLog')
    date = models.DateField(null=True)
    time = models.TimeField(null=True)

    #
    # class Meta:
    #     abstract = True

    def __str__(self):
        return self.title


class Contest(Event):
    first = models.IntegerField(default=30,)
    second = models.IntegerField(default=20,)
    third = models.IntegerField(default=10, )
    fourth = models.IntegerField(default=5, null=True, blank=True)
    fifth = models.IntegerField(default=5, null=True, blank=True)


class EntryEvents(Event):
    pass


class Bonus(Event):
    # title = models.CharField(max_length=400)
    count = models.IntegerField(max_length=10, default=10)

    def __str__(self):
        return self.title


class BonusLog(models.Model):
    bonus = models.ForeignKey(Bonus, on_delete=models.DO_NOTHING, )
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def bonus_sum(self):
        return self.bonus.count

    def __str__(self):
        return str(self.bonus) + " \\ " + str(self.person)

    # class Meta:
    #     unique_together = (("person", "bonus"),)


def on_bonuslog_save(sender, instance, **kwargs):
    if kwargs['created']:  # just on creation (not update)
        person = instance.person
        person.score += instance.bonus.count
        person.save()
        team = person.team
        sum = instance.bonus.count / team.count * 10
        team.score += int(sum)
        team.save()


post_save.connect(on_bonuslog_save, sender=BonusLog)


class ScoreLog(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # @classmethod
    # def create(cls, event, person, created_at):
    #     log = cls(event=event, person=person, created_at=created_at)
    #     person.score += 5
    #     person.save()
    #     # do something with the book
    #     return log

    def __str__(self):
        return str(self.event) + " \\ " + str(self.person)

    # class Meta:
    #     unique_together = (("person", "event"),)


def on_scorelog_save(sender, instance, **kwargs):
    if kwargs['created']:  # just on creation (not update)
        person = instance.person
        person.score += 5
        person.save()
        team = person.team
        if team is not None:
            sum = 5 / team.count * 10
            team.score += int(sum)
            team.save()


post_save.connect(on_scorelog_save, sender=ScoreLog)


class ContestLog(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    rank = models.IntegerField()
    create = models.DateTimeField(auto_now_add=True)


def on_contestlog_save(sender, instance, **kwargs):
    if kwargs['created']:  # just on creation (not update)
        team = instance.team
        rank = instance.rank
        people = Person.objects.filter(team=team)
        # sum = 40 - rank * 10

        if rank == 1:
            sum = instance.contest.first
        elif rank == 2:
            sum = instance.contest.second
        elif rank == 3:
            sum = instance.contest.third
        elif rank == 4:
            sum = instance.contest.fourth
        elif rank == 5:
            sum = instance.contest.fifth

        else:
            sum = 5

        team.score += sum

        for person in people:
            person.score += sum
            person.save()
        team.save()


post_save.connect(on_contestlog_save, sender=ContestLog)
