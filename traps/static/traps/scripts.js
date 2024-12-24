let currentIndex = 0;

// Fonction pour obtenir le token CSRF
const getCsrfToken = () => {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
};

// Fonction pour mettre à jour le plateau
const updateBoard = async (newIndex) => {
    const form = document.getElementById('trap-form');
    const formData = new FormData(form);
    formData.append('position_index', newIndex);

    try {
        const response = await fetch('/traps/', {
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
document.getElementById('trap-select').addEventListener('change', () => {
    currentIndex = 0;
    updateBoard(currentIndex);
});


// Initialisation
updateBoard(currentIndex);
