import frappe
from frappe import _
from frappe.utils import getdate
from collections import defaultdict


@frappe.whitelist()
def get_satisfaction_stats(course=None, start_date=None, end_date=None):
	"""
	Retorna estatísticas agregadas de satisfação por curso/período
	"""
	filters = {"docstatus": 1}

	if course:
		filters["course"] = course
	if start_date:
		filters["survey_date"] = [">", getdate(start_date)]
	if end_date:
		filters["survey_date"] = ["<=", getdate(end_date)]

	surveys = frappe.get_list(
		"Course Satisfaction",
		filters=filters,
		fields=[
			"name",
			"course",
			"student",
			"survey_date",
		],
	)

	if not surveys:
		return {
			"total_surveys": 0,
			"average_rating": 0,
			"by_item": {},
		}

	ratings_by_item = defaultdict(list)

	for survey_name in [s["name"] for s in surveys]:
		doc = frappe.get_doc("Course Satisfaction", survey_name)
		for item in doc.satisfaction_items:
			rating_value = int(item.rating.split()[0])
			ratings_by_item[item.item_name].append(rating_value)

	# Calcular médias
	stats = {
		"total_surveys": len(surveys),
		"average_rating": 0,
		"by_item": {},
	}

	all_ratings = []
	for item_name, ratings in ratings_by_item.items():
		avg = round(sum(ratings) / len(ratings), 2)
		stats["by_item"][item_name] = {
			"average": avg,
			"count": len(ratings),
			"distribution": get_rating_distribution(ratings),
		}
		all_ratings.extend(ratings)

	if all_ratings:
		stats["average_rating"] = round(
			sum(all_ratings) / len(all_ratings), 2
		)

	return stats


def get_rating_distribution(ratings):
	"""Retorna distribuição de ratings (1-5)"""
	distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
	for rating in ratings:
		distribution[rating] += 1
	return distribution


@frappe.whitelist()
def create_default_satisfaction_items(satisfaction_doc):
	"""
	Cria automaticamente os 4 itens padrão de avaliação
	"""
	doc = frappe.get_doc("Course Satisfaction", satisfaction_doc)

	default_items = [
		("Treinamento", "Qual o nível de satisfação com o treinamento?"),
		("Instrutor", "Qual o nível de satisfação com o instrutor?"),
		("Conteúdo", "Qual o nível de satisfação com o conteúdo?"),
		(
			"Satisfação Geral",
			"Qual o nível de satisfação geral?",
		),
	]

	doc.satisfaction_items = []
	for item_name, item_label in default_items:
		doc.append(
			"satisfaction_items",
			{
				"item_name": item_name,
				"item_label": item_label,
			},
		)

	doc.save()
	frappe.msgprint(_("Itens de satisfação criados com sucesso."))


@frappe.whitelist()
def get_course_satisfaction_summary(course):
	"""
	Retorna resumo de satisfação para um curso específico
	"""
	surveys = frappe.get_list(
		"Course Satisfaction",
		filters={"course": course, "docstatus": 1},
		fields=["name"],
	)

	if not surveys:
		return None

	rating_totals = {"Treinamento": [], "Instrutor": [], "Conteúdo": [], "Satisfação Geral": []}

	for survey in surveys:
		doc = frappe.get_doc("Course Satisfaction", survey["name"])
		for item in doc.satisfaction_items:
			rating_value = int(item.rating.split()[0])
			rating_totals[item.item_name].append(rating_value)

	summary = {}
	for item, ratings in rating_totals.items():
		if ratings:
			summary[item] = {
				"average": round(sum(ratings) / len(ratings), 2),
				"count": len(ratings),
			}

	return summary
