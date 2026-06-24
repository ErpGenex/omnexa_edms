# Copyright (c) 2026, Omnexa and contributors
# License: MIT

"""Electronic Archive workspace — replaces legacy Document Control sidebar entry."""

from __future__ import annotations

import frappe

from omnexa_core.omnexa_core.vertical_workspace_sync import (
	build_content_from_link_rows,
	build_link_rows_for_app,
	build_shortcuts_from_link_rows,
	drop_missing_workspace_dashboard_links,
)

WorkspaceLink = tuple[str, str, str]

WORKSPACE_NAME = "Electronic Archive"

WORKSPACE_SECTIONS: list[tuple[str, list[WorkspaceLink]]] = [
	(
		"📁 Document Registry",
		[
			("DocType", "Omnexa Document Register", "Document Register"),
			("DocType", "Omnexa Document Control Settings", "Archive Settings"),
		],
	),
	(
		"📊 Archive Reports",
		[
			("Report", "Omnexa Document Registry Index", "Registry Index"),
			("Report", "Omnexa Document Compliance Summary", "Compliance Summary"),
		],
	),
	(
		"🔗 Vertical Sources",
		[
			("DocType", "Engineering Document Register", "Engineering Register"),
			("DocType", "Construction CDE Document", "Construction CDE"),
		],
	),
]


def _build_link_rows() -> list[dict]:
	return build_link_rows_for_app("omnexa_edms", WORKSPACE_SECTIONS)


def sync_edms_workspace_menu(*, save: bool = True, rebuild: bool = True) -> dict:
	stats = {"sections": 0, "links": 0, "shortcuts": 0}
	if not frappe.db.exists("Workspace", WORKSPACE_NAME):
		return stats
	rows = _build_link_rows()
	ws = frappe.get_doc("Workspace", WORKSPACE_NAME)
	if rebuild:
		ws.set("links", [])
		ws.set("shortcuts", [])
	for row in rows:
		if row.get("type") == "Card Break":
			stats["sections"] += 1
		else:
			stats["links"] += 1
		ws.append("links", row)
	for sc in build_shortcuts_from_link_rows(rows):
		ws.append("shortcuts", sc)
	stats["shortcuts"] = len(ws.shortcuts or [])
	drop_missing_workspace_dashboard_links(ws)
	ws.content = build_content_from_link_rows(rows, ws, title="Electronic Archive", slug="edms")
	ws.public = 1
	ws.is_hidden = 0
	if save:
		ws.flags.ignore_permissions = True
		ws.flags.ignore_version = True
		ws.save()
		frappe.clear_cache(doctype="Workspace")
	return stats
