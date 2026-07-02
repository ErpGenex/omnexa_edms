# Copyright (c) 2026, Omnexa and contributors
# License: MIT. See license.txt

"""Basic import smoke tests for omnexa_edms."""

from frappe.tests.utils import FrappeTestCase

from omnexa_edms.edms_global_benchmark import get_global_edms_score


class TestEdmsSmoke(FrappeTestCase):
	def test_benchmark_module(self):
		out = get_global_edms_score()
		self.assertIsInstance(out, dict)
