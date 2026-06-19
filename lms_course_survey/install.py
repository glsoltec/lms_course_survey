import frappe
from frappe.utils import update_progress_bar


def before_install():
	"""Executado antes da instalação"""
	pass


def after_install():
	"""Executado após a instalação - cria DocType Course Feedback"""
	frappe.db.commit()

	# Criar DocType Course Feedback
	create_course_feedback_doctype()

	frappe.db.commit()


def create_course_feedback_doctype():
	"""Cria o DocType Course Feedback manualmente se não existir"""

	# Se já existe, pular
	if frappe.db.exists("DocType", "Course Feedback"):
		return

	# Importar e criar o DocType
	import json
	import os

	doctype_path = os.path.join(
		os.path.dirname(__file__),
		"satisfacao/doctype/course_feedback/course_feedback.json"
	)

	if os.path.exists(doctype_path):
		with open(doctype_path, "r", encoding="utf-8") as f:
			doctype_data = json.load(f)

		# Criar DocType
		doc = frappe.get_doc(doctype_data)
		doc.insert(ignore_if_duplicate=True)
		frappe.db.commit()
