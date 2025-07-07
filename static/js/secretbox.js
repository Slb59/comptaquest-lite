document.addEventListener("DOMContentLoaded", function () {
const filterForms = document.querySelectorAll("form[data-autosubmit]");

filterForms.forEach((form) => {
    const fields = form.querySelectorAll("input, select");

    fields.forEach((field) => {
    field.addEventListener("change", () => {
        form.submit();
    });
    });
});
        

document.querySelectorAll(".validate-btn").forEach(button => {
    button.addEventListener("click", async (e) => {
        const btn = e.currentTarget;
        const rowId = btn.dataset.rowId;
        const checkUrl = btn.dataset.checkUrl;
        const postUrl = btn.dataset.url;

        try {
            // ✅ Vérifie l'état d'abord
            const checkRes = await fetch(checkUrl);
            const checkData = await checkRes.json();

            if (!checkData.can_validate) {
                alert(checkData.message);
                return;
            }

            // ✅ Demande la nouvelle date
            const newDate = prompt("Nouvelle date (AAAA-MM-JJ) :");
            if (!newDate) return;

            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            const postRes = await fetch(postUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": csrfToken,
                },
                body: new URLSearchParams({ new_date: newDate }),
            });

            const postData = await postRes.json();

            if (postData.success) {
                alert("Tâche validée !");
                const row = document.getElementById(rowId);
                row.classList.add("opacity-50");
                // Cross out only text cells, not the last column(actions)
                row.querySelectorAll("td:not(:last-child)").forEach(cell => {
                    cell.classList.add("line-through");
                });
            } else {
                alert(postData.message);
            }

        } catch (err) {
            alert("Une erreur s'est produite.");
            console.error(err);
        }
    });
});

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// Fonction pour récupérer le CSRF token
function getCookie(name) {
    let cookieValue = null;
if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";").map(c => c.trim());
for (let cookie of cookies) {
            if (cookie.startsWith(name + "=")) {
    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
break;
            }
        }
    }
return cookieValue;
}
});
