import random

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View, generic

from .models import Choice, Question, MockTest

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "mock_tests"

    def get_queryset(self):
        """Return the previous mock tests"""
        return MockTest.objects.order_by("-created_at")
    
class MockTestView(View):
    template_name = "polls/mock_test.html"

    def get(self, request, *args, **kwargs):
        question_ids = Question.objects.all().values_list('id', flat=True)
        mock_test_question_ids = random.sample(list(question_ids), k=5)
        mock_questions = Question.objects.filter(id__in=mock_test_question_ids)
        mock_test = MockTest.objects.create()
        mock_test.questions.set(mock_questions)
        mock_test.save()

        context = {
            "mock_test": mock_test,
        }
        return render(request, self.template_name, context)
    

class MockTestResultView(generic.DetailView):
    model = MockTest
    context_object_name = "mock_test"
    template_name = "polls/mock_test_result.html"


def answer_mock_test(request, mock_test_id):
    mock_test = get_object_or_404(MockTest, pk=mock_test_id)
    mock_test_question_ids = mock_test.questions.all().values_list('id', flat=True)
    
    choices_ids = []
    for question_id in mock_test_question_ids:
        choices_ids.append(request.POST[str(question_id)])

    mock_choices = Choice.objects.filter(id__in=choices_ids)
    mock_test.choices.set(mock_choices)
    mock_test.save()

    return HttpResponseRedirect(reverse("polls:mock_test_result", args=(mock_test.id,)))
