# Omnexa EDMS

Electronic document archiving and records management (**الأرشفة الإلكترونية**).

Replaces the legacy **Document Control** engineering sidebar entry with a dedicated app workspace **Electronic Archive**, while reusing the central `Omnexa Document Register` from `omnexa_eng_document_control`.

```bash
bench --site <site> install-app omnexa_edms
bench --site <site> migrate
```
