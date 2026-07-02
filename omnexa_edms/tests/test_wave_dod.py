# Copyright (c) 2026, Omnexa and contributors
# License: MIT. See license.txt

"""Wave 1 DoD smoke — omnexa_edms."""

from frappe.tests.utils import FrappeTestCase

from omnexa_edms.edms_assessment import export_edms_global_audit
from omnexa_edms.edms_gap_register import get_gap_status
from omnexa_edms.edms_global_benchmark import get_global_edms_score


class TestWaveDoDEdms(FrappeTestCase):
	def test_global_edms_score(self):
		score = get_global_edms_score()
		self.assertIn("weighted_score", score)

	def test_gap_register(self):
		gaps = get_gap_status()
		self.assertIn("gaps_open", gaps)

	def test_export_audit_api_callable(self):
		self.assertTrue(callable(export_edms_global_audit))
