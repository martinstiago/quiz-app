import random

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View, generic

from .forms import TagSelectForm
from .models import Choice, Question, MockTest
from taggit.models import Tag

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "mock_tests"

    def get_queryset(self):
        """Return the previous mock tests"""
        return MockTest.objects.order_by("-created_at")
    
class MockTestView(View):
    template_name = "polls/mock_test.html"

    def get(self, request, *args, **kwargs):
        tag_slug = kwargs.get("tag_slug")
        if tag_slug:
            # Filter questions by tag
            questions = Question.objects.filter(tags__slug=tag_slug).distinct()
        else:
            questions = Question.objects.all()
        question_ids = questions.values_list('id', flat=True)
        if len(question_ids) < 5:
            mock_test_question_ids = list(question_ids)
        else:
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

class StartMockTestView(View):
    template_name = "polls/start_mock_test.html"

    def get(self, request, *args, **kwargs):
        form = TagSelectForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = TagSelectForm(request.POST)
        if form.is_valid():
            tag = form.cleaned_data["tag"]
            # Redirect to a new URL with the tag slug
            return HttpResponseRedirect(reverse("polls:mock_test_by_tag", args=(tag.slug,)))
        return render(request, self.template_name, {"form": form})
