**Clés Payplug**

1. Dans le portail Payplug, à la rubrique des clés d'API, générez une clé
   de type **API Key** (clé secrète) en environnement **Test** et, plus tard, une clé en
   environnement **Live**. Les clés actuelles sont des jetons JWT (`eyJ...`) ; les
   anciennes clés `sk_test_...` et `sk_live_...` sont aussi acceptées.
   La clé publique n'est pas utilisée : le module ne passe que par la page de paiement
   hébergée.
2. Dans Odoo, ouvrez *Facturation (ou Comptabilité) > Configuration > Fournisseurs de
   paiement* et choisissez **Payplug**.
3. Dans l'onglet *Identifiants*, collez la clé secrète. Seuls les administrateurs
   (groupe *Paramètres*) peuvent la lire ou la modifier.
4. Réglez l'état :
   - **Mode test** avec une clé de l'environnement Test : aucun débit réel ;
   - **Activé** avec une clé de l'environnement Live : paiements réels.

   Pour une ancienne clé `sk_...`, Odoo refuse une clé de production en mode test et
   une clé de test sur un fournisseur activé. Pour une clé JWT, l'accord entre le mode
   et la clé est vérifié à chaque paiement : un paiement dont le mode ne correspond
   pas est refusé.
5. Dans l'onglet *Configuration*, vérifiez le journal de paiement et les moyens de
   paiement. Par défaut, seul *Carte* (CB, Visa, Mastercard) est activé. Bancontact,
   iDEAL et MyBank sont proposés, mais ne les activez qu'après les avoir fait ouvrir sur
   votre compte Payplug.
6. Publiez le fournisseur pour qu'il apparaisse sur le site web.

**Adresse de notification (webhook)**

Le module donne à Payplug, pour chaque paiement, l'adresse
`https://<votre-domaine>/payment/payplug/webhook`. Il n'y a rien à saisir dans le portail
Payplug, mais cette adresse doit être joignable depuis Internet en HTTPS :

- ne la protégez pas par une authentification, un filtrage IP ou une règle de pare-feu
  (WAF, fail2ban, Cloudflare…) qui bloquerait les requêtes POST de Payplug ;
- vérifiez le paramètre système `web.base.url` (ou le domaine du site web) : c'est lui
  qui sert à construire les adresses de retour et de notification.

Les retours du client passent par `/payment/payplug/return` et `/payment/payplug/cancel`.

**Paramètre système réservé aux tests**

`payment_payplug.api_base_url` remplace l'adresse de l'API Payplug
(`https://api.payplug.com/v1/` par défaut). Il ne sert qu'à pointer vers un faux serveur
de test ; ne le créez pas en production.
