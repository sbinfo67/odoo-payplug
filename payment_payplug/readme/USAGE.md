**Paiement sur le site web ou depuis le portail**

Le client choisit *Carte* (ou un autre moyen activé), est redirigé vers la page Payplug,
paie, puis revient sur la page d'état du paiement d'Odoo. La commande ou la facture est
confirmée dès qu'Odoo a relu le paiement auprès de Payplug, soit au retour du client,
soit à la réception de la notification.

Si le client clique sur *Annuler* sur la page Payplug, le paiement est abandonné chez
Payplug et la transaction passe à l'état *Annulée*. Un paiement refusé passe à l'état
*Erreur* avec le motif donné par Payplug ; un paiement jamais terminé est annulé quand
Payplug signale son expiration (environ 15 minutes).

**Remboursement**

Depuis le paiement (*Comptabilité > Clients > Paiements*), ou depuis la facture via son
paiement, cliquez sur *Rembourser* et indiquez le montant (total ou partiel). Odoo
demande le remboursement à Payplug, crée une transaction de remboursement liée à la
transaction d'origine, puis le paiement comptable négatif correspondant.

Un remboursement fait directement dans le portail Payplug est aussi enregistré dans
Odoo, à la réception de sa notification.

Payplug n'accepte pas de remboursement inférieur à 0,10 €.

**Vérifier une transaction**

Sur une transaction Payplug en attente ou en erreur, le bouton *Vérifier le statut sur
Payplug* relit le paiement auprès de Payplug et met la transaction à jour (utile si une
notification n'a pas pu arriver).

**Référence de paiement Payplug sur la facture**

Les factures clients portent un champ *Payplug Payment Reference*
(`payplug_payment_ref`), à côté de la référence de paiement, dans l'onglet des
informations complémentaires.

Il sert au rapprochement des virements Payplug. Un virement regroupe plusieurs
paiements, frais déduits, et son libellé bancaire ne porte aucune référence de
commande : ni le nom du client ni la référence de la commande ne suffisent à retrouver
à quelle facture il se rapporte. L'identifiant du paiement, lui, est sans ambiguïté.

Le champ ne concerne que les ventes encaissées **hors d'Odoo**, typiquement une
boutique PrestaShop dont la synchronisation l'alimente. Un paiement pris par Odoo
lui-même — page de paiement, lien de paiement — garde son identifiant sur sa
transaction (`payment.transaction.provider_reference`) et n'a pas besoin de ce champ.

Le contenu est l'identifiant brut tel que la boutique l'a enregistré : `pay_…` pour une
carte, `inst_…` pour un paiement en plusieurs fois. Le champ est indexé, et n'est pas
repris lors de la duplication d'une facture.
