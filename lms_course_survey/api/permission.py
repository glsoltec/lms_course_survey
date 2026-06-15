import frappe


def has_app_permission(user=None):
	"""
	Verifica se usuário tem permissão de acessar o app
	"""
	if not user:
		user = frappe.session.user

	# Administrador sempre tem acesso
	if "Administrator" in frappe.get_roles(user):
		return True

	# Professores/Instrutores têm acesso
	if "Instructor" in frappe.get_roles(user) or "Teacher" in frappe.get_roles(user):
		return True

	# Usuários comuns também podem acessar
	return frappe.db.exists("User", user)
