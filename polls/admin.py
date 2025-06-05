# admin.py
from django.contrib import admin
from .models import Question, Choice, MockTest

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date', 'attachment_link')  # Shows download link in the table
    inlines = [ChoiceInline]
    fields = ('question_text', 'pub_date', 'tags', 'attachment')  # Shows upload field in the form

admin.site.register(Choice)
admin.site.register(MockTest)

