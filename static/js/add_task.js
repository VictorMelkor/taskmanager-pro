    document.querySelectorAll('.add-task-btn').forEach(button => {
        button.addEventListener('click', () => {
            // Encontra o container da coluna
            const columnCard = button.closest('.column-card');
            if (!columnCard) return;

            // Encontra o container das tasks dentro da coluna
            const tasksContainer = columnCard.querySelector('.tasks-container');
            if (!tasksContainer) return;

            // Impede que abra múltiplos inputs na mesma coluna
            if (tasksContainer.querySelector('.task-input')) return;

            // Cria o card da task com input
            const taskCard = document.createElement('section');
            taskCard.classList.add('task-card');

            const input = document.createElement('input');
            input.type = 'text';
            input.placeholder = 'Nome da tarefa...';
            input.classList.add('task-input');

            taskCard.appendChild(input);
            tasksContainer.prepend(taskCard);
            input.focus();

            const submitTask = () => {
                const name = input.value.trim();
                if (!name) {
                    taskCard.remove();
                    return;
                }

                // Pega a URL para adicionar a task do data attribute do columnCard
                const url = columnCard.dataset.addTaskUrl;
                if (!url) {
                    alert('URL para adicionar tarefa não configurada.');
                    taskCard.remove();
                    return;
                }
                
                console.log("Enviando para URL:", url, "Nome:", name);
                fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken(),
                    },
                    body: JSON.stringify({ name }),
                })
                    .then(res => res.json())
                    .then(data => {
                        if (data.success) {
                            taskCard.innerText = data.name;
                            taskCard.dataset.taskId = data.id;
                        } else {
                            alert(data.error || 'Erro ao criar tarefa.');
                            taskCard.remove();
                        }
                    })
                    .catch(err => {
                        console.error(err);
                        alert('Erro ao criar tarefa.');
                        taskCard.remove();
                    });
            };

            let submitted = false;

            input.addEventListener('keydown', e => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    if (!submitted) {
                        submitted = true;
                        submitTask();
                    }
                }
                if (e.key === 'Escape') taskCard.remove();
            });

            input.addEventListener('blur', () => {
                if (!submitted) {
                    submitted = true;
                    submitTask();
                }
            });
        });
    });

    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
