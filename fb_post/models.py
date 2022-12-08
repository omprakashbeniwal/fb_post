from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    profile_pic = models.URLField()

    def __str__(self):
        return self.name


class Post(models.Model):
    content = models.CharField(max_length=1000)
    posted_at = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Comment(models.Model):
    content = models.CharField(max_length=1000)
    commented_at = models.DateTimeField(auto_now_add=True)
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True,
                             blank=True)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE,
                                       null=True, blank=True)

    def __str__(self):
        return self.content


class React(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True,
                             blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True,
                                blank=True)

    REACTION_CHOICES = [

        ('WO', 'WOW'),
        ('LI', 'LIT'),
        ('LO', 'LOVE'),
        ('HA', 'HAHA'),
        ('TU', 'THUMBS-UP'),
        ('TD', 'THUMBS-DOWN'),
        ('AN', 'ANGRY'),
        ('SA', 'SAD')
    ]
    reaction = models.CharField(max_length=100, choices=REACTION_CHOICES, )
    reacted_at = models.DateTimeField(auto_now_add=True)
    reacted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.reaction
