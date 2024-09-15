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
