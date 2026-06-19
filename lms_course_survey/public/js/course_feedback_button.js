/**
 * Adiciona botão de Feedback no painel do Course
 * Aparece apenas se curso completado (progress = 100%)
 */

frappe.ui.form.on('Course', {
	refresh: function(frm) {
		// Apenas para visualizar (não novo documento)
		if (frm.doc.name && !frm.is_new()) {
			add_feedback_button(frm);
		}
	}
});

function add_feedback_button(frm) {
	// Só para usuarios logados
	if (frappe.session.user === 'Guest') {
		return;
	}

	const course_name = frm.doc.name;

	// Chamar backend para verificar se pode responder
	frappe.call({
		method: 'lms_course_survey.satisfacao.course_integration.get_course_feedback_button_data',
		args: {
			course: course_name
		},
		callback: function(r) {
			if (r.message) {
				const data = r.message;

				// Se não deve mostrar, sair
				if (!data.show_button) {
					// Mostrar mensagem informativa em cinza
					show_feedback_info_message(frm, data.message, data.reason);
					return;
				}

				// Determinar cor e ícone do botão
				const is_completed = data.status === 'completed';
				const button_class = data.button_class || 'btn-primary';
				const icon = data.icon || 'message-square';

				// Adicionar botão ao formulário
				frm.add_custom_button(
					'<i class="' + get_icon_class(icon) + '"></i> ' + data.button_text,
					function() {
						// Abrir feedback em nova aba
						window.open(data.feedback_url, '_blank');
					}
				).addClass(button_class);

				// Mostrar mensagem de status abaixo do botão
				show_feedback_status_message(frm, data.message, is_completed);
			}
		}
	});
}

function get_icon_class(icon) {
	// Mapear nomes de ícones para classes Bootstrap
	const icons = {
		'message-square': 'fa fa-comment-o',
		'check-circle': 'fa fa-check-circle',
		'clock': 'fa fa-clock-o',
		'alert': 'fa fa-exclamation-circle'
	};
	return icons[icon] || 'fa fa-comment-o';
}

function show_feedback_info_message(frm, message, reason) {
	// Mostrar mensagem cinza quando curso não completado
	const message_types = {
		'not_logged_in': {
			indicator: 'red',
			icon: 'fa-lock'
		},
		'not_enrolled': {
			indicator: 'orange',
			icon: 'fa-question-circle'
		},
		'not_completed': {
			indicator: 'yellow',
			icon: 'fa-clock-o'
		}
	};

	const msg_type = message_types[reason] || { indicator: 'grey', icon: 'fa-info-circle' };

	frm.dashboard.clear_comment();
	frm.dashboard.add_comment(
		'<i class="fa ' + msg_type.icon + '"></i> ' + message,
		'blue'
	);
}

function show_feedback_status_message(frm, message, is_completed) {
	// Mostrar mensagem de status
	const indicator = is_completed ? 'green' : 'blue';
	const icon = is_completed ? 'fa-check-circle' : 'fa-comment-o';

	frm.dashboard.clear_comment();
	frm.dashboard.add_comment(
		'<i class="fa ' + icon + '"></i> ' + message,
		indicator
	);
}

// Também adicionar no view de Course quando não é formulário
frappe.listview_settings['Course'] = {
	add_fields: ['progress'],
	get_indicator: function(doc) {
		// Mostrar indicador visual se feedback pendente (opcional)
		return;
	}
};
