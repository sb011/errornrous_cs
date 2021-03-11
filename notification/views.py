from django.shortcuts import render, redirect
from notification.models import Notification
# Create your views here.


def ShowNOtification(request):
    user = request.user
    notifications = Notification.objects.filter(
        receiver=user).order_by('-date')
    Notification.objects.filter(receiver=user, is_seen=False).update(is_seen=True)
    context = {'notifications': notifications}
    return render(request, 'notification/notify.html', context)

def DeleteNotification(request, *args, **kwargs):
	user = request.user
	noti_id = kwargs.get("noti_id")
	notification = Notification.objects.filter(id=noti_id)
	notification.delete()
	return redirect('notification:show_notification')


def CountNotification(request):
	count_notifications = 0;
	if request.user.is_authenticated:
		count_notifications = Notification.objects.filter(receiver=request.user, is_seen=False).count()

	return {'count_notifications': count_notifications}