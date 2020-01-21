from django.db import models
from datetime import datetime
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
# Create your models here.

class Dataset(models.Model):
    name = models.TextField()


class ThreadTask(models.Model):
    name = models.TextField()
    is_done = models.BooleanField(blank=False, default=False)
    started = models.DateTimeField(default = timezone.now)
    ended = models.DateTimeField(null=True)
    log_text = models.TextField()

    def done(self):
        self.is_done = True
        self.ended = datetime.now()
        self.save()

    def log(self, message):
        self.refresh_from_db()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.log_text += '\n' + timestamp + ": " + message
        self.log_text = self.log_text.strip()
        self.save() 
        async_to_sync(get_channel_layer().group_send)(
            'taskmessages',
            {
                'type': 'task_message',
                'message': message,
                'class': 'warning',
                'timeout': 3000,
            }
        )

    def last_log(self):
        msgs = self.log_text.split('\n')
        for i in range(len(msgs) - 1, 0, -1):
            if msgs[i].strip():
                return msgs[i]
        return ""

    def __str__(self):
        return "{}".format(self.name)
