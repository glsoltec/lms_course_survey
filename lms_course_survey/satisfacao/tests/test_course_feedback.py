import frappe
from frappe.tests.utils import FrappeTestCase


class TestCourseFeedback(FrappeTestCase):
	def test_create_course_feedback(self):
		"""Testa criação de feedback"""
		doc = frappe.new_doc("Course Feedback")
		doc.course = "Test Course"
		doc.instructor_rating = "Bom"
		doc.content_rating = "Bom"
		doc.course_rating = "Ótimo"
		doc.overall_rating = "Bom"

		doc.insert()
		self.assertEqual(doc.student, frappe.session.user)

	def test_feedback_submission(self):
		"""Testa submissão de feedback"""
		doc = frappe.new_doc("Course Feedback")
		doc.course = "Test Course"
		doc.instructor_rating = "Regular"
		doc.content_rating = "Bom"
		doc.course_rating = "Bom"
		doc.overall_rating = "Regular"

		doc.insert()
		doc.submit()
		self.assertEqual(doc.docstatus, 1)

	def test_feedback_comments_optional(self):
		"""Testa que comentários são opcionais"""
		doc = frappe.new_doc("Course Feedback")
		doc.course = "Test Course"
		doc.instructor_rating = "Ótimo"
		doc.content_rating = "Ótimo"
		doc.course_rating = "Ótimo"
		doc.overall_rating = "Ótimo"
		# feedback_comments deixado vazio

		doc.insert()
		self.assertEqual(doc.feedback_comments, None or "")

	def test_all_ratings_required(self):
		"""Testa validação quando faltam ratings"""
		doc = frappe.new_doc("Course Feedback")
		doc.course = "Test Course"
		doc.instructor_rating = "Bom"
		# Deixar outros ratings vazios deve falhar na validação

		self.assertRaises(frappe.ValidationError, doc.insert)
