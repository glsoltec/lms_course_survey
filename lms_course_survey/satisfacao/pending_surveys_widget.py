"""
Widget de Pesquisas Pendentes
Exibe pesquisas que não foram respondidas ainda
"""

import frappe
from frappe import _


@frappe.whitelist()
def get_pending_surveys_data():
	"""
	Retorna dados para widget de pesquisas pendentes
	"""
	student = frappe.session.user

	# Cursos completados
	completed_courses = frappe.get_list(
		"Course Enrollment",
		filters={"student": student, "progress": 100},
		fields=["course", "completion_date"],
	)

	pending = []
	for enrollment in completed_courses:
		course = enrollment["course"]
		completion_date = enrollment["completion_date"]

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
				"completion_date": completion_date,
				"days_since_completion": get_days_since(completion_date),
				"survey_url": f"/app/course-satisfaction-form?course={course}",
			})

	# Ordenar por dias desde conclusão (mais antigos primeiro)
	pending.sort(key=lambda x: x["days_since_completion"], reverse=True)

	return {
		"total": len(pending),
		"surveys": pending[:5],  # Mostrar top 5
	}


def get_days_since(date):
	"""Retorna dias desde uma data"""
	from datetime import datetime
	from frappe.utils import getdate

	if not date:
		return 0

	diff = getdate() - getdate(date)
	return diff.days


def get_pending_surveys_card_html():
	"""
	Retorna HTML do card para dashboard
	"""
	try:
		data = get_pending_surveys_data()
	except:
		return ""

	if not data["surveys"]:
		return ""

	html = """
	<div class="card pending-surveys-card">
		<div class="card-header bg-warning text-dark">
			<h5 class="mb-0">
				📋 Pesquisas Pendentes
				<span class="badge bg-danger float-end">{}</span>
			</h5>
		</div>
		<div class="card-body">
			<p class="text-muted mb-3">
				Você completou cursos mas ainda não respondeu as pesquisas de satisfação.
			</p>
			<ul class="list-unstyled">
	""".format(data["total"])

	for survey in data["surveys"]:
		html += f"""
		<li class="mb-2 pb-2 border-bottom">
			<div class="d-flex justify-content-between align-items-start">
				<div>
					<h6 class="mb-1">{survey['course_name']}</h6>
					<small class="text-muted">
						Concluído há {survey['days_since_completion']} dia(s)
					</small>
				</div>
				<a href="{survey['survey_url']}" class="btn btn-sm btn-primary">
					Responder
				</a>
			</div>
		</li>
		"""

	html += """
			</ul>
			<div class="mt-3">
				<a href="/app/course-satisfaction-list" class="btn btn-outline-secondary btn-sm">
					Ver Todas as Pesquisas
				</a>
			</div>
		</div>
	</div>
	"""

	return html


def get_pending_surveys_report():
	"""
	Relatório para gestores: Quem não respondeu pesquisa
	"""
	# Todos os cursos completados
	completed_enrollments = frappe.get_list(
		"Course Enrollment",
		filters={"progress": 100},
		fields=["student", "course", "completion_date"],
	)

	data = []
	for enrollment in completed_enrollments:
		student = enrollment["student"]
		course = enrollment["course"]
		completion_date = enrollment["completion_date"]

		survey_exists = frappe.db.exists(
			"Course Satisfaction",
			{
				"student": student,
				"course": course,
				"docstatus": 1,
			},
		)

		if not survey_exists:
			user = frappe.get_doc("User", student)
			course_doc = frappe.get_doc("Course", course)

			data.append({
				"student": student,
				"student_name": user.full_name,
				"student_email": user.email,
				"course": course,
				"course_name": course_doc.course_name,
				"completion_date": completion_date,
				"days_pending": get_days_since(completion_date),
				"survey_url": f"/app/course-satisfaction-form?course={course}",
				"status": "⏳ Pendente",
			})

	return data


@frappe.whitelist()
def remind_pending_surveys(survey_course=None):
	"""
	Envia lembrete para pesquisa pendente
	"""
	from lms_course_survey.satisfacao.survey_reminders import send_reminder_email

	student = frappe.session.user

	# Se passou course, apenas esse
	if survey_course:
		courses = [survey_course]
	else:
		# Todos os pendentes
		pending = get_pending_surveys_data()
		courses = [s["course"] for s in pending["surveys"]]

	for course in courses:
		user_doc = frappe.get_doc("User", student)
		course_doc = frappe.get_doc("Course", course)

		send_reminder_email({
			"student": student,
			"student_name": user_doc.full_name,
			"student_email": user_doc.email,
			"course": course,
			"course_name": course_doc.course_name,
		})

	frappe.msgprint(
		_("Lembrete enviado! Verifique seu email."),
		title=_("Sucesso"),
		indicator="green",
	)
