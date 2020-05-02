from django.urls import path, include, re_path
from . import views

app_name = 'questions'

urlpatterns = [
	path('', views.QuestionView.as_view(), name = "question"),
    path('<int:pk>/favourite/', views.AddQuestionToFavorite.as_view(), name = 'addToFavourite'),
    path('<int:pk>/vote/<int:vote>', views.VoteToQuestionClass.as_view(), name = 'voteToQuestion'),
    path('<int:pk>/vote_to_answer/<int:vote_value>', views.VoteToAnswerClass.as_view(), name = 'voteToAnswer'),
    path('<int:pk>/', views.QuestionDetailView.as_view(), name = 'question_datas'),

    path('ask/', views.AskQuestion.as_view(), name = 'ask_question'),
	path('tag/<slug:slug>/', views.TaggedQuestionView.as_view(), name = 'tag_question'),

]