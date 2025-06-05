import datetime

from django.db import models
from django.utils import timezone
from django.utils.html import format_html
from taggit.managers import TaggableManager

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    tags = TaggableManager()
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.question_text

    def randomise_choicegs(self):
        return self.choice_set.order_by('?')
    
    def attachment_link(self):
        if self.attachment:
            return format_html('<a href="{}" download>Download</a>', self.attachment.url)
        return "(No attachment)"
    attachment_link.short_description = "Attachment"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    correct = models.BooleanField(default=0)

    def __str__(self):
        return self.choice_text
    
class MockTest(models.Model):
    questions = models.ManyToManyField(Question)
    choices = models.ManyToManyField(Choice)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.created_at)

    def max_score(self):
        return self.questions.all().count()

    def score(self):
        return self.choices.filter(correct=True).count()

    def randomise_questions(self):
        return self.questions.order_by('?')

