from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from django.contrib.admin.options import TabularInline
from .models import *
from BotManager.models import *


class EventChildAdmin(PolymorphicChildModelAdmin):
    base_model = Event


class LogAdminInline(TabularInline):
    model = ScoreLog


class PromoAdminInline(TabularInline):
    fk_name = "bonus"
    model = Promocode

class ContestLogAdminInline(TabularInline):
    model = ContestLog


@admin.register(EntryEvents)
class ModelBAdmin(EventChildAdmin):
    inlines = (LogAdminInline,)
    base_model = EntryEvents  # Explicitly set


@admin.register(Bonus)
class ModelBAdmin(EventChildAdmin):
    inlines = (PromoAdminInline,)
    base_model = Bonus  # Explicitly set


@admin.register(Contest)
class ModelBAdmin(EventChildAdmin):
    base_model = Contest  # Explicitly set
    inlines = (ContestLogAdminInline,)


@admin.register(Event)
class ModelAParentAdmin(PolymorphicParentModelAdmin):
    base_model = Event  # Optional, explicitly set here.
    child_models = (EntryEvents, Contest, Bonus)
    list_filter = (PolymorphicChildModelFilter, 'date')  # This is optional.
    list_display = ['id', 'title', 'max_point']


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    model = Person
    list_display = ['id', 'second', 'first', 'team', 'score']
    # list_editable = ['score',]
    list_filter = ('team',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    model = Team
    list_display = ['title', 'mentor', 'score', ]
    list_editable = ['score']
    # list_filter = ('team',)


@admin.register(ScoreLog)
class ScoreLogAdmin(admin.ModelAdmin):
    model = ScoreLog
    list_display = ['id', 'event', 'person']
    list_editable = ['event']
    list_filter = ('event',)


@admin.register(BonusLog)
class BonusLogAdmin(admin.ModelAdmin):
    model = BonusLog
    list_display = ['id', 'bonus', 'person','created_at']
    # list_editable = ['event']
    # list_filter = ('event',)
