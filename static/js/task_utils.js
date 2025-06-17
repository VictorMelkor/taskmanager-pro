export function setupAddTaskButton(button, columnCard, getCSRFToken) {
    button.addEventListener('click', () => {
        const tasksContainer = columnCard.querySelector('.tasks-container');
        if (!tasksContainer || tasksContainer.querySelector('.task-input')) return;

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
            if (!name) return taskCard.remove();

            const url = button.dataset.addTaskUrl || columnCard.dataset.addTaskUrl;
            if (!url) {
                alert('URL para adicionar tarefa não configurada.');
                return taskCard.remove();
            }

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
            if (e.key === 'Enter' && !submitted) {
                e.preventDefault();
                submitted = true;
                submitTask();
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
}
