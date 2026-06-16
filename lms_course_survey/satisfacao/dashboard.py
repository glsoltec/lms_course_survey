import frappe
from frappe import _


def get_dashboard_data(data):
	"""
	Dashboard personalizado para Course Feedback DocType
	Mostra gráficos de feedback agregados
	"""
	return {
		"heatmap": False,
		"heatmap_message": _("Resumo de feedback dos cursos."),
		"cards": get_cards(),
		"chart_data": get_chart_data(),
		"non_standard_fieldtypes": {},
	}


def get_cards():
	"""
	Cards com métricas principais de feedback
	"""
	from frappe.utils import getdate
	from frappe.utils import add_days

	# Últimas 30 dias
	start_date = add_days(getdate(), -30)

	total_feedbacks = frappe.db.count(
		"Course Feedback",
		filters={
			"docstatus": 1,
			"submitted_date": [">", start_date],
		},
	)

	# Calcular notas médias
	feedbacks = frappe.get_list(
		"Course Feedback",
		filters={
			"docstatus": 1,
			"submitted_date": [">", start_date],
		},
		fields=["instructor_rating", "content_rating", "course_rating", "overall_rating"],
	)

	ratings_map = {"Péssimo": 1, "Ruim": 2, "Regular": 3, "Bom": 4, "Ótimo": 5}

	if feedbacks:
		overall_ratings = [ratings_map.get(f.get("overall_rating"), 0) for f in feedbacks]
		avg_overall = round(sum(overall_ratings) / len(overall_ratings), 2)
	else:
		avg_overall = 0

	return [
		{
			"label": _("Feedbacks (últimos 30 dias)"),
			"stat": total_feedbacks,
			"indicator": "blue",
			"doctype": "Course Feedback",
		},
		{
			"label": _("Avaliação Geral Média"),
			"stat": f"{avg_overall}/5.0",
			"indicator": get_indicator(avg_overall),
			"doctype": "Course Feedback",
		},
	]


def get_chart_data():
	"""
	Gera dados para gráfico comparativo de feedback
	"""
	from frappe.utils import getdate
	from frappe.utils import add_days

	start_date = add_days(getdate(), -30)

	feedbacks = frappe.get_list(
		"Course Feedback",
		filters={
			"docstatus": 1,
			"submitted_date": [">", start_date],
		},
		fields=["instructor_rating", "content_rating", "course_rating", "overall_rating"],
	)

	ratings_map = {"Péssimo": 1, "Ruim": 2, "Regular": 3, "Bom": 4, "Ótimo": 5}

	# Agrupar ratings por categoria
	ratings_by_category = {
		"Instrutor": [],
		"Conteúdo": [],
		"Curso": [],
		"Geral": [],
	}

	for feedback in feedbacks:
		ratings_by_category["Instrutor"].append(ratings_map.get(feedback.get("instructor_rating"), 0))
		ratings_by_category["Conteúdo"].append(ratings_map.get(feedback.get("content_rating"), 0))
		ratings_by_category["Curso"].append(ratings_map.get(feedback.get("course_rating"), 0))
		ratings_by_category["Geral"].append(ratings_map.get(feedback.get("overall_rating"), 0))

	# Calcular médias
	averages = {}
	for category, ratings in ratings_by_category.items():
		if ratings:
			averages[category] = round(sum(ratings) / len(ratings), 2)
		else:
			averages[category] = 0

	return {
		"data": {
			"labels": [_("Instrutor"), _("Conteúdo"), _("Curso"), _("Geral")],
			"datasets": [
				{
					"name": _("Nota Média"),
					"values": [
						averages.get("Instrutor", 0),
						averages.get("Conteúdo", 0),
						averages.get("Curso", 0),
						averages.get("Geral", 0),
					],
				}
			],
		},
		"type": "bar",
		"height": 300,
	}


def get_indicator(rating):
	"""
	Define cor do indicador (1-5)
	"""
	if rating >= 4:
		return "green"
	elif rating >= 3:
		return "yellow"
	else:
		return "red"
