from django.db import models

class Opening(models.Model):
    name = models.CharField(max_length=100)
    moves = models.TextField()  # Liste des coups sous forme PGN (e.g., "1.e4 e5 2.d4 exd4 3.Nf3 Nc6")

    class Meta:
        db_table = 'Openings'

    def __str__(self):
        return self.name


class Variation(models.Model):
    name = models.CharField(max_length=100)
    moves = models.TextField()  # Liste des coups spécifiques à la variante
    opening = models.ForeignKey(Opening, on_delete=models.CASCADE, related_name='variations')

    class Meta:
        db_table = 'Variations'

    def __str__(self):
        return f"{self.name} (Variante de {self.opening.name})"
