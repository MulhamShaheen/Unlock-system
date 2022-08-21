from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from .models import *


# admin.site.register(Function)

class FunctionChildAdmin(PolymorphicChildModelAdmin):
    base_model = Function


@admin.register(Promocode)
class ModelBAdmin(FunctionChildAdmin):
    base_model = Promocode  # Explicitly set
    list_display = [ 'code', 'answer', 'temporary']
    list_editable = ['temporary']
    # list_filter = ('',)

@admin.register(Question)
class ModelBAdmin(FunctionChildAdmin):
    base_model = Question  # Explicitly set


@admin.register(Voting)
class ModelBAdmin(FunctionChildAdmin):
    base_model = Voting  # Explicitly set



@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    model = Choice
    list_display = ['title', 'count', 'voting']
    list_editable = ['count']
    list_filter = ('voting',)


class OptionInline(admin.TabularInline):
    model = Options

@admin.register(Options)
class OptionsAdmin(admin.ModelAdmin):
    model = Choice
    list_display = ['title', 'count', 'max', 'registration']
    list_editable = ['count', 'max']
    list_filter = ('registration',)

@admin.register(Registration)
class ModelBAdmin(FunctionChildAdmin):
    base_model = Registration  # Explicitly set
    inlines = (OptionInline,)



@admin.register(Function)
class FunctionParentAdmin(PolymorphicParentModelAdmin):
    base_model = Function  # Optional, explicitly set here.
    child_models = (Promocode, Question, Voting,Registration)
    list_filter = (PolymorphicChildModelFilter, 'date')  # This is optional.
    list_display = ['id', 'date', 'time']
    list_editable = ['date',]


@admin.register(PromoLog)
class RegistryLogAdmin(admin.ModelAdmin):
    model = PromoLog
    list_display = ['function', 'person', 'code','created_at']
    list_filter = ('function',)

#
@admin.register(QuestionLog)
class RegistryLogAdmin(admin.ModelAdmin):
    model = QuestionLog
    list_display = ['function', 'person', 'created_at']
    list_filter = ('function',)


# @admin.register(ChoiceLog)
# class RegistryLogAdmin(admin.ModelAdmin):
#     model = ChoiceLog
#     list_display = ['function', 'choice', 'person', 'created_at']
#     list_filter = ('choice',)


@admin.register(RegistryLog)
class RegistryLogAdmin(admin.ModelAdmin):
    model = RegistryLog
    list_display = ['option', 'person', 'created_at']
    list_filter = ('option',)

