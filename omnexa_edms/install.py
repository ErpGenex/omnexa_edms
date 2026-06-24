# Copyright (c) 2026, Omnexa and contributors
# License: MIT

import frappe


def after_install():
	_bootstrap()


def after_migrate():
	_bootstrap()


def _bootstrap():
	_ensure_roles()
	_hide_legacy_document_control_workspace()
	try:
		from omnexa_edms.workspace.edms_workspace import sync_edms_workspace_menu

		sync_edms_workspace_menu(save=True, rebuild=True)
	except Exception:
		frappe.log_error(frappe.get_traceback(), "EDMS: workspace sync failed")


def _hide_legacy_document_control_workspace():
	"""Remove engineering Document Control from public desk sidebar."""
	if not frappe.db.exists("Workspace", "Document Control"):
		return
	frappe.db.set_value("Workspace", "Document Control", "public", 0, update_modified=False)
	frappe.db.set_value("Workspace", "Document Control", "is_hidden", 1, update_modified=False)
	frappe.clear_cache(doctype="Workspace")


def _ensure_roles():
	for role_name in ("Omnexa EDMS User",):
		if frappe.db.exists("Role", role_name):
			frappe.db.set_value("Role", role_name, "desk_access", 1, update_modified=False)
			continue
		frappe.get_doc({"doctype": "Role", "role_name": role_name, "desk_access": 1}).insert(ignore_permissions=True)
