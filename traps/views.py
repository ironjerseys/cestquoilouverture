from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
import chess
import chess.svg
import re
from .models import Traps
from django.middleware.csrf import CsrfViewMiddleware

def traps_view(request):
    if request.method == 'POST':
        print(f"Trap ID: {request.POST.get('trap_id')}, Position Index: {request.POST.get('position_index')}")
        print("Received POST data:", request.POST)
        try:
            # Récupère les données du formulaire
            trap_id = request.POST.get('trap_id')  # Utilisez 'trap_id'
            position_index = int(request.POST.get('position_index', 0))

            # Récupère le piège correspondant
            trap = Traps.objects.get(id=trap_id)  # Utilisez 'trap'
            moves = trap.moves

            # Nettoie les numéros de coups
            moves = re.sub(r"\d+\.", "", moves).split()

            # Vérifie les limites de l'index
            if position_index < 0:
                position_index = 0
            if position_index >= len(moves):
                position_index = len(moves) - 1

            # Génère le plateau à partir des coups jusqu'à la position actuelle
            board = chess.Board()
            for move in moves[:position_index + 1]:
                try:
                    board.push_san(move)
                except Exception as e:
                    print(f"Erreur avec le coup {move} à l'index {position_index}: {e}")
                    raise e

            # Génère l'image SVG
            svg_data = chess.svg.board(board, size=400)

            # Renvoie les données au format JSON
            return JsonResponse({
                'svg': svg_data,
                'next_index': min(position_index + 1, len(moves) - 1),
                'prev_index': max(position_index - 1, 0)
            })

        except Traps.DoesNotExist:
            return JsonResponse({'error': 'Trap not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        traps = Traps.objects.all()
        return render(request, 'traps/traps_view.html', {'traps': traps})