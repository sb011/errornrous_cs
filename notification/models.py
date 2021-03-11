from django.db import models
from django.db.models.deletion import CASCADE
from account.models import Account
# Create your models here.


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        (1, 'Like'),
        (2, 'LikeQuestion'),
        (3, 'Answer'),
    )
    question = models.ForeignKey(
        'question.Question', on_delete=models.CASCADE, related_name="noti_ques", blank=True, null=True)
    answer = models.ForeignKey('question.Answer', on_delete=models.CASCADE,
                               related_name="noti_ans", blank=True, null=True)
    sender = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="noti_from_user")
    receiver = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="noti_to_user")
    notification_type = models.CharField(
        choices=NOTIFICATION_TYPES, max_length=10)
    text_preview = models.CharField(max_length=100, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
