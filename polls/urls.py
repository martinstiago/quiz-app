from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),    
    path("mock_tests/", views.MockTestView.as_view(), name="start_mock_test"),
    path("mock_tests/<int:mock_test_id>", views.answer_mock_test, name="answer_mock_test"),
    path("mock_tests/<int:pk>/result/", views.MockTestResultView.as_view(), name="mock_test_result"),
    path("start-mock-test/", views.StartMockTestView.as_view(), name="start_mock_test"),
    path("mock_tests/tag/<slug:tag_slug>/", views.MockTestView.as_view(), name="mock_test_by_tag"),
]

