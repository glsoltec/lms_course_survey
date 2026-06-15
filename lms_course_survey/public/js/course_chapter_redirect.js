/**
 * Course Chapter Redirect - Pesquisa de Satisfação
 * Redireciona para pesquisa após o último capítulo ser visualizado
 */

(function() {
	"use strict";

	// Aguardar carregamento da página
	document.addEventListener("DOMContentLoaded", function() {
		// Obter informações de parâmetros da URL ou do contexto
		const urlParams = new URLSearchParams(window.location.search);
		const courseChapter = urlParams.get("chapter") || get_chapter_from_context();
		const course = urlParams.get("course") || get_course_from_context();

		if (!course || !courseChapter) {
			return; // Não é página de capítulo
		}

		// Verificar se é último capítulo e disparar pesquisa
		check_and_trigger_survey(course, courseChapter);

		// Monitorar quando usuário completa leitura do capítulo
		monitor_chapter_completion(course, courseChapter);
	});

	/**
	 * Extrai informações do Course Chapter do contexto Frappe
	 */
	function get_chapter_from_context() {
		if (typeof cur_frm !== "undefined" && cur_frm.doctype === "Course Chapter") {
			return cur_frm.doc.name;
		}
		return null;
	}

	function get_course_from_context() {
		if (typeof cur_frm !== "undefined" && cur_frm.doctype === "Course Chapter") {
			return cur_frm.doc.course;
		}
		return null;
	}

	/**
	 * Verifica se é último capítulo e dispara survey
	 */
	function check_and_trigger_survey(course, courseChapter) {
		frappe.call({
			method: "lms_course_survey.satisfacao.course_chapter_integration.after_chapter_completion",
			args: {
				course: course,
				course_chapter: courseChapter,
			},
			callback: function(r) {
				if (r.message && r.message.status === "redirect_survey") {
					show_survey_prompt(r.message);
				}
			},
		});
	}

	/**
	 * Exibe modal/prompt pedindo para responder pesquisa
	 */
	function show_survey_prompt(data) {
		const message = data.message;

		// Criar modal
		const modalHtml = `
      <div class="modal fade" id="survey-modal" tabindex="-1" role="dialog" aria-labelledby="surveyModalLabel">
        <div class="modal-dialog modal-lg" role="document">
          <div class="modal-content">
            <div class="modal-header bg-primary text-white">
              <h5 class="modal-title" id="surveyModalLabel">
                <i class="fas fa-star"></i> ${message.title}
              </h5>
              <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <p>${message.description}</p>
              <div class="alert alert-info">
                <i class="fas fa-info-circle"></i>
                <strong>Dica:</strong> Sua opinião nos ajuda a melhorar continuamente!
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                <i class="fas fa-times"></i> Responder Depois
              </button>
              <button type="button" class="btn btn-primary" id="go-survey-btn">
                <i class="fas fa-arrow-right"></i> Ir para Pesquisa
              </button>
            </div>
          </div>
        </div>
      </div>
    `;

		// Adicionar ao DOM
		document.body.insertAdjacentHTML("beforeend", modalHtml);

		// Mostrar modal
		const modal = new bootstrap.Modal(document.getElementById("survey-modal"), {
			backdrop: "static", // Não permite fechar clicando fora
			keyboard: false, // Desabilita ESC
		});

		modal.show();

		// Listener do botão
		document.getElementById("go-survey-btn").addEventListener("click", function() {
			modal.hide();
			// Redirecionar para formulário
			window.location.href = data.survey_url;
		});
	}

	/**
	 * Monitora quando usuário completa leitura do capítulo
	 * Dispara pesquisa após tempo mínimo de leitura
	 */
	function monitor_chapter_completion(course, courseChapter) {
		const MIN_READ_TIME = 60000; // 1 minuto
		let startTime = Date.now();

		// Quando usuário quer ir para próximo capítulo
		const nextChapterBtn = document.querySelector(
			'a[data-action="next-chapter"], button.btn-next-chapter'
		);

		if (nextChapterBtn) {
			nextChapterBtn.addEventListener("click", function(e) {
				const readTime = Date.now() - startTime;

				// Se leu pouco tempo, mostrar aviso
				if (readTime < MIN_READ_TIME) {
					e.preventDefault();
					frappe.msgprint({
						title: "Leitura Recomendada",
						indicator: "orange",
						message: "Por favor, dedique pelo menos 1 minuto para ler o capítulo.",
					});
				}
			});
		}
	}

	/**
	 * Função utilitária: Redirecionar para pesquisa
	 * Pode ser chamada manualmente
	 */
	window.redirect_to_satisfaction_survey = function(course, courseChapter) {
		const url = `/app/course-satisfaction-form?course=${course}&course_chapter=${courseChapter}`;
		window.location.href = url;
	};

	/**
	 * Função utilitária: Verificar status da pesquisa
	 */
	window.check_satisfaction_status = function(course, callback) {
		frappe.call({
			method: "lms_course_survey.satisfacao.course_chapter_integration.get_course_satisfaction_status",
			args: {
				course: course,
			},
			callback: callback,
		});
	};
})();
