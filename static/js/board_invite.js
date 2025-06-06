document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById("invite-form");
    const responseDiv = document.getElementById("invite-response");

    if (!form) return;

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const formData = new FormData(form);
        const url = form.action;

        fetch(url, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
            },
            body: formData,
        })
        .then(res => res.json())
        .then(data => {
            if (data.link) {
                responseDiv.innerHTML = `<p>${data.message}</p><a href="${data.link}" target="_blank">${data.link}</a>`;
            } else {
                responseDiv.textContent = data.message;
            }
        })
        .catch(() => {
            responseDiv.textContent = "Erro ao gerar convite.";
        });
    });
});
