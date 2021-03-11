# Generated by Django 3.1.7 on 2021-03-09 06:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('question', '0009_auto_20210309_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='auth',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='auth_answer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='question_answer', to='question.question'),
        ),
    ]