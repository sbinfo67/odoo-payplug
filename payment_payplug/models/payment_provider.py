# Copyright 2026 Sébastien Berger (sbinfo67)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import urls

from odoo.addons.payment.logging import get_payment_logger

from .. import const

_logger = get_payment_logger(__name__, sensitive_keys=const.SENSITIVE_KEYS)


class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    code = fields.Selection(
        selection_add=[("payplug", "Payplug")],
        ondelete={"payplug": "set default"},
    )
    payplug_secret_key = fields.Char(
        help="The secret key of your Payplug account: a test key (sk_test_...) in "
        "test mode, a live key (sk_live_...) when the provider is enabled.",
        required_if_provider="payplug",
        copy=False,
        groups="base.group_system",
    )

    # === COMPUTE METHODS === #

    def _compute_feature_support_fields(self):
        """Override of `payment` to enable additional features."""
        res = super()._compute_feature_support_fields()
        self.filtered(lambda p: p.code == "payplug").update(
            {
                "support_refund": "partial",
            }
        )
        return res

    def _get_supported_currencies(self):
        """Override of `payment` to return the supported currencies."""
        supported_currencies = super()._get_supported_currencies()
        if self.code == "payplug":
            supported_currencies = supported_currencies.filtered(
                lambda c: c.name in const.SUPPORTED_CURRENCIES
            )
        return supported_currencies

    # === CONSTRAINT METHODS === #

    @api.constrains("state", "payplug_secret_key")
    def _check_payplug_secret_key_matches_state(self):
        """Prevent using a live key in test mode, and a test key on an enabled provider.

        Payplug serves both modes on the same endpoints; the key alone decides whether
        real money is charged. A mismatch would either charge customers during tests or
        accept fake payments in production.
        """
        for provider in self.sudo().filtered(
            lambda p: p.code == "payplug"
            and p.state != "disabled"
            and p.payplug_secret_key
        ):
            key = provider.payplug_secret_key.strip()
            if provider.state == "test" and not key.startswith(
                const.SECRET_KEY_PREFIX_TEST
            ):
                raise ValidationError(
                    self.env._(
                        "In test mode, the Payplug secret key must be a test key "
                        "(starting with %s).",
                        const.SECRET_KEY_PREFIX_TEST,
                    )
                )
            if provider.state == "enabled" and not key.startswith(
                const.SECRET_KEY_PREFIX_LIVE
            ):
                raise ValidationError(
                    self.env._(
                        "When the provider is enabled, the Payplug secret key must be "
                        "a live key (starting with %s).",
                        const.SECRET_KEY_PREFIX_LIVE,
                    )
                )

    # === CRUD METHODS === #

    def _get_default_payment_method_codes(self):
        """Override of `payment` to return the default payment method codes."""
        self.ensure_one()
        if self.code != "payplug":
            return super()._get_default_payment_method_codes()
        return const.DEFAULT_PAYMENT_METHOD_CODES

    def _get_reset_values(self):
        """Override of `payment` to also reset the secret key."""
        values = super()._get_reset_values()
        if self.code == "payplug":
            values["payplug_secret_key"] = False
        return values

    # === REQUEST HELPERS === #

    def _payplug_get_api_base_url(self):
        """Return the base URL of the Payplug API, ending with a slash.

        The URL can be overridden with a system parameter so that tests target a local
        fake server instead of the real API.
        """
        base_url = (
            self.env["ir.config_parameter"].sudo().get_param(const.API_BASE_URL_PARAM)
            or const.DEFAULT_API_BASE_URL
        )
        return base_url.rstrip("/") + "/"

    def _build_request_url(self, endpoint, **kwargs):
        """Override of `payment` to build the request URL."""
        if self.code != "payplug":
            return super()._build_request_url(endpoint, **kwargs)
        return urls.urljoin(self._payplug_get_api_base_url(), endpoint.strip("/"))

    def _build_request_headers(self, method, endpoint, payload, **kwargs):
        """Override of `payment` to build the request headers."""
        if self.code != "payplug":
            return super()._build_request_headers(method, endpoint, payload, **kwargs)
        secret_key = (self.sudo().payplug_secret_key or "").strip()
        return {
            "Accept": "application/json",
            "Authorization": f"Bearer {secret_key}",
            "Content-Type": "application/json",
            "PayPlug-Version": const.API_VERSION,
        }

    def _parse_response_error(self, response):
        """Override of `payment` to parse the error message."""
        if self.code != "payplug":
            return super()._parse_response_error(response)
        content = response.json()
        message = content.get("message") or response.text
        details = content.get("details")
        if details:
            message = f"{message} {details}"
        return message
