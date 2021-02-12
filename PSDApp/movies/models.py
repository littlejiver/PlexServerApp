from django.db import models


class MovieEntry(models.Model):
    MovieName = models.CharField(max_length=50)
    MovieYear = models.IntegerField()
    MovieStars = models.CharField(max_length=50)

    class Meta:
        db_table = "movie_entry"
