// Script JavaScript para melhorias da interface

document.addEventListener('DOMContentLoaded', function () {
    // Validação de formulário simples
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function (e) {
            const inputs = this.querySelectorAll('input[required], textarea[required]');
            let isValid = true;

            inputs.forEach(input => {
                if (!input.value.trim()) {
                    input.style.borderColor = '#dc3545';
                    isValid = false;
                } else {
                    input.style.borderColor = '#ddd';
                }
            });

            if (!isValid) {
                e.preventDefault();
                alert('Por favor, preencha todos os campos obrigatórios!');
            }
        });
    });

    // Adiciona animação aos botões
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function () {
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 100);
        });
    });

    // Fecha alertas automaticamente após 5 segundos
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        if (alert.classList.contains('alert-success')) {
            setTimeout(() => {
                alert.style.opacity = '0';
                alert.style.transition = 'opacity 0.3s ease';
                setTimeout(() => {
                    alert.remove();
                }, 300);
            }, 5000);
        }
    });

    // Marca o link ativo na navegação
    const currentUrl = window.location.href;
    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        if (link.href === currentUrl) {
            link.style.backgroundColor = 'rgba(255, 255, 255, 0.3)';
            link.style.fontWeight = 'bold';
        }
    });
});

// Função para confirmar exclusão
function confirmarAcao(mensagem = 'Tem certeza que deseja continuar?') {
    return confirm(mensagem);
}
