app_name = "omnexa_edms"
app_title = "Omnexa EDMS"
app_publisher = "Omnexa"
app_description = "Electronic document archiving and records management (الأرشفة الإلكترونية)"
app_email = "edms@erpgenex.com"
app_license = "mit"

required_apps = ["omnexa_core", "omnexa_eng_document_control"]

add_to_apps_screen = [
	{
		"name": "omnexa_edms",
		"logo": "/assets/omnexa_edms/images/edms.svg",
		"title": "Electronic Archive",
		"route": "/app/electronic-archive"
	}
]

after_install = "omnexa_edms.install.after_install"
after_migrate = "omnexa_edms.install.after_migrate"
