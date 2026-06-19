import frappe


@frappe.whitelist()
def get_feedback_stats(course=None):
	"""
	Retorna estatísticas agregadas de feedback
	"""
	filters = {"docstatus": 1}

	if course:
		filters["course"] = course

	feedbacks = frappe.get_list(
		"Course Feedback",
		filters=filters,
		fields=["instructor_rating", "content_rating", "course_rating", "overall_rating"],
	)

	if not feedbacks:
		return {
			"total_feedbacks": 0,
			"instructor_avg": 0,
			"content_avg": 0,
			"course_avg": 0,
			"overall_avg": 0,
		}

	ratings_map = {"Péssimo": 1, "Ruim": 2, "Regular": 3, "Bom": 4, "Ótimo": 5}
	total = len(feedbacks)

	instructor_ratings = [ratings_map.get(f.get("instructor_rating"), 0) for f in feedbacks]
	content_ratings = [ratings_map.get(f.get("content_rating"), 0) for f in feedbacks]
	course_ratings = [ratings_map.get(f.get("course_rating"), 0) for f in feedbacks]
	overall_ratings = [ratings_map.get(f.get("overall_rating"), 0) for f in feedbacks]

	stats = {
		"total_feedbacks": total,
		"instructor_avg": round(sum(instructor_ratings) / total, 2) if total > 0 else 0,
		"content_avg": round(sum(content_ratings) / total, 2) if total > 0 else 0,
		"course_avg": round(sum(course_ratings) / total, 2) if total > 0 else 0,
		"overall_avg": round(sum(overall_ratings) / total, 2) if total > 0 else 0,
	}

	return stats


@frappe.whitelist()
def get_course_feedback_summary(course):
	"""
	Retorna resumo de feedback para um curso específico
	"""
	feedbacks = frappe.get_list(
		"Course Feedback",
		filters={"course": course, "docstatus": 1},
		fields=["instructor_rating", "content_rating", "course_rating", "overall_rating"],
	)

	if not feedbacks:
		return None

	ratings_map = {"Péssimo": 1, "Ruim": 2, "Regular": 3, "Bom": 4, "Ótimo": 5}
	total = len(feedbacks)

	summary = {
		"total": total,
		"instructor": round(
			sum(ratings_map.get(f.get("instructor_rating"), 0) for f in feedbacks) / total, 2
		) if total > 0 else 0,
		"content": round(
			sum(ratings_map.get(f.get("content_rating"), 0) for f in feedbacks) / total, 2
		) if total > 0 else 0,
		"course": round(
			sum(ratings_map.get(f.get("course_rating"), 0) for f in feedbacks) / total, 2
		) if total > 0 else 0,
		"overall": round(
			sum(ratings_map.get(f.get("overall_rating"), 0) for f in feedbacks) / total, 2
		) if total > 0 else 0,
	}

	return summary
