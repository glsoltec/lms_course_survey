frappe.ui.form.on('Course Feedback', {
	onload(frm) {
		// Só permite para usuários logados
		if (frappe.session.user === 'Guest') {
			frappe.msgprint({
				title: 'Acesso Negado',
				message: 'Você deve estar logado para responder o feedback',
				indicator: 'red'
			});
			frappe.call({
				method: 'frappe.auth.api.logout',
				callback: () => window.location.href = '/login'
			});
		}

		// Auto-preenchimento do aluno logado
		frm.set_value('student', frappe.session.user);

		// Se veio de URL com course, preencher
		const urlParams = new URLSearchParams(window.location.search);
		const course = urlParams.get('course');
		if (course) {
			frm.set_value('course', course);
		}
	},

	validate(frm) {
		// Garantir que todas as opções foram selecionadas
		if (!frm.doc.instructor_rating) {
			frappe.throw('Avalie o instrutor');
		}
		if (!frm.doc.content_rating) {
			frappe.throw('Avalie o conteúdo');
		}
		if (!frm.doc.course_rating) {
			frappe.throw('Avalie o curso');
		}
		if (!frm.doc.overall_rating) {
			frappe.throw('Faça uma avaliação geral');
		}
	},

	on_submit(frm) {
		frappe.msgprint({
			title: 'Sucesso!',
			message: 'Seu feedback foi registrado com sucesso. Obrigado por avaliar este curso!',
			indicator: 'green'
		});
	}
});
