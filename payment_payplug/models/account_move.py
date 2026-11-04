# Copyright 2026 Sébastien Berger (sbinfo67)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    # The bank transfers Payplug sends group several payments, fees deducted, and their
    # statement label carries no order reference. Reconciling them needs the payment
    # identifier on the invoice itself: neither the customer name nor the shop's order
    # reference is reliable enough.
    #
    # Invoices whose payment was taken by Odoo already reach their identifier through
    # `payment.transaction.provider_reference`. This field is for the other case: a sale
    # paid on the shop, where the identifier lives in PrestaShop and nowhere else.
    payplug_payment_ref = fields.Char(
        string="Payplug Payment Reference",
        index=True,
        copy=False,
        help=(
            "Identifier of the Payplug payment that settled this invoice, as the shop "
            "recorded it: 'pay_...' for a card payment, 'inst_...' for an instalment "
            "plan. Left empty for an order that did not go through the shop's Payplug "
            "module — a payment link issued from Odoo keeps its identifier on the "
            "payment transaction instead."
        ),
    )
