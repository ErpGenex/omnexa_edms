# Copyright (c) 2026, Omnexa and contributors
# License: MIT


def execute():
	from omnexa_edms.workspace.edms_workspace import sync_edms_workspace_menu

	sync_edms_workspace_menu(save=True, rebuild=True)
