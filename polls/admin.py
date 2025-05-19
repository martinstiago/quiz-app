from django.contrib import admin

from .models import Question, Choice, MockTest

class ChoiceInline(admin.TabularInline):  # or admin.StackedInline
    model = Choice
    extra = 0

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(MockTest)
