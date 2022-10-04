from django.db import models
from jsonfield import JSONField


class WorkerResult(models.Model):
    clue_added = models.IntegerField(default=0)
    blog_created = models.BooleanField(default=False)
    data = JSONField()

    def __str__(self):
        return f"{self.clue_added}"


class subscribe(models.Model):
    emailsub = models.EmailField(max_length=200)

    def __str__(self):
        return self.emailsub


class ClueMain(models.Model):
    clue = models.CharField(max_length=9999999, null=True)
    answer = models.CharField(max_length=9999999, null=True)
    year = year = models.CharField(max_length=9999999, null=True, blank=True)
    publish_date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.clue}"


# class Clue(models.Model):
#     clue = models.CharField(max_length=9999999)

#     def __str__(self):
#         return f"{self.clue}"


# class Word(models.Model):
#     clue = models.ForeignKey(Clue, on_delete=models.CASCADE)
#     word = models.CharField(max_length=9999999, null=True, blank=True)
#     year = models.CharField(max_length=9999999, null=True, blank=True)
#     publish_date = models.DateField(auto_now_add=True)

#     def serialize(self):
#         return {
#             "id": self.id,
#             "word": self.word,
#         }

#     def __str__(self):
#         return f"{self.word}"


class Blog(models.Model):
    title = models.CharField(max_length=9999999)
    image = models.ImageField(default="images/Capture.png")
    active = models.BooleanField(default=False)
    clue_count = models.IntegerField(default=0)
    publish_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"


class BlogClue(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    clue = models.ForeignKey(ClueMain, on_delete=models.CASCADE)
    publish_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.blog}"
