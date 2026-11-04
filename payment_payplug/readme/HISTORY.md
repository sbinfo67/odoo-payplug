## 19.0.1.3.0 (2026-11-04)

- Lecture du rapport comptable Payplug (`/accounting_reports`) : création, attente du
  fichier et téléchargement, pour les modules de rapprochement bancaire.
- En-tête `User-Agent` explicite sur toutes les requêtes envoyées à Payplug (Cloudflare
  refuse certaines signatures de client génériques).

## 19.0.1.1.0 (2026-10-24)

- Authentification OAuth2 (*client credentials*) au choix, à côté de la clé API : jetons
  d'accès de 5 minutes gardés en mémoire et renouvelés automatiquement, nouvelle demande
  et renvoi unique de la requête si Payplug refuse le jeton, contrôle de
  l'environnement (Test ou Live) du jeton.

## 19.0.1.0.0 (2026-10-24)

- Première version : paiement par la page hébergée Payplug, notifications,
  remboursements totaux et partiels, paiement des factures.
