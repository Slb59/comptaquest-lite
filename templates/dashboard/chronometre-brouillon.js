// static/js/dashboard.js
document.addEventListener('DOMContentLoaded', function () {
    const buttons = document.querySelectorAll('.timer-button');

    buttons.forEach(button => {
        button.addEventListener('click', function () {
            const todoId = this.dataset.todoId;
            const timerDisplay = document.getElementById(`timer-${todoId}`);
            let time = 0;
            let timer = setInterval(() => {
                time++;
                timerDisplay.textContent = formatTime(time);
            }, 1000);

            this.textContent = 'Arrêter';
            this.onclick = function () {
                clearInterval(timer);
                // Envoyer la durée au serveur via AJAX
                fetch(`/update-duration/${todoId}/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': '{{ csrf_token }}'
                    },
                    body: JSON.stringify({ duration: time })
                });
                this.textContent = 'Chronomètre';
            };
        });
    });

    function formatTime(seconds) {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;
        return `${hours}h ${minutes}m ${secs}s`;
    }
});
