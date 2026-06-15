import frappe
from frappe.model.document import Document


class CourseSatisfaction(Document):
	def before_insert(self):
		# Preencher data/hora automaticamente
		self.survey_date = frappe.utils.now()

	def before_submit(self):
		# Validar se todas as 4 questões foram respondidas
		if len(self.satisfaction_items) != 4:
			frappe.throw(
				frappe._("Pesquisa deve conter exatamente 4 itens de avaliação.")
			)

		# Validar se todas as respostas foram preenchidas
		items_required = {
			"Treinamento",
			"Instrutor",
			"Conteúdo",
			"Satisfação Geral",
		}
		items_respondidos = {item.item_name for item in self.satisfaction_items}

		if items_required != items_respondidos:
			frappe.throw(
				frappe._(
					f"Itens faltando: {items_required - items_respondidos}"
				)
			)

		# Validar se todas as respostas têm rating
		for item in self.satisfaction_items:
			if not item.rating:
				frappe.throw(
					frappe._(
						f"Item '{item.item_name}' não foi avaliado. Por favor, selecione uma nota."
					)
				)

	def on_submit(self):
		# Log de conclusão da pesquisa
		frappe.log_error(
			title="Pesquisa Completada",
			message=f"Aluno: {self.student} | Curso: {self.course} | Rating Médio: {self.get_average_rating()}",
		)

	def get_average_rating(self):
		"""Calcula a média dos ratings"""
		if not self.satisfaction_items:
			return 0
		total = sum(item.rating for item in self.satisfaction_items)
		return round(total / len(self.satisfaction_items), 2)
