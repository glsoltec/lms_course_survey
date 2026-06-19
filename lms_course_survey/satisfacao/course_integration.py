"""
Integração com Course - Adiciona botão de Feedback no painel do curso
"""

import frappe


@frappe.whitelist()
def get_course_feedback_button_data(course):
	"""
	Retorna dados para o botão de feedback no painel do curso
	Verifica se aluno completou e se respondeu feedback
	"""
	student = frappe.session.user

	if student == "Guest":
		return {
			"show_button": False,
			"reason": "not_logged_in",
			"message": "Você precisa estar logado"
		}

	# Verificar se aluno completou o curso
	enrollment = frappe.db.get_value(
		"Course Enrollment",
		{
			"student": student,
			"course": course,
		},
		["progress", "name"]
	)

	if not enrollment:
		return {
			"show_button": False,
			"reason": "not_enrolled",
			"message": "Você não está inscrito neste curso"
		}

	progress = enrollment[0]

	# Se não completou (progress < 100), não mostra botão
	if progress < 100:
		return {
			"show_button": False,
			"reason": "not_completed",
			"message": f"Complete o curso para responder feedback (Progress: {progress}%)",
			"progress": progress
		}

	# Verificar se já respondeu feedback
	feedback_exists = frappe.db.exists(
		"Course Feedback",
		{
			"student": student,
			"course": course,
			"docstatus": 1,
		}
	)

	if feedback_exists:
		return {
			"show_button": True,
			"status": "completed",
			"message": "✅ Você já respondeu o feedback deste curso",
			"button_text": "Ver seu Feedback",
			"button_class": "btn-success",
			"feedback_url": f"/app/course-feedback?course={course}&student={student}",
			"icon": "check-circle"
		}
	else:
		return {
			"show_button": True,
			"status": "pending",
			"message": "📋 Sua opinião é importante! Responda o formulário de feedback",
			"button_text": "Responder Feedback Agora",
			"button_class": "btn-primary",
			"feedback_url": f"/app/course-feedback?course={course}",
			"icon": "message-square"
		}


@frappe.whitelist()
def get_student_course_feedback(course):
	"""
	Retorna o feedback respondido pelo aluno para um curso
	"""
	student = frappe.session.user

	feedback = frappe.db.get_value(
		"Course Feedback",
		{
			"student": student,
			"course": course,
			"docstatus": 1,
		},
		[
			"name",
			"instructor_rating",
			"content_rating",
			"course_rating",
			"overall_rating",
			"submitted_date"
		]
	)

	if feedback:
		return {
			"exists": True,
			"feedback_id": feedback[0],
			"instructor_rating": feedback[1],
			"content_rating": feedback[2],
			"course_rating": feedback[3],
			"overall_rating": feedback[4],
			"submitted_date": feedback[5],
		}
	else:
		return {
			"exists": False,
		}
