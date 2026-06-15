import frappe
from frappe.tests.utils import FrappeTestCase


class TestCourseSatisfaction(FrappeTestCase):
	def test_create_course_satisfaction(self):
		"""Testa criação de pesquisa de satisfação"""
		doc = frappe.new_doc("Course Satisfaction")
		doc.student = "test_user@example.com"
		doc.course = "Test Course"

		# Adicionar 4 itens padrão
		for i, item_name in enumerate(
			["Treinamento", "Instrutor", "Conteúdo", "Satisfação Geral"]
		):
			doc.append(
				"satisfaction_items",
				{
					"item_name": item_name,
					"item_label": f"Questão {i+1}",
					"rating": "5 - Ótimo",
				},
			)

		doc.insert()
		self.assertEqual(len(doc.satisfaction_items), 4)

	def test_validation_missing_items(self):
		"""Testa validação quando faltam itens"""
		doc = frappe.new_doc("Course Satisfaction")
		doc.student = "test_user@example.com"
		doc.course = "Test Course"

		# Adicionar apenas 2 itens (deve falhar)
		doc.append(
			"satisfaction_items",
			{
				"item_name": "Treinamento",
				"rating": "5 - Ótimo",
			},
		)

		doc.insert()

		# Tentar submeter deve falhar
		self.assertRaises(frappe.ValidationError, doc.submit)

	def test_average_rating(self):
		"""Testa cálculo de média"""
		doc = frappe.new_doc("Course Satisfaction")
		doc.student = "test_user@example.com"
		doc.course = "Test Course"

		for item_name in [
			"Treinamento",
			"Instrutor",
			"Conteúdo",
			"Satisfação Geral",
		]:
			doc.append(
				"satisfaction_items",
				{
					"item_name": item_name,
					"rating": "4 - Bom",
				},
			)

		doc.insert()
		avg = doc.get_average_rating()
		self.assertEqual(avg, 4.0)
