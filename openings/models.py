from django.db import models

class Opening(models.Model):
    name = models.CharField(max_length=100)
    moves = models.TextField()  # Liste des coups sous forme PGN (e.g., "1.e4 e5 2.d4 exd4 3.Nf3 Nc6")

    class Meta:
        db_table = 'Openings'
