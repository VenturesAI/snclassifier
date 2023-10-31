from django.db import models
from django.utils import timezone

class LogMessage(models.Model):
    message = models.CharField(max_length=300)
    log_date = models.DateTimeField("date logged", auto_now_add=True)

    def __str__(self):
        """Returns a string representation of a message."""
        date = timezone.localtime(self.log_date)
        return f"'{self.message}' logged on {date.strftime('%A, %d %B, %Y at %X')}"

class YoutubeComent(models.Model):
    author = models.CharField(max_length=300)
    text = models.CharField(max_length=300)
    video_link = models.CharField(max_length=300)
    date = models.DateTimeField("date logged")

    # def __str__(self):
    #     """Returns a string representation of a message."""
    #     date = timezone.localtime(self.log_date)
    #     return f"'{self.message}' logged on {date.strftime('%A, %d %B, %Y at %X')}"