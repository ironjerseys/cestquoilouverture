let currentIndex = 0;

// Fonction pour obtenir le token CSRF
const getCsrfToken = () => {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
};

// Fonction pour mettre à jour le plateau
const updateBoard = async (newIndex) => {
    const form = document.getElementById('opening-form');
    const formData = new FormData(form);
    formData.append('position_index', newIndex);

    try {
        const response = await fetch('', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCsrfToken()
            },
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        if (data.error) {
            alert('Erreur : ' + data.error);
        } else {
            document.getElementById('chess-board').innerHTML = data.svg;
            currentIndex = newIndex;
        }
    } catch (error) {
        console.error('Fetch error:', error);
    }
};

// Événements pour les boutons Précédent et Suivant
document.getElementById('prev-move-btn').addEventListener('click', () => {
    updateBoard(Math.max(currentIndex - 1, 0));
});

document.getElementById('next-move-btn').addEventListener('click', () => {
    updateBoard(currentIndex + 1);
});

// Événement pour charger les variantes
document.getElementById('opening-select').addEventListener('change', async function () {
    currentIndex = 0;
    const openingId = this.value;

    const response = await fetch(`/openings/variations/${openingId}/`);
    const data = await response.json();

    const variationSelect = document.getElementById('variation-select');
    variationSelect.innerHTML = '<option value="">-- Sélectionnez une variante --</option>';
    data.variations.forEach(variation => {
        const option = document.createElement('option');
        option.value = variation.id;
        option.textContent = variation.name;
        variationSelect.appendChild(option);
    });

    updateBoard(currentIndex);
});

// Initialisation
updateBoard(currentIndex);
