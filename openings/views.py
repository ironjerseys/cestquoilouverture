from django.http import JsonResponse
from django.shortcuts import render
import chess
import chess.svg
import re
from .models import Opening
from django.middleware.csrf import CsrfViewMiddleware

def opening_view(request):
    if request.method == 'POST':
        print("Received POST data:", request.POST)
        try:
            # Récupère les données du formulaire
            opening_id = request.POST.get('opening_id')
            position_index = int(request.POST.get('position_index', 0))

            # Récupère l'ouverture correspondante
            opening = Opening.objects.get(id=opening_id)
            moves = opening.moves

            # Nettoie les numéros de coups (e.g., "1.e4 e5 2.d4 exd4" -> ["e4", "e5", "d4", "exd4"])
            moves = re.sub(r"\d+\.", "", moves).split()

            # Vérifie les limites de l'index
            if position_index < 0:
                position_index = 0
            if position_index >= len(moves):
                position_index = len(moves) - 1

            # Génère le plateau à partir des coups jusqu'à la position actuelle
            board = chess.Board()
            for move in moves[:position_index + 1]:
                board.push_san(move)

            # Génère l'image SVG
            svg_data = chess.svg.board(board, size=400)

            # Renvoie les données au format JSON
            return JsonResponse({
                'svg': svg_data,
                'next_index': min(position_index + 1, len(moves) - 1),
                'prev_index': max(position_index - 1, 0)
            })

        except Opening.DoesNotExist:
            return JsonResponse({'error': 'Ouverture non trouvée'}, status=404)
        except CsrfViewMiddleware as e:
            print("CSRF error:", e)
            return JsonResponse({'error': 'CSRF validation failed'}, status=403)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        # Pour une requête GET, affiche la page avec la liste des ouvertures
        openings = Opening.objects.all()
        return render(request, 'openings/opening_view.html', {'openings': openings})
