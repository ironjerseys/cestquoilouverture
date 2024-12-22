from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
import chess
import chess.svg
import re
from .models import Opening, Variation
from django.middleware.csrf import CsrfViewMiddleware

def opening_view(request):
    if request.method == 'POST':
        print("Received POST data:", request.POST)
        try:
            opening_id = request.POST.get('opening_id')
            variation_id = request.POST.get('variation_id')
            position_index = int(request.POST.get('position_index', 0))

            print("Opening ID:", opening_id)
            print("Variation ID:", variation_id)
            print("Position Index:", position_index)

            # Récupération des coups
            opening = Opening.objects.get(id=opening_id)
            opening_moves = re.sub(r"\d+\.", "", opening.moves).split()

            if variation_id:
                variation = Variation.objects.get(id=variation_id)
                variant_moves = re.sub(r"\d+\.", "", variation.moves).split()
            else:
                variant_moves = []

            # Générer le plateau combiné
            try:
                board = get_combined_board(opening_moves, variant_moves, position_index)
            except Exception as e:
                return JsonResponse({'error': f'Erreur lors de la génération du plateau : {e}'}, status=500)

            # Génère l'image SVG
            svg_data = chess.svg.board(board, size=400)

            # Renvoie les données au format JSON
            return JsonResponse({
                'svg': svg_data,
                'next_index': min(position_index + 1, len(opening_moves) + len(variant_moves) - 1),
                'prev_index': max(position_index - 1, 0)
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        openings = Opening.objects.all()
        return render(request, 'openings/opening_view.html', {'openings': openings})


    

def get_variations(request, opening_id):
    """
    Vue pour récupérer les variantes associées à une ouverture donnée.
    """
    if request.method == 'GET':
        # Récupérer l'ouverture
        opening = get_object_or_404(Opening, id=opening_id)
        
        # Récupérer les variantes associées
        variations = opening.variations.all()
        
        # Construire une réponse JSON
        response_data = [
            {'id': variation.id, 'name': variation.name, 'moves': variation.moves}
            for variation in variations
        ]
        return JsonResponse({'variations': response_data})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
def get_combined_board(opening_moves, variant_moves, position_index):
    """
    Combine les coups de l'ouverture et de la variante jusqu'à un index donné.
    """
    print("Opening moves:", opening_moves)
    print("Variant moves:", variant_moves)

    all_moves = opening_moves + variant_moves  # Combine les coups
    print("All moves:", all_moves)

    board = chess.Board()  # Initialise un plateau vide
    for move in all_moves[:position_index + 1]:  # Ajoute les coups jusqu'à l'index donné
        try:
            board.push_san(move)
        except ValueError as e:
            print(f"Erreur avec le coup {move} à l'index {position_index}: {e}")
            raise

    return board

