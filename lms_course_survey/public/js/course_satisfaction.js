// Course Satisfaction - Client Script
// Comportamentos interativos no formulário

frappe.ui.form.on('Course Satisfaction', {
	// Quando o formulário é carregado
	onload(frm) {
		if (frm.doc.docstatus === 0) {
			// Formulário novo - preencher data atual
			frm.set_value('survey_date', frappe.datetime.now_datetime());

			// Se não tem itens, adicionar os 4 padrão
			if (frm.doc.satisfaction_items.length === 0) {
				add_default_items(frm);
			}
		}

		// Mostrar nota média em tempo real
		update_average_display(frm);
	},

	// Quando field "student" muda
	student(frm) {
		frm.refresh_field('student_name');
	},

	// Quando field "course" muda
	course(frm) {
		frm.refresh_field('course_name');

		// Tentar buscar instrutor do curso
		if (frm.doc.course) {
			frappe.call({
				method: 'frappe.client.get',
				args: {
					doctype: 'Course',
					name: frm.doc.course,
				},
				callback: function(r) {
					if (r.message && r.message.instructor) {
						frm.set_value('instructor', r.message.instructor);
					}
				},
			});
		}
	},

	// Quando a table "satisfaction_items" muda
	satisfaction_items_add(frm, cdt, cdn) {
		// Resetar foco para rating field
		frappe.ui.form.open_grid_form(frm, cdt, cdn);
	},
});

// Quando algum item é editado
frappe.ui.form.on('Satisfaction Item', {
	rating(frm, cdt, cdn) {
		// Atualizar média quando rating muda
		update_average_display(frm);
	},
});

// Funções auxiliares

function add_default_items(frm) {
	const items = [
		{
			item_name: 'Treinamento',
			item_label: 'Qual o nível de satisfação com o treinamento?',
		},
		{
			item_name: 'Instrutor',
			item_label: 'Qual o nível de satisfação com o instrutor?',
		},
		{
			item_name: 'Conteúdo',
			item_label: 'Qual o nível de satisfação com o conteúdo?',
		},
		{
			item_name: 'Satisfação Geral',
			item_label: 'Qual o nível de satisfação geral?',
		},
	];

	items.forEach(item => {
		frm.add_child('satisfaction_items', {
			item_name: item.item_name,
			item_label: item.item_label,
		});
	});

	frm.refresh_field('satisfaction_items');
}

function update_average_display(frm) {
	// Calcular e exibir média de satisfação
	let total = 0;
	let count = 0;

	frm.doc.satisfaction_items.forEach(item => {
		if (item.rating) {
			const rating_value = parseInt(item.rating.split(' ')[0]);
			total += rating_value;
			count++;
		}
	});

	const average = count > 0 ? (total / count).toFixed(2) : 0;

	// Mostrar em alert ou custom field (se adicionado)
	const message = `Satisfação Média: ${average}/5.0`;

	// Opcional: adicionar campo read-only "average_rating" para exibir
	if (frm.fields_dict.average_rating) {
		frm.set_value('average_rating', average);
	}
}

// Dashboard de Satisfação
frappe.pages['satisfaction-dashboard'] = frappe.views.ListView.extend({
	init: function(wrapper, route_name) {
		this.page_title = 'Dashboard de Satisfação';
		this.page_route = 'satisfacao';
		super.init(wrapper);
	},

	filters: [
		['Course Satisfaction', 'docstatus', '=', 1],
	],

	get_checked_items: function() {
		return this.page.datatable
			.getCheckedRows()
			.map(row => this.page.datatable.rowmanager.rows[row.idx].doc.name);
	},
});
