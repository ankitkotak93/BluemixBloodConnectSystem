from django.contrib import admin
from blood.models import Question,Choice, Recepient, Donor, Hospital, Camp, Link, Post, Story, Notification

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Recepient)
admin.site.register(Donor)
admin.site.register(Hospital)
admin.site.register(Camp)
admin.site.register(Link)
admin.site.register(Post)
admin.site.register(Story)
admin.site.register(Notification)
