import frappe
from frappe import _
from collections import defaultdict


def execute(filters=None):
	"""
	Relatório de Dashboard - Análise de Satisfação por Item
	"""
	if filters is None:
		filters = {}

	columns = get_columns()
	data = get_data(filters)
	chart_data = get_chart_data(filters)

	return columns, data, None, chart_data


def get_columns():
	return [
		{"label": _("Item de Avaliação"), "fieldname": "item_name", "fieldtype": "Data", "width": 200},
		{"label": _("Total Respostas"), "fieldname": "total_count", "fieldtype": "Int", "width": 120},
		{
			"label": _("Nota Média"),
			"fieldname": "average_rating",
			"fieldtype": "Float",
			"width": 120,
		},
		{
			"label": _("Péssimo (1)"),
			"fieldname": "rating_1",
			"fieldtype": "Int",
			"width": 100,
		},
		{
			"label": _("Ruim (2)"),
			"fieldname": "rating_2",
			"fieldtype": "Int",
			"width": 100,
		},
		{
			"label": _("Regular (3)"),
			"fieldname": "rating_3",
			"fieldtype": "Int",
			"width": 100,
		},
		{"label": _("Bom (4)"), "fieldname": "rating_4", "fieldtype": "Int", "width": 100},
		{
			"label": _("Ótimo (5)"),
			"fieldname": "rating_5",
			"fieldtype": "Int",
			"width": 100,
		},
		{
			"label": _("% Satisfeitos (4-5)"),
			"fieldname": "satisfaction_percent",
			"fieldtype": "Percent",
			"width": 130,
		},
	]


def get_data(filters):
	"""
	Extrai dados das pesquisas submetidas
	"""
	query_filters = {"docstatus": 1}

	if filters.get("course"):
		query_filters["course"] = filters["course"]

	if filters.get("from_date"):
		query_filters["survey_date"] = [">", filters["from_date"]]

	if filters.get("to_date"):
		query_filters["survey_date"] = ["<=", filters["to_date"]]

	surveys = frappe.get_list(
		"Course Satisfaction",
		filters=query_filters,
		fields=["name"],
	)

	ratings_by_item = defaultdict(lambda: {"ratings": [], "distribution": {i: 0 for i in range(1, 6)}})

	for survey in surveys:
		doc = frappe.get_doc("Course Satisfaction", survey["name"])
		for item in doc.satisfaction_items:
			rating_value = int(item.rating.split()[0])
			ratings_by_item[item.item_name]["ratings"].append(rating_value)
			ratings_by_item[item.item_name]["distribution"][rating_value] += 1

	data = []
	for item_name in [
		"Treinamento",
		"Instrutor",
		"Conteúdo",
		"Satisfação Geral",
	]:
		if item_name in ratings_by_item:
			info = ratings_by_item[item_name]
			ratings = info["ratings"]
			dist = info["distribution"]
			total = len(ratings)
			avg = round(sum(ratings) / total, 2) if total > 0 else 0
			satisfied = dist[4] + dist[5]
			satisfaction_pct = round((satisfied / total * 100), 1) if total > 0 else 0

			data.append(
				{
					"item_name": item_name,
					"total_count": total,
					"average_rating": avg,
					"rating_1": dist[1],
					"rating_2": dist[2],
					"rating_3": dist[3],
					"rating_4": dist[4],
					"rating_5": dist[5],
					"satisfaction_percent": satisfaction_pct,
				}
			)

	return data


def get_chart_data(filters):
	"""
	Retorna dados para gráficos
	"""
	data = get_data(filters)

	chart = {
		"data": {
			"labels": [d["item_name"] for d in data],
			"datasets": [
				{
					"name": _("Nota Média"),
					"values": [d["average_rating"] for d in data],
					"chartType": "bar",
				}
			],
		},
		"type": "bar",
		"height": 400,
	}

	return chart
