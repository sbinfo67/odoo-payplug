# Copyright 2026 Sébastien Berger (sbinfo67)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo.tests import tagged

from odoo.addons.account_payment.tests.common import AccountPaymentCommon

from .common import PayplugCommon


@tagged("post_install", "-at_install", "payment_payplug")
class TestPayplugAccountMove(PayplugCommon, AccountPaymentCommon):
    """The field the shop synchronisation writes to, so transfers can be reconciled."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.invoice = cls.init_invoice(
            "out_invoice", partner=cls.partner, amounts=[120.0], taxes=[], post=True
        )

    def test_reference_is_stored_and_searchable(self):
        self.invoice.payplug_payment_ref = "pay_5iHMDxy4ABR4YBVW4UscIn"

        self.assertEqual(
            self.env["account.move"].search(
                [("payplug_payment_ref", "=", "pay_5iHMDxy4ABR4YBVW4UscIn")]
            ),
            self.invoice,
            "The reconciliation script looks invoices up by this field.",
        )

    def test_instalment_reference_is_accepted(self):
        # A payment in instalments is identified by its plan, not by a payment.
        self.invoice.payplug_payment_ref = "inst_1AbCdEfGhIjKlMnOpQrStU"

        self.assertEqual(
            self.invoice.payplug_payment_ref, "inst_1AbCdEfGhIjKlMnOpQrStU"
        )

    def test_reference_is_not_copied(self):
        self.invoice.payplug_payment_ref = "pay_5iHMDxy4ABR4YBVW4UscIn"

        # Carrying the identifier over would attach one payment to two invoices, and
        # the reconciliation would settle the wrong one.
        self.assertFalse(self.invoice.copy().payplug_payment_ref)
