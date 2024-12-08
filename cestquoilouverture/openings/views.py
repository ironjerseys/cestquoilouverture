from django.shortcuts import render

# openings/views.py
from django.shortcuts import render
from django.http import JsonResponse
import chess
import chess.svg

from .models import Opening

def opening_view(request):
    if request.method == 'POST':
        opening_id = request.POST.get('opening_id')
        opening = Opening.objects.get(id=opening_id)
        moves = opening.moves.split()
        
        board = chess.Board()
        position_index = int(request.POST.get('position_index', 0))
        
        # Applique les coups jusqu'à l'index actuel
        for move in moves[:position_index + 1]:
            board.push_san(move)

        # Génère l'image SVG
        svg_data = chess.svg.board(board, size=400)
        return JsonResponse({'svg': svg_data, 'next_index': position_index + 1})

    openings = Opening.objects.all()
    return render(request, 'openings/opening_view.html', {'openings': openings})

