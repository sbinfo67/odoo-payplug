# Copyright 2026 Sébastien Berger (sbinfo67)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

import datetime
import json

from odoo.exceptions import ValidationError
from odoo.tests import tagged
from odoo.tools import mute_logger

from .common import PayplugOAuth2Common

LOGGERS = (
    "odoo.addons.payment_payplug.models.payment_provider",
    "odoo.addons.payment.models.payment_provider",
)
CSV = (
    "id,processing_date_utc,type,amount_(€),api_id,processing_id\n"
    "1,2026-10-24 18:37:00,Payment,9450,pay_a,\n"
    "2,2026-10-26 09:43:52,Transfer,-9177,,cfcded66-cd80\n"
)
START = datetime.date(2026, 10, 1)
END = datetime.date(2026, 10, 31)


@tagged("post_install", "-at_install", "payment_payplug")
class TestPayplugAccountingReport(PayplugOAuth2Common):
    def setUp(self):
        super().setUp()
        self.fake_payplug.state.accounting_report_csv = CSV

    def _api_requests(self, path_prefix="/v1/accounting_reports"):
        return [
            (method, path, headers, body)
            for method, path, headers, body in self.fake_payplug.state.requests
            if path.startswith(path_prefix)
        ]

    def test_create_report(self):
        report = self.payplug._payplug_create_accounting_report(START, END)
        self.assertTrue(report["id"].startswith("ar_"))
        self.assertFalse(report["temporary_url"])
        method, _path, headers, body = self._api_requests()[0]
        self.assertEqual(method, "POST")
        self.assertEqual(
            json.loads(body), {"start_date": "2026-10-01", "end_date": "2026-10-31"}
        )
        self.assertTrue(headers["User-Agent"].startswith("Odoo-payment_payplug"))

    def test_create_report_invalid_period(self):
        with self.assertRaises(ValidationError):
            self.payplug._payplug_create_accounting_report(END, START)
        with self.assertRaises(ValidationError):
            self.payplug._payplug_create_accounting_report(None, END)
        self.assertFalse(self._api_requests())

    def test_fetch_waits_for_the_file(self):
        self.fake_payplug.state.accounting_report_polls = 3
        report, text = self.payplug._payplug_fetch_accounting_report(
            START, END, max_wait=10, poll_interval=0.01
        )
        self.assertEqual(text, CSV)  # Byte order mark removed.
        self.assertTrue(report["temporary_url"])
        methods = [method for method, *_rest in self._api_requests()]
        self.assertEqual(methods, ["POST", "GET", "GET", "GET"])
        # The file is downloaded without the API credentials, with a User-Agent.
        (_path, headers), *_ = self.fake_payplug.state.file_requests
        self.assertNotIn("Authorization", headers)
        self.assertTrue(headers["User-Agent"].startswith("Odoo-payment_payplug"))

    def test_fetch_timeout(self):
        self.fake_payplug.state.accounting_report_polls = 1000
        with self.assertRaisesRegex(ValidationError, "still not ready"):
            self.payplug._payplug_fetch_accounting_report(
                START, END, max_wait=0.05, poll_interval=0.01
            )
        self.assertFalse(self.fake_payplug.state.file_requests)

    def test_get_report_refuses_invalid_identifiers(self):
        for report_id in ("../payments", "a/b", "", None, "x" * 65):
            with self.assertRaises(ValidationError):
                self.payplug._payplug_get_accounting_report(report_id)
        self.assertFalse(self._api_requests())

    @mute_logger(*LOGGERS)
    def test_get_unknown_report(self):
        with self.assertRaises(ValidationError):
            self.payplug._payplug_get_accounting_report("ar_unknown")

    def test_download_refuses_foreign_plain_http(self):
        for url in (
            "http://storage.example.com/report.csv",
            "ftp://storage.example.com/report.csv",
            "",
            None,
        ):
            with self.assertRaisesRegex(ValidationError, "download link"):
                self.payplug._payplug_download_accounting_report(
                    {"id": "ar_x", "temporary_url": url}
                )
        self.assertFalse(self.fake_payplug.state.file_requests)

    @mute_logger(*LOGGERS)
    def test_download_missing_file(self):
        url = f"{self.fake_payplug.public_url}/_files/accounting_reports/ar_none.csv"
        with self.assertRaisesRegex(ValidationError, "HTTP 404"):
            self.payplug._payplug_download_accounting_report(
                {"id": "ar_none", "temporary_url": url}
            )

    def test_user_agent_on_every_request(self):
        headers = self.payplug._build_request_headers("GET", "payments/pay_x", None)
        self.assertEqual(headers["User-Agent"], self.payplug._payplug_get_user_agent())
