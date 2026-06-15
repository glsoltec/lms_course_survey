"""
Validação de Certificado - Requer pesquisa de satisfação
Bloqueia emissão do certificado até pesquisa ser respondida
"""

import frappe
from frappe import _


def validate_survey_before_certificate(doc, method=None):
	"""
	Hook: Valida pesquisa antes de emitir certificado
	Lançado quando usuário tenta gerar certificado
	"""
	if doc.doctype != "Course Completion Certificate":
		return

	student = doc.student
	course = doc.course

	# Verificar se pesquisa foi respondida
	survey_completed = frappe.db.exists(
		"Course Satisfaction",
		{
			"student": student,
			"course": course,
			"docstatus": 1,
		},
	)

	if not survey_completed:
		frappe.throw(
			_(
				f"<h4>⚠️ Pesquisa de Satisfação Obrigatória</h4>"
				f"<p>Você deve responder a pesquisa de satisfação antes de gerar o certificado.</p>"
				f"<p><a href='/app/course-satisfaction-form?course={course}' target='_blank' class='btn btn-primary'>"
				f"👉 Clique aqui para responder a pesquisa</a></p>"
			)
		)


def block_course_completion_without_survey(doc, method=None):
	"""
	Hook alternativo: Bloqueia marcação de curso como completo
	"""
	if doc.doctype != "Course Enrollment":
		return

	# Se tentando marcar como completo
	if doc.progress == 100 and doc.docstatus == 0:
		student = doc.student
		course = doc.course

		survey_completed = frappe.db.exists(
			"Course Satisfaction",
			{
				"student": student,
				"course": course,
				"docstatus": 1,
			},
		)

		if not survey_completed:
			frappe.throw(
				_(
					"Complete a pesquisa de satisfação para finalizar o curso. "
					f"<a href='/app/course-satisfaction-form?course={course}'>Responder agora</a>"
				)
			)


def get_survey_completion_status(course, student=None):
	"""
	Retorna status de conclusão para um aluno/curso
	Útil para exibir no curso ou no certificado
	"""
	if not student:
		student = frappe.session.user

	survey = frappe.db.get_value(
		"Course Satisfaction",
		{
			"student": student,
			"course": course,
			"docstatus": 1,
		},
		["name", "survey_date"],
	)

	if survey:
		return {
			"completed": True,
			"survey_name": survey[0],
			"survey_date": survey[1],
		}
	else:
		return {
			"completed": False,
			"survey_name": None,
			"survey_date": None,
		}


@frappe.whitelist()
def get_pending_surveys():
	"""
	Retorna lista de pesquisas pendentes para o usuário logado
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

		# Verificar se respondeu pesquisa
		survey_exists = frappe.db.exists(
			"Course Satisfaction",
			{
				"student": student,
				"course": course,
				"docstatus": 1,
			},
		)

		if not survey_exists:
			course_doc = frappe.get_doc("Course", course)
			pending.append({
				"course": course,
				"course_name": course_doc.course_name,
				"survey_url": f"/app/course-satisfaction-form?course={course}",
			})

	return pending
