"""
Validação de Certificado - Requer feedback do aluno
Bloqueia emissão do certificado até feedback ser respondido
"""

import frappe


def validate_certificate_needs_feedback(doc, method=None):
	"""
	Hook: Bloqueia certificado se aluno não respondeu feedback
	Lançado quando usuário tenta gerar certificado
	"""
	if doc.doctype != "Course Completion Certificate":
		return

	student = doc.student
	course = doc.course

	# Verificar se feedback foi respondido e submetido
	feedback_completed = frappe.db.exists(
		"Course Feedback",
		{
			"student": student,
			"course": course,
			"docstatus": 1,
		},
	)

	if not feedback_completed:
		frappe.throw(
			f"""
			<strong>📋 Feedback Obrigatório</strong><br><br>
			Você deve responder o questionário de satisfação antes de gerar o certificado.<br><br>
			<a href='/app/course-feedback?course={course}' class='btn btn-primary btn-sm'>
			→ Responder Feedback Agora
			</a>
			""",
			title="Feedback Pendente"
		)


def get_feedback_completion_status(course, student=None):
	"""
	Retorna status de conclusão do feedback para um aluno/curso
	Útil para exibir no curso ou no certificado
	"""
	if not student:
		student = frappe.session.user

	feedback = frappe.db.get_value(
		"Course Feedback",
		{
			"student": student,
			"course": course,
			"docstatus": 1,
		},
		["name", "submitted_date"],
	)

	if feedback:
		return {
			"completed": True,
			"feedback_name": feedback[0],
			"feedback_date": feedback[1],
		}
	else:
		return {
			"completed": False,
			"feedback_name": None,
			"feedback_date": None,
		}


@frappe.whitelist()
def get_pending_feedbacks():
	"""
	Retorna lista de cursos com feedback pendente para o usuário logado
	Útil para dashboard pessoal
	"""
	student = frappe.session.user

	# Cursos que aluno completou
	completed_courses = frappe.get_list(
		"Course Enrollment",
		filters={
			"student": student,
			"progress": 100,
		},
		fields=["course"],
	)

	pending = []
	for enrollment in completed_courses:
		course = enrollment["course"]

		# Verificar se respondeu feedback
		feedback_exists = frappe.db.exists(
			"Course Feedback",
			{
				"student": student,
				"course": course,
				"docstatus": 1,
			},
		)

		if not feedback_exists:
			course_doc = frappe.get_doc("Course", course)
			pending.append({
				"course": course,
				"course_name": course_doc.course_name,
				"feedback_url": f"/app/course-feedback?course={course}",
			})

	return pending
