from django.contrib import admin

from fb_post.models import User, Post, Comment, React

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(React)
