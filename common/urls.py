from django.urls import path

from common.views import CategoryListView, ChoiceCreateView, QuizListView, SearchView

urlpatterns = [
    path("category/list", CategoryListView.as_view(), name="category-list"),
    path("quiz/list", QuizListView.as_view(), name="quiz-list"),
    path("quiz/send-vote", ChoiceCreateView.as_view(), name="quiz-send-vote"),
    path('search/', SearchView.as_view(), name='search'),

]
