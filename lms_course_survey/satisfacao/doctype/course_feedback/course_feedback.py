import frappe
from frappe.model.document import Document
from frappe.utils import now


class CourseFeedback(Document):
	def before_insert(self):
		# Auto-preenchimento de auditoria
		self.student = frappe.session.user
		self.submitted_date = now()

	def before_submit(self):
		# Validar que aluno está logado (não anônimo)
		if frappe.session.user == "Guest":
			frappe.throw("Você deve estar logado para responder o feedback")

		# Validar que course existe e está ativo
		if not frappe.db.exists("LMS Course", self.course):
			frappe.throw(f"Curso '{self.course}' não foi encontrado")

		course = frappe.get_doc("LMS Course", self.course)
		if hasattr(course, 'is_published') and course.is_published != 1:
			frappe.throw(f"Curso '{self.course}' não está ativo")

	def on_submit(self):
		frappe.db.commit()

	@staticmethod
	def get_feedback_stats(course=None):
		"""Retorna estatísticas para dashboard"""
		filters = {"docstatus": 1}
		if course:
			filters["course"] = course

		feedbacks = frappe.get_list(
			"Course Feedback",
			filters=filters,
			fields=["instructor_rating", "content_rating", "course_rating", "overall_rating"]
		)

		if not feedbacks:
			return {}

		ratings_map = {"Péssimo": 1, "Ruim": 2, "Regular": 3, "Bom": 4, "Ótimo": 5}

		total = len(feedbacks)
		instructor_sum = sum(ratings_map.get(f.get("instructor_rating"), 0) for f in feedbacks)
		content_sum = sum(ratings_map.get(f.get("content_rating"), 0) for f in feedbacks)
		course_sum = sum(ratings_map.get(f.get("course_rating"), 0) for f in feedbacks)
		overall_sum = sum(ratings_map.get(f.get("overall_rating"), 0) for f in feedbacks)

		stats = {
			"total_feedbacks": total,
			"instructor_avg": round(instructor_sum / total, 2) if total > 0 else 0,
			"content_avg": round(content_sum / total, 2) if total > 0 else 0,
			"course_avg": round(course_sum / total, 2) if total > 0 else 0,
			"overall_avg": round(overall_sum / total, 2) if total > 0 else 0,
		}

		return stats

	@staticmethod
	def check_feedback_submitted(student, course):
		"""Verifica se aluno já respondeu feedback para um curso"""
		return frappe.db.exists(
			"Course Feedback",
			{
				"student": student,
				"course": course,
				"docstatus": 1
			}
		)
