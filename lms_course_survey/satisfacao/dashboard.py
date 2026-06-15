import frappe
from frappe import _


def get_dashboard_data(data):
	"""
	Gera dashboard personalizado para Course Satisfaction DocType
	Mostra gráficos de satisfação agregados
	"""

	return {
		"heatmap": False,
		"heatmap_message": _("Este é um resumo de satisfação dos cursos."),
		"cards": get_cards(),
		"chart_data": get_chart_data(),
		"non_standard_fieldtypes": {},
	}


def get_cards():
	"""
	Cards mostrando métricas principais
	"""
	from frappe.utils import getdate
	from datetime import timedelta

	# Últimas 30 dias
	start_date = frappe.utils.add_days(getdate(), -30)

	total_surveys = frappe.db.count(
		"Course Satisfaction",
		filters={
			"docstatus": 1,
			"survey_date": [">", start_date],
		},
	)

	# Média geral dos últimos 30 dias
	surveys = frappe.get_list(
		"Course Satisfaction",
		filters={
			"docstatus": 1,
			"survey_date": [">", start_date],
		},
		fields=["name"],
	)

	all_ratings = []
	for survey in surveys:
		doc = frappe.get_doc("Course Satisfaction", survey["name"])
		for item in doc.satisfaction_items:
			rating = int(item.rating.split()[0])
			all_ratings.append(rating)

	avg_rating = (
		round(sum(all_ratings) / len(all_ratings), 2)
		if all_ratings
		else 0
	)

	return [
		{
			"label": _("Pesquisas (últimos 30 dias)"),
			"stat": total_surveys,
			"indicator": "green",
			"doctype": "Course Satisfaction",
		},
		{
			"label": _("Nota Média Geral"),
			"stat": f"{avg_rating}/5.0",
			"indicator": get_indicator(avg_rating),
			"doctype": "Course Satisfaction",
		},
	]


def get_chart_data():
	"""
	Gera dados para gráfico de satisfação por item
	"""
	from frappe.utils import getdate
	from datetime import timedelta

	start_date = frappe.utils.add_days(getdate(), -30)

	surveys = frappe.get_list(
		"Course Satisfaction",
		filters={
			"docstatus": 1,
			"survey_date": [">", start_date],
		},
		fields=["name"],
	)

	ratings_by_item = {
		"Treinamento": [],
		"Instrutor": [],
		"Conteúdo": [],
		"Satisfação Geral": [],
	}

	for survey in surveys:
		doc = frappe.get_doc("Course Satisfaction", survey["name"])
		for item in doc.satisfaction_items:
			rating = int(item.rating.split()[0])
			if item.item_name in ratings_by_item:
				ratings_by_item[item.item_name].append(rating)

	# Calcular médias
	averages = {}
	for item, ratings in ratings_by_item.items():
		if ratings:
			averages[item] = round(sum(ratings) / len(ratings), 2)
		else:
			averages[item] = 0

	return {
		"data": {
			"labels": [
				_("Treinamento"),
				_("Instrutor"),
				_("Conteúdo"),
				_("Satisfação Geral"),
			],
			"datasets": [
				{
					"name": _("Nota Média"),
					"values": [
						averages.get("Treinamento", 0),
						averages.get("Instrutor", 0),
						averages.get("Conteúdo", 0),
						averages.get("Satisfação Geral", 0),
					],
				}
			],
		},
		"type": "bar",
		"height": 300,
	}


def get_indicator(rating):
	"""
	Define cor do indicador baseado na nota
	"""
	if rating >= 4:
		return "green"
	elif rating >= 3:
		return "yellow"
	else:
		return "red"
