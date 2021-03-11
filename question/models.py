from notification.models import Notification
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.conf import settings
from django.db.models.expressions import Value
from django.utils import timezone
from account.models import Account
from django.contrib import admin
from django.db.models.signals import post_save, post_delete
# Create your models here.


class Question(models.Model):
    title = models.CharField(max_length=30)
    question = models.CharField(max_length=300)
    auth = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='owner', blank=True)
    like = models.ManyToManyField(
        Account, related_name="question_like", default=0, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)


class Answer(models.Model):
    answer = models.CharField(max_length=300)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="question_answer", blank=True)
    auth = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="auth_answer", blank=True)
    like = models.ManyToManyField(
        Account, related_name="answer_like", default=None, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def user_add_answer(sender, instance, *args, **kwargs):
        ans = instance
        answer = ans.answer
        question = ans.question
        sender = ans.auth

        notify = Notification(answer=ans, question=question, sender=sender, receiver=ans.question.auth, notification_type=3)
        notify.save()

    def user_remove_answer(sender, instance, *args, **kwargs):
        ans = instance
        answer = ans.answer
        question = ans.question
        sender = ans.auth

        notify = Notification.objects.filter(answer=ans, question=question, sender=sender, notification_type=3)
        notify.delete()

    def __str__(self):
        return str(self.answer)

    def number_of_likes(self):
        return self.like.all().count()


LIKE_CHOICES = (
    ('like', 'like'),
    ('unlike', 'unlike'),
)


class LikeQuestion(models.Model):
    auth = models.ForeignKey(
        Account, related_name="question_auth", on_delete=models.CASCADE)
    question = models.ForeignKey(
        Question, related_name="ques", on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES,
                             default='Like', max_length=10)

    def user_like_question(sender, instance, *args, **kwargs):
        like = instance
        question = like.question
        sender = like.auth

        notify = Notification(question=question, sender=sender,
                              receiver=question.auth, notification_type=2)
        notify.save()

    def user_unlike_question(sender, instance, *args, **kwargs):
        like = instance
        question = like.question
        sender = like.auth

        notify = Notification.objects.filter(
            question=question, sender=sender, notification_type=2)
        notify.delete()

    def __str__(self):
        return str(self.POST)

    def __str__(self):
        return str(self.ans)


class Like(models.Model):
    auth = models.ForeignKey(
        Account, related_name="auth_like", on_delete=models.CASCADE)
    ans = models.ForeignKey(
        Answer, related_name="ans_like", on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES,
                             default='Like', max_length=10)

    def user_like_answer(sender, instance, *args, **kwargs):
        like = instance
        ans = like.ans
        sender = like.auth

        notify = Notification(answer=ans, sender=sender,
                              receiver=ans.auth, notification_type=1)
        notify.save()

    def user_unlike_answer(sender, instance, *args, **kwargs):
        like = instance
        ans = like.ans
        sender = like.auth

        notify = Notification.objects.filter(
            answer=ans, sender=sender, notification_type=1)
        notify.delete()

    def __str__(self):
        return str(self.POST)


post_save.connect(Like.user_like_answer, sender=Like)
post_delete.connect(Like.user_unlike_answer, sender=Like)

post_save.connect(LikeQuestion.user_like_question, sender=LikeQuestion)
post_delete.connect(LikeQuestion.user_unlike_question, sender=LikeQuestion)


post_save.connect(Answer.user_add_answer, sender=Answer)
post_delete.connect(Answer.user_remove_answer, sender=Answer)
