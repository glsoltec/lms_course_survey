"""
Integração com Course Chapter (ERPNext LMS)
Redireciona para pesquisa após o último capítulo
"""

import frappe
from frappe import _
from frappe.utils import get_url


def get_course_chapters(course):
	"""
	Retorna lista de capítulos do curso em ordem
	"""
	chapters = frappe.get_list(
		"Course Chapter",
		filters={"course": course},
		fields=["name", "chapter_number", "title"],
		order_by="chapter_number asc",
	)
	return chapters


def get_last_chapter(course):
	"""
	Retorna o último capítulo do curso
	"""
	chapters = get_course_chapters(course)
	return chapters[-1] if chapters else None


def is_last_chapter(course, chapter):
	"""
	Verifica se é o último capítulo do curso
	"""
	last = get_last_chapter(course)
	return last and last.get("name") == chapter


def get_satisfaction_survey_url(course, course_chapter=None):
	"""
	Gera URL para formulário de satisfação
	"""
	base_url = "/app/course-satisfaction-form?"
	url = f"{base_url}course={course}"

	if course_chapter:
		url += f"&course_chapter={course_chapter}"

	return get_url(url)


def check_survey_completed(student, course):
	"""
	Verifica se aluno já completou pesquisa para este curso
	"""
	existing = frappe.get_list(
		"Course Satisfaction",
		filters={
			"student": student,
			"course": course,
			"docstatus": 1,
		},
		fields=["name"],
	)
	return len(existing) > 0


def get_redirect_message(course, chapter):
	"""
	Mensagem para redirecionar após capítulo
	"""
	return {
		"indicator": "green",
		"title": _("Parabéns! 🎉"),
		"description": _(
			"Você completou o último capítulo do curso. "
			"Por favor, responda a pesquisa de satisfação para nos ajudar a melhorar."
		),
		"action": {
			"label": _("Responder Pesquisa"),
			"url": get_satisfaction_survey_url(course, chapter),
		},
	}


@frappe.whitelist()
def after_chapter_completion(course, course_chapter):
	"""
	Chamada via hook após capítulo ser marcado como completo
	"""
	student = frappe.session.user

	# Verificar se é último capítulo
	if not is_last_chapter(course, course_chapter):
		return {"status": "ok", "action": None}

	# Verificar se já respondeu pesquisa
	if check_survey_completed(student, course):
		return {
			"status": "ok",
			"action": None,
			"message": _("Pesquisa já respondida. Obrigado!"),
		}

	# Gerar URL de redirecionamento
	message = get_redirect_message(course, course_chapter)

	return {
		"status": "redirect_survey",
		"message": message,
		"survey_url": get_satisfaction_survey_url(course, course_chapter),
	}


@frappe.whitelist()
def get_course_satisfaction_status(course):
	"""
	Retorna status de satisfação do aluno para um curso
	"""
	student = frappe.session.user

	completed = check_survey_completed(student, course)

	if completed:
		survey = frappe.get_list(
			"Course Satisfaction",
			filters={
				"student": student,
				"course": course,
				"docstatus": 1,
			},
			fields=["name", "survey_date"],
		)[0]

		return {
			"status": "completed",
			"message": _("Pesquisa respondida"),
			"survey_name": survey.get("name"),
			"survey_date": survey.get("survey_date"),
		}
	else:
		return {
			"status": "pending",
			"message": _("Pesquisa não respondida"),
		}


def on_course_chapter_view(doc, method=None):
	"""
	Hook: Quando usuário visualiza um capítulo do curso
	Verifica se é último e dispara redirecionamento
	"""
	# Este hook seria acionado por uma página/view customizada
	pass


def get_course_dashboard_data(data):
	"""
	Customizar dashboard do Course para mostrar status de satisfação
	"""
	return data
