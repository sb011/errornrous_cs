from account.models import Account
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from question.models import Answer, Like, Question, LikeQuestion
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from account.models import Account
from question.forms import AddAnswerForm, AddQuestionForm, QuestionUpdateForm, AnswerUpdateForm
# Create your views here.


def all_question_view(request, *args, **kwargs):
    context = {}
    questions = Question.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(questions, 3)
    try:
        question = paginator.page(page)
    except PageNotAnInteger:
        question = paginator.page(1)
    except EmptyPage:
        question = paginator.page(paginator.num_pages)
    context['questions'] = questions
    context['question'] = question
    return render(request, 'question/home.html', context)


def question_view(request, *args, **kwargs):
    context = {}
    user = request.user
    question_id = kwargs.get("question_id")
    # answer_id = kwargs.get("answer_id")
    if user.is_authenticated:
        try:
            question = Question.objects.get(id=question_id)
            answer = Answer.objects.filter(question=question)
            account = Account.objects.get(id=user.id)
        except Question.DoesNotExist:
            return HttpResponse("That question doesn't exist.")

        if question:
            # question.views = question.views + 1
            context['question'] = question
            # question.save()

        if answer:
            context['answer'] = answer

        answer_owner = answer.filter(auth=account)
        is_self = True
        is_friend = False
        if user.is_authenticated and question.auth != user:
            is_self = False
        elif not user.is_authenticated:
            is_self = False

        context['answer_owner'] = answer_owner
        context['is_self'] = is_self
        context['is_friend'] = is_friend
        context['BASE_URL'] = settings.BASE_URL

    return render(request, 'question/eachquestion.html', context)


def like_question_view(request, *args, **kwargs):
    user = request.user
    question_id = kwargs.get("question_id")
    if user.is_authenticated:
        if request.POST:
            id = request.POST.get('question_like')
            obj = Question.objects.get(id=id)

            if user in obj.like.all():
                obj.like.remove(user)
            else:
                obj.like.add(user)

            liked, created = LikeQuestion.objects.get_or_create(
                auth=user, question_id=id)

            if not created:
                if liked.value == 'Like':
                    liked.value = 'unlike'
                else:
                    liked.value = 'like'
            liked.save()
    return redirect('question:question', question_id)


def like_answer_view(request, *args, **kwargs):
    user = request.user
    question_id = kwargs.get("question_id")
    if user.is_authenticated:
        if request.POST:
            id = request.POST.get('answer_like')
            obj = Answer.objects.get(id=id)

            if user in obj.like.all():
                obj.like.remove(user)
            else:
                obj.like.add(user)

            liked, created = Like.objects.get_or_create(auth=user, ans_id=id)

            if not created:
                if liked.value == 'Like':
                    liked.value = 'unlike'
                else:
                    liked.value = 'like'
            liked.save()
    return redirect('question:question', question_id)


def add_question(request, *args, **kwargs):
    context = {}
    user = request.user
    auth = Account.objects.get(id=user.id)
    if user.is_authenticated:
        form = AddQuestionForm()
        if request.POST:
            form = AddQuestionForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.auth = auth
                obj.save()
                return redirect('account:view', user_id=user.id)
            else:
                context['form'] = form
    return render(request, 'question/add_question.html', context)


def remove_question(request, *args, **kwargs):
    context = {}
    user = request.user
    question_id = kwargs.get("question_id")
    if user.is_authenticated:
        try:
            question = Question.objects.get(id=question_id)
        except Exception as e:
            return HttpResponse("Question not exists!!")

        context['question'] = question
        if request.POST:
            question.delete()
            return redirect('account:view', user_id=user.id)

    return render(request, 'question/remove_question.html', context)


def add_answer(request, *args, **kwargs):
    context = {}
    user = request.user
    question_id = kwargs.get("question_id")
    auth = Account.objects.get(id=user.id)
    question = Question.objects.get(id=question_id)
    if user.is_authenticated:
        form = AddAnswerForm()
        if request.POST:
            form = AddAnswerForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.auth = auth
                obj.question = question
                obj.save()
                return redirect('question:question', question_id=question.id)
            else:
                context['form'] = form
    return render(request, 'question/add_answer.html', context)


def remove_answer(request, *args, **kwargs):
    context = {}
    user = request.user
    answer_id = kwargs.get("answer_id")
    question_id = kwargs.get("question_id")
    if user.is_authenticated:
        try:
            answer = Answer.objects.get(id=answer_id)
        except Exception as e:
            return HttpResponse("Answer not exists!!")

        context['answer'] = answer
        if request.POST:
            answer.delete()
            return redirect('question:question', question_id=question_id)
    context['question_id'] = question_id
    return render(request, 'question/remove_answer.html', context)


def question_search_view(request, *args, **kwargs):
    context = {}
    if request.method == "GET":
        search_query = request.GET.get("q")
        if len(search_query) > 0:
            search_results = Question.objects.filter(
                title__icontains=search_query)
            user = request.user
            questions = []
            for question in search_results:
                questions.append(question)
            print(questions)
            context['questions'] = questions
    return render(request, "question/search_results.html", context)


def edit_question_view(request, *args, **kwargs):
    user = request.user
    if not request.user.is_authenticated:
        return redirect("account:login")
    question_id = kwargs.get("question_id")
    question = Question.objects.get(pk=question_id)
    context = {}
    if request.POST:
        form = QuestionUpdateForm(
            request.POST, request.FILES, instance=question)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.auth = user
            obj.save()
            return redirect("question:question", question_id=question.pk)
        else:
            form = QuestionUpdateForm(request.POST, instance=question,
                                      initial={
                                          "id": question.pk,
                                          "title": question.title,
                                          "question": question.question,
                                      }
                                      )
            context['form'] = form
    else:
        form = QuestionUpdateForm(request.POST, instance=question,
                                  initial={
                                      "id": question.pk,
                                      "title": question.title,
                                      "question": question.question,
                                  }
                                  )
        context['form'] = form
    return render(request, "question/edit_question.html", context)


def edit_answer_view(request, *args, **kwargs):
    user = request.user
    if not request.user.is_authenticated:
        return redirect("account:login")
    question_id = kwargs.get("question_id")
    answer_id = kwargs.get("answer_id")
    question = Question.objects.get(pk=question_id)
    answer = Answer.objects.get(pk=answer_id)
    context = {}
    if request.POST:
        form = AnswerUpdateForm(
            request.POST, request.FILES, instance=answer)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.question = question
            obj.auth = user
            obj.save()
            return redirect("question:question", question_id=question.pk)
        else:
            form = AnswerUpdateForm(request.POST, instance=answer,
                                    initial={
                                        "id": answer.pk,
                                        "answer": answer.answer,
                                    }
                                    )
            context['form'] = form
    else:
        form = AnswerUpdateForm(request.POST, instance=answer,
                                initial={
                                    "id": answer.pk,
                                    "answer": answer.answer,
                                }
                                )
        context['form'] = form
    return render(request, "question/edit_answer.html", context)
