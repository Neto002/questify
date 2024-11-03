// Referência ao botão e ao ícone
const toggleButton = document.getElementById('darkModeToggle');
const themeIcon = document.getElementById('theme-icon');
const body = document.body;

// Verifica o estado atual do tema
let darkMode = localStorage.getItem('darkMode') || 'enabled'; // Por padrão, o modo escuro está ativado

// Define o estado inicial do ícone
if (darkMode === 'enabled') {
    body.classList.add('dark-mode');
    themeIcon.classList.remove('fa-sun');
    themeIcon.classList.add('fa-moon');
} else {
    body.classList.remove('dark-mode');
    themeIcon.classList.remove('fa-moon');
    themeIcon.classList.add('fa-sun');
}

// Alterna o modo ao clicar
toggleButton.addEventListener('click', () => {
    if (body.classList.contains('dark-mode')) {
        body.classList.remove('dark-mode');
        themeIcon.classList.remove('fa-moon');
        themeIcon.classList.add('fa-sun');
        localStorage.setItem('darkMode', 'disabled');
    } else {
        body.classList.add('dark-mode');
        themeIcon.classList.remove('fa-sun');
        themeIcon.classList.add('fa-moon');
        localStorage.setItem('darkMode', 'enabled');
    }
});

// Funções Drag and Drop
function allowDrop(event) {
    event.preventDefault();
}

function drag(event) {
    event.dataTransfer.setData("text", event.target.id);
}

function drop(event) {
    event.preventDefault();

    // Verifica se o elemento de destino é uma coluna
    if (event.target.classList.contains('board-column')) {
        const data = event.dataTransfer.getData("text");
        const task = document.getElementById(data);
        event.target.appendChild(task);
    } else if (event.target.parentElement.classList.contains('board-column')) {
        const data = event.dataTransfer.getData("text");
        const task = document.getElementById(data);
        event.target.parentElement.appendChild(task);
    }
}

// Função para abrir o modal de edição de projetos
function editProject(projectName, projectId) {
    // Preencher os campos do modal
    document.getElementById('editProjectName').value = projectName;
    document.getElementById('editProjectId').value = projectId;

    // Exibir o modal de edição de projetos
    var projectModal = new bootstrap.Modal(document.getElementById('editProjectModal'));
    projectModal.show();

    // Adicionar lógica de exclusão de projeto
    document.getElementById('deleteProjectButton').onclick = function () {
        if (confirm(`Deseja realmente excluir o projeto "${projectName}"?`)) {
            // Lógica de exclusão do projeto
            console.log(`Projeto "${projectName}" excluído`);
        }
    };
}

// Função para abrir o modal de edição de tarefas
function editTask(taskName, taskXp, taskProject) {
    // Preencher os campos do modal
    document.getElementById('editTaskName').value = taskName;
    document.getElementById('editTaskXp').value = taskXp;
    document.getElementById('editTaskProject').value = taskProject;

    // Exibir o modal de edição de tarefas
    var taskModal = new bootstrap.Modal(document.getElementById('editTaskModal'));
    taskModal.show();

    // Adicionar lógica de exclusão de tarefa
    document.getElementById('deleteTaskButton').onclick = function () {
        if (confirm(`Deseja realmente excluir a tarefa "${taskName}"?`)) {
            // Lógica de exclusão da tarefa
            console.log(`Tarefa "${taskName}" excluída`);
        }
    };
}

// Função para abrir o modal de edição de tarefas
function deleteProject(projectName, id) {
    // Preencher os campos do modal
    document.getElementById('deleteProjectLabel').value = `Deletar $(projectName)?`;
    document.getElementById('deleteProjectData').value = id;

    // Exibir o modal de edição de tarefas
    var taskModal = new bootstrap.Modal(document.getElementById('deleteProjectModal'));
    taskModal.show();

};


// Função para resgatar uma recompensa
function redeemReward(rewardName, rewardCost) {
    if (confirm(`Você deseja realmente resgatar a recompensa "${rewardName}" por ${rewardCost} XP?`)) {
        // Aqui você pode fazer uma requisição ao backend para processar o resgate
        fetch('/redeem-reward', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                reward: rewardName,
                cost: rewardCost
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(`Recompensa "${rewardName}" resgatada com sucesso!`);
            } else {
                alert(`Erro: ${data.message}`);
            }
        })
        .catch(error => {
            console.error('Erro ao resgatar a recompensa:', error);
            alert('Houve um erro ao processar o resgate. Tente novamente.');
        });
    }
}

function toggleTaskStatus(taskId, status, home) {
    window.open(`$(home)/?taskID=$(taskId)&status=$(status)`)
}
