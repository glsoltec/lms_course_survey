/**
 * Adiciona botão de Feedback na página de visualização de curso (LMS Frontend)
 * Injetado em: /lms/courses/<course_name>
 */

(function() {
	let hasBeenInjected = false;
	let currentCourse = null;

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

	function createFeedbackCard(button_data) {
		const card = document.createElement('div');
		card.className = 'lms-feedback-card';
		card.id = 'lms-feedback-card'; // ID único para evitar duplicatas

		const statusClass = button_data.status === 'completed' ? 'completed' :
							button_data.show_button ? 'pending' : 'disabled';
		card.classList.add('status-' + statusClass);

		if (!button_data.show_button && button_data.reason === 'not_completed') {
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

	function injectFeedbackButton(course_name, button_data) {
		// Evitar injetar múltiplas vezes
		if (document.getElementById('lms-feedback-card')) {
			document.getElementById('lms-feedback-card').remove();
		}

		const container = document.querySelector('.course-hero') ||
						  document.querySelector('.course-header') ||
						  document.querySelector('[data-course-name]') ||
						  document.querySelector('.page-content') ||
						  document.querySelector('main') ||
						  document.querySelector('article') ||
						  document.querySelector('[role="main"]');

		if (!container) {
			console.warn('LMS Feedback Button: Container não encontrado');
			return;
		}

		const card = createFeedbackCard(button_data);
		if (container.firstChild) {
			container.insertBefore(card, container.firstChild);
		} else {
			container.appendChild(card);
		}
	}

	function fetchAndInjectButton() {
		// Verificar se está em página de curso (/lms/courses/...)
		if (!window.location.pathname.includes('/lms/courses/')) {
			console.log('LMS Feedback Button: Não está em página de curso');
			return;
		}

		// Extrair nome do curso da URL
		const pathParts = window.location.pathname.split('/');
		const courseIndex = pathParts.indexOf('courses');
		if (courseIndex === -1 || !pathParts[courseIndex + 1]) {
			console.log('LMS Feedback Button: Não conseguiu extrair curso da URL');
			return;
		}

		const course_name = pathParts[courseIndex + 1];

		// Se já foi injetado para este curso, não fazer novamente
		if (hasBeenInjected && currentCourse === course_name) {
			return;
		}

		console.log('LMS Feedback Button: Buscando dados para curso:', course_name);

		// Chamar backend para obter dados do botão
		const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';
		fetch('/api/method/lms_course_survey.satisfacao.course_integration.get_course_feedback_button_data', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-Frappe-CSRF-Token': csrfToken
			},
			body: JSON.stringify({ course: course_name })
		})
		.then(response => {
			console.log('LMS Feedback Button: Resposta da API -', response.status);
			return response.json();
		})
		.then(data => {
			console.log('LMS Feedback Button: Dados recebidos -', data);
			if (data.message) {
				injectFeedbackButton(course_name, data.message);
				hasBeenInjected = true;
				currentCourse = course_name;
			}
		})
		.catch(error => {
			console.error('LMS Feedback Button: Erro ao buscar dados -', error);
		});
	}

	// Injetar estilos
	injectStyles();

	// Executar quando DOM está pronto
	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', function() {
			fetchAndInjectButton();
		});
	} else {
		fetchAndInjectButton();
	}

	// Detectar mudanças de página (para SPA) - com debounce para evitar chamadas múltiplas
	let lastPathname = window.location.pathname;
	let debounceTimer = null;

	const checkPageChange = function() {
		if (window.location.pathname !== lastPathname) {
			lastPathname = window.location.pathname;
			hasBeenInjected = false; // Reset para nova página
			currentCourse = null;

			// Debounce para evitar múltiplas chamadas rápidas
			clearTimeout(debounceTimer);
			debounceTimer = setTimeout(() => {
				fetchAndInjectButton();
			}, 500);
		}
	};

	// Usar popstate para detectar mudanças de URL (mais eficiente que MutationObserver)
	window.addEventListener('popstate', checkPageChange);
	window.addEventListener('hashchange', checkPageChange);

	// Listener de pushState (para frameworks SPA)
	const originalPushState = window.history.pushState;
	window.history.pushState = function() {
		originalPushState.apply(this, arguments);
		checkPageChange();
	};

	console.log('LMS Feedback Button: Script carregado e pronto');
})();
