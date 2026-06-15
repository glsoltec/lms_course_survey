"""
Lembretes Automáticos - Notifica alunos com pesquisa pendente
Scheduler job que roda diariamente/semanalmente
"""

import frappe
from frappe import _
from frappe.utils import get_url, add_days, getdate


def send_survey_reminders():
	"""
	Envia lembretes via email para alunos com pesquisa pendente
	Deve ser executado via Scheduler (diário ou semanal)
	"""
	# Encontrar pesquisas pendentes
	pending_surveys = get_all_pending_surveys()

	email_sent = 0
	for survey in pending_surveys:
		try:
			send_reminder_email(survey)
			email_sent += 1
		except Exception as e:
			frappe.log_error(f"Erro ao enviar email para {survey['student']}: {str(e)}")

	frappe.logger().info(
		f"[Pesquisa de Satisfação] {email_sent} lembretes enviados"
	)


def get_all_pending_surveys():
	"""
	Retorna lista de todos os cursos completos mas sem pesquisa respondida
	"""
	# Cursos completados
	completed_enrollments = frappe.get_list(
		"Course Enrollment",
		filters={"progress": 100},
		fields=["student", "course", "completion_date"],
	)

	pending = []
	for enrollment in completed_enrollments:
		student = enrollment["student"]
		course = enrollment["course"]
		completion_date = enrollment["completion_date"]

		# Verificar se já respondeu pesquisa
		survey_exists = frappe.db.exists(
			"Course Satisfaction",
			{
				"student": student,
				"course": course,
				"docstatus": 1,
			},
		)

		if not survey_exists:
			# Verificar se já enviou lembrete recentemente
			recent_notification = frappe.db.exists(
				"Communication",
				{
					"reference_doctype": "Course Satisfaction",
					"recipients": student,
					"creation": [">", add_days(getdate(), -3)],  # Últimos 3 dias
				},
			)

			if not recent_notification:
				course_doc = frappe.get_doc("Course", course)
				user_doc = frappe.get_doc("User", student)

				pending.append({
					"student": student,
					"student_name": user_doc.full_name,
					"student_email": user_doc.email,
					"course": course,
					"course_name": course_doc.course_name,
					"completion_date": completion_date,
				})

	return pending


def send_reminder_email(survey_data):
	"""
	Envia email personalizado lembrando sobre pesquisa pendente
	"""
	survey_url = get_url(f"/app/course-satisfaction-form?course={survey_data['course']}")

	subject = f"📋 Lembrete: Pesquisa de Satisfação - {survey_data['course_name']}"

	message = f"""
	<h3>Olá {survey_data['student_name']}! 👋</h3>

	<p>Notamos que você completou o curso <strong>{survey_data['course_name']}</strong>,
	mas ainda não respondeu a pesquisa de satisfação.</p>

	<p>Sua opinião é muito importante para nós! Dedique apenas 3-5 minutos para responder
	4 perguntas simples que nos ajudarão a melhorar continuamente.</p>

	<p style="margin: 30px 0; text-align: center;">
	<a href="{survey_url}"
	   style="display: inline-block;
	           padding: 12px 30px;
	           background-color: #0d6efd;
	           color: white;
	           text-decoration: none;
	           border-radius: 5px;
	           font-weight: bold;">
	👉 Responder Pesquisa Agora
	</a>
	</p>

	<hr style="margin: 20px 0; border: none; border-top: 1px solid #ddd;">

	<p><strong>Por que sua opinião importa?</strong></p>
	<ul>
	<li>Ajuda a melhorar a qualidade do conteúdo</li>
	<li>Permite avaliar efetividade do treinamento</li>
	<li>Contribui para desenvolvimento dos instrutores</li>
	<li>Garante que mantemos os melhores padrões</li>
	</ul>

	<p style="color: #666; font-size: 0.9em; margin-top: 30px;">
	Se preferir responder depois,
	<a href="{survey_url}">clique aqui para acessar a pesquisa</a>.
	</p>

	<p style="color: #999; font-size: 0.8em;">
	Este é um lembrete automático. Você receberá no máximo um lembrete a cada 3 dias.
	</p>
	"""

	frappe.sendmail(
		recipients=[survey_data["student_email"]],
		subject=subject,
		message=message,
		expose_recipients=False,
	)

	# Log da notificação enviada
	frappe.get_doc({
		"doctype": "Communication",
		"communication_type": "Email",
		"communication_medium": "Email",
		"subject": subject,
		"content": message,
		"reference_doctype": "Course Satisfaction",
		"recipients": survey_data["student"],
	}).insert(ignore_permissions=True)


def create_pending_survey_tasks():
	"""
	Cria TO-DO items para gestores sobre pesquisas pendentes
	Útil para acompanhamento administrativo
	"""
	pending = get_all_pending_surveys()

	if not pending:
		return

	# Agrupar por curso
	by_course = {}
	for survey in pending:
		course = survey["course"]
		if course not in by_course:
			by_course[course] = []
		by_course[course].append(survey["student_name"])

	# Criar TODOs para coordenadores
	coordinators = frappe.db.get_list(
		"User",
		filters={"user_type": "System User"},
		fields=["name"],
		limit_page_length=100,
	)

	for coordinator in coordinators:
		for course, students in by_course.items():
			student_list = "<br>".join(students)

			frappe.get_doc({
				"doctype": "ToDo",
				"owner": coordinator["name"],
				"assigned_by": "Administrator",
				"title": f"📋 Pesquisa Pendente - {course}",
				"description": f"""
				<h5>Alunos com pesquisa de satisfação pendente:</h5>
				{student_list}
				<br><br>
				<a href="/app/course-satisfaction?course={course}">
				Ver todas as respostas do curso
				</a>
				""",
				"status": "Open",
			}).insert(ignore_permissions=True)


@frappe.whitelist()
def get_my_pending_surveys():
	"""
	Retorna pesquisas pendentes para o aluno logado
	Útil para exibir na dashboard pessoal
	"""
	student = frappe.session.user

	pending = []
	completed_courses = frappe.get_list(
		"Course Enrollment",
		filters={"student": student, "progress": 100},
		fields=["course"],
	)

	for enrollment in completed_courses:
		course = enrollment["course"]

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
