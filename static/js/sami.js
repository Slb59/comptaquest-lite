
document.addEventListener("DOMContentLoaded", function () {
    const fields = [
    "id_bedtime",
    "id_wakeup",
    "id_nonstop",
    "id_energy",
    "id_naptime",
    "id_phone",
    "id_reading",
    ];

    function calculateTotalSleep() {
        let total = 0;
    fields.forEach(function (id) {
            const field = document.getElementById(id);
    const value = parseInt(field?.value || 0);
    if (!isNaN(value)) {
        total += value;
            }
        });
    const display = document.getElementById("total-sleep");
    if (display) {
        display.textContent = total;
        }
    }

    // Recalculer à chaque changement
    fields.forEach(function (id) {
        const field = document.getElementById(id);
    if (field) {
        field.addEventListener("input", calculateTotalSleep);
        }
    });

    // Calcul initial
    calculateTotalSleep();
});

