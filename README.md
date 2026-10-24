

# Payplug pour Odoo
<!-- /!\ Non OCA Context : Set here the badge of your runbot / runboat instance. -->
[![Pre-commit Status](https://github.com/sbinfo67/odoo-payplug/actions/workflows/pre-commit.yml/badge.svg?branch=19.0)](https://github.com/sbinfo67/odoo-payplug/actions/workflows/pre-commit.yml?query=branch%3A19.0)
[![Build Status](https://github.com/sbinfo67/odoo-payplug/actions/workflows/test.yml/badge.svg?branch=19.0)](https://github.com/sbinfo67/odoo-payplug/actions/workflows/test.yml?query=branch%3A19.0)
[![codecov](https://codecov.io/gh/sbinfo67/odoo-payplug/branch/19.0/graph/badge.svg)](https://codecov.io/gh/sbinfo67/odoo-payplug)
<!-- /!\ Non OCA Context : Set here the badge of your translation instance. -->

<!-- /!\ do not modify above this line -->

Fournisseur de paiement [Payplug](https://www.payplug.com/) pour le cadre de paiement
d'Odoo 19 : paiement par la page hébergée Payplug sur le site web et le portail client
(commandes, factures, liens de paiement), notifications serveur, remboursements totaux
et partiels.

La documentation (installation, configuration des clés de test et de production,
adresse de notification à laisser ouverte, remboursements, limites connues) se trouve
dans le [README du module](payment_payplug/README.rst).

**Installation rapide**

1. Copiez le dossier `payment_payplug` dans un chemin d'extensions d'Odoo 19 (ou
   installez le paquet Python construit depuis `payment_payplug/pyproject.toml`).
2. Mettez à jour la liste des applications, puis installez *Payment Provider:
   Payplug*. Le module dépend de `payment` et `account_payment`.
3. Configurez le fournisseur dans *Facturation > Configuration > Fournisseurs de
   paiement > Payplug*.

**Avertissement :** ce projet est indépendant ; il n'est ni affilié à Payplug, ni
approuvé par Payplug.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[payment_payplug](payment_payplug/) | 19.0.1.0.0 | <a href='https://github.com/sbinfo67'><img src='https://github.com/sbinfo67.png' width='32' height='32' style='border-radius:50%;' alt='sbinfo67'/></a> | Payplug payment provider: hosted payment page, refunds

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [LGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Odoo Community Association (OCA)
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
<!-- /!\ Non OCA Context : Set here the full description of your organization. -->
