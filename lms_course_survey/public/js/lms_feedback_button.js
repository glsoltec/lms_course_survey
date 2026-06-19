/**
 * Adiciona botão de Feedback na página de visualização de curso (LMS Frontend)
 * Injetado em: /lms/courses/<course_name>
 */

(function() {
	// Detectar quando está na página de curso frontend
	const detectCoursePageAndInjectButton = function() {
		// Verificar se está em página de curso (/lms/courses/...)
		if (!window.location.pathname.includes('/lms/courses/')) {
			return;
		}

		// Extrair nome do curso da URL
		const pathParts = window.location.pathname.split('/');
		const courseIndex = pathParts.indexOf('courses');
		if (courseIndex === -1 || !pathParts[courseIndex + 1]) {
			return;
		}

		const course_name = pathParts[courseIndex + 1];

		// Chamar backend para obter dados do botão
		fetch('/api/method/lms_course_survey.satisfacao.course_integration.get_course_feedback_button_data', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-Frappe-CSRF-Token': frappe.csrf_token
			},
			body: JSON.stringify({ course: course_name })
		})
		.then(response => response.json())
		.then(data => {
			if (data.message) {
				injectFeedbackButton(course_name, data.message);
			}
		})
		.catch(error => console.log('LMS Feedback Button: Erro ao buscar dados', error));
	};

	function injectFeedbackButton(course_name, button_data) {
		// Procurar por elemento container onde injetar
		// Tenta diferentes seletores comuns
		let container = document.querySelector('.course-hero') ||
						document.querySelector('.course-header') ||
						document.querySelector('[data-course-name]') ||
						document.querySelector('.page-content') ||
						document.querySelector('main') ||
						document.body;

		if (!container) return;

		// Criar card de feedback
		const card = createFeedbackCard(button_data);

		// Injetar no topo do container
		if (container.firstChild) {
			container.insertBefore(card, container.firstChild);
		} else {
			container.appendChild(card);
		}
	}

	function createFeedbackCard(button_data) {
		const card = document.createElement('div');
		card.className = 'lms-feedback-card';

		// Classes baseadas no status
		const statusClass = button_data.status === 'completed' ? 'completed' :
							button_data.show_button ? 'pending' : 'disabled';
		card.classList.add('status-' + statusClass);

		// HTML do card
		if (!button_data.show_button && button_data.reason === 'not_completed') {
			// Mostrar progresso
			card.innerHTML = `
				<div class="feedback-card-content">
					<div class="feedback-icon">⏰</div>
					<div class="feedback-text">
						<h4>Complete o curso para responder feedback</h4>
						<p>${button_data.message}</p>
					</div>
				</div>
			`;
		} else if (button_data.show_button) {
			// Mostrar botão
			const btnClass = button_data.status === 'completed' ? 'btn-success' : 'btn-primary';
			const icon = button_data.status === 'completed' ? '✓' : '📋';

			card.innerHTML = `
				<div class="feedback-card-content">
					<div class="feedback-icon">${icon}</div>
					<div class="feedback-text">
						<h4>${button_data.message}</h4>
					</div>
					<div class="feedback-action">
						<button class="feedback-button ${btnClass}" onclick="window.open('${button_data.feedback_url}', '_blank')">
							${button_data.button_text} →
						</button>
					</div>
				</div>
			`;
		} else {
			// Não logado ou não inscrito
			card.innerHTML = `
				<div class="feedback-card-content">
					<div class="feedback-icon">🔒</div>
					<div class="feedback-text">
						<h4>Feedback não disponível</h4>
						<p>${button_data.message}</p>
					</div>
				</div>
			`;
		}

		return card;
	}

	// Injetar estilos CSS
	function injectStyles() {
		if (document.getElementById('lms-feedback-styles')) return;

		const style = document.createElement('style');
		style.id = 'lms-feedback-styles';
		style.textContent = `
			.lms-feedback-card {
				margin: 20px 0;
				padding: 20px;
				border-radius: 8px;
				background: #f8f9fa;
				border-left: 4px solid #6c757d;
				box-shadow: 0 2px 4px rgba(0,0,0,0.08);
				font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
			}

			.lms-feedback-card.status-pending {
				background: #e3f2fd;
				border-left-color: #2196F3;
			}

			.lms-feedback-card.status-completed {
				background: #e8f5e9;
				border-left-color: #4CAF50;
			}

			.lms-feedback-card.status-disabled {
				background: #fff3e0;
				border-left-color: #FF9800;
			}

			.feedback-card-content {
				display: flex;
				align-items: center;
				gap: 16px;
			}

			.feedback-icon {
				font-size: 32px;
				min-width: 40px;
				text-align: center;
			}

			.feedback-text {
				flex: 1;
			}

			.feedback-text h4 {
				margin: 0 0 4px 0;
				font-size: 16px;
				font-weight: 600;
				color: #333;
			}

			.feedback-text p {
				margin: 0;
				font-size: 14px;
				color: #666;
			}

			.feedback-action {
				margin-left: auto;
			}

			.feedback-button {
				padding: 10px 20px;
				border: none;
				border-radius: 4px;
				font-size: 14px;
				font-weight: 600;
				cursor: pointer;
				transition: all 0.3s ease;
				white-space: nowrap;
			}

			.feedback-button.btn-primary {
				background: #2196F3;
				color: white;
			}

			.feedback-button.btn-primary:hover {
				background: #1976D2;
				transform: translateY(-2px);
				box-shadow: 0 4px 8px rgba(33, 150, 243, 0.3);
			}

			.feedback-button.btn-success {
				background: #4CAF50;
				color: white;
			}

			.feedback-button.btn-success:hover {
				background: #45a049;
				transform: translateY(-2px);
				box-shadow: 0 4px 8px rgba(76, 175, 80, 0.3);
			}

			.feedback-button:active {
				transform: translateY(0);
			}

			@media (max-width: 768px) {
				.feedback-card-content {
					flex-direction: column;
					align-items: flex-start;
				}

				.feedback-action {
					margin-left: 0;
					width: 100%;
				}

				.feedback-button {
					width: 100%;
					text-align: center;
				}
			}
		`;
		document.head.appendChild(style);
	}

	// Executar quando DOM está pronto
	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', function() {
			injectStyles();
			detectCoursePageAndInjectButton();
		});
	} else {
		injectStyles();
		detectCoursePageAndInjectButton();
	}

	// Re-verificar se página mudar (SPA)
	const observer = new MutationObserver(function() {
		if (window.location.pathname.includes('/lms/courses/')) {
			detectCoursePageAndInjectButton();
		}
	});

	observer.observe(document.body, {
		childList: true,
		subtree: true
	});
})();
