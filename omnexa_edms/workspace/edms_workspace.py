# Copyright (c) 2026, Omnexa and contributors
# License: MIT

"""Electronic Archive workspace — replaces legacy Document Control sidebar entry."""

from __future__ import annotations

import json

import frappe

from omnexa_core.omnexa_core.vertical_workspace_sync import (
	build_link_rows_for_app,
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

_SHORTCUT_COLORS = ("Blue", "Green", "Orange", "Red", "Cyan", "Purple")


def _build_link_rows() -> list[dict]:
	return build_link_rows_for_app("omnexa_edms", WORKSPACE_SECTIONS)


def _build_shortcuts(link_rows: list[dict]) -> list[dict]:
	shortcuts: list[dict] = []
	idx = 0
	for row in link_rows:
		if row.get("type") != "Link":
			continue
		lt = row.get("link_type")
		entry = {
			"label": row["label"],
			"link_to": row["link_to"],
			"type": lt,
			"color": _SHORTCUT_COLORS[idx % len(_SHORTCUT_COLORS)],
		}
		if lt == "DocType":
			entry["doc_view"] = "List"
		if lt == "Report" and row.get("report_ref_doctype"):
			entry["report_ref_doctype"] = row["report_ref_doctype"]
		shortcuts.append(entry)
		idx += 1
		if idx >= 8:
			break
	return shortcuts


def _build_content(link_rows: list[dict]) -> str:
	content = [
		{
			"id": "edms-title",
			"type": "header",
			"data": {"text": '<span class="h4"><b>Electronic Archive</b></span>', "col": 12},
		}
	]
	link_idx = 0
	for row in link_rows:
		if row.get("type") == "Card Break":
			continue
		content.append(
			{
				"id": f"edms-lnk-{link_idx}",
				"type": "shortcut",
				"data": {"shortcut_name": row["label"], "col": 4},
			}
		)
		link_idx += 1
	return json.dumps(content, separators=(",", ":"))


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
	for sc in _build_shortcuts(rows):
		ws.append("shortcuts", sc)
	stats["shortcuts"] = len(ws.shortcuts or [])
	drop_missing_workspace_dashboard_links(ws)
	ws.content = _build_content(rows)
	ws.public = 1
	ws.is_hidden = 0
	if save:
		ws.flags.ignore_permissions = True
		ws.flags.ignore_version = True
		ws.save()
		frappe.clear_cache(doctype="Workspace")
	return stats
