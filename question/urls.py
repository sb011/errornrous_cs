from django.urls import path
from question.views import *
app_name = "question"

urlpatterns = [
    path('', all_question_view, name="all_question"),
    path('add_question/', add_question, name="add_question"),
    path('remove_question/<question_id>',
         remove_question, name="remove_question"),
    path('search/', question_search_view, name="search"),
    path('<question_id>/', question_view, name="question"),
    path('<question_id>/add_answer/', add_answer, name="add_answer"),
    path('<question_id>/edit/', edit_question_view, name="edit_question"),
    path('<question_id>/question_like/',
         like_question_view, name="question_like"),
    path('<question_id>/like/', like_answer_view, name="like"),
    path('<question_id>/answer_edit/<answer_id>',
         edit_answer_view, name="edit_answer"),
    path('<question_id>/remove_answer/<answer_id>',
         remove_answer, name="remove_answer"),
]
