# 💼 Portfolio – Anton  
**Apprenti développeur d’applications (CFC) · EPFL, Lausanne**  
🛠️ Python · JavaScript · APIs · Blockchain · Automatisation

---

## 🤖 1. Bot Telegram – Trading Solana

**Achetez et vendez des tokens (meme tokens) Solana depuis Telegram.**

- 🔐 **Sécurité** : la clé privée est saisie une fois, effacée automatiquement, stockée uniquement en mémoire vive.
- 📈 **Achat** : entrez l’adresse du contrat → le bot récupère les infos (Jupiter + Helius) → affiche un devis (prix, impact, frais) → signature de la transaction.
- 📉 **Vente** : le bot liste vos tokens → choisissez un pourcentage (25 %, 50 %, 75 % ou 100 %).
- ⚙️ **Paramètres** : slippage ajustable par utilisateur.
- 🧩 **Architecture** : code modulaire (config, états, claviers, services) – facile à faire évoluer.

---

## 📊 2. Détecteur d’arbitrage – Polymarket

**Scanne les événements toutes les 60 secondes** pour repérer les écarts de prix.

- 🎯 **Principe** : la somme des prix des options « Oui » doit être proche de 1.0. Toute déviation = opportunité d’arbitrage.
- 📬 **Alertes** : envoi automatique sur Telegram avec le détail de l’écart.
- 🐞 **Correction technique** : l’API CLOB `/midpoints` attend un tableau simple → ajustement effectué. Fallback via une autre API pour les marchés sans carnet d’ordres.
- ✅ **Résultat concret** : détection d’un vrai candidat (*Balance of Power*) avec un écart de **+1,85 %** et un volume de **22 000 $** – preuve de fonctionnement en conditions réelles.

---

## 💎 3. Scraper de boutiques de luxe – Natkina

**Recherche de points de vente pour une marque de joaillerie.**

- 🗺️ **Source** : OpenStreetMap (API Overpass) – recherche par tags (`shop=jewelry`, `shop=watches`, etc.).
- 🧹 **Nettoyage** : unification des adresses, ajout des coordonnées GPS, récupération du site web et des horaires (si disponibles).
- 📤 **Export** : fichier CSV prêt pour l’équipe commerciale.
- 🔄 **Reprise** : possibilité de continuer après une interruption sans rescanner les mêmes zones.
- 🏆 **Résultat** : **plus de 800 boutiques** identifiées en Suisse et dans les grandes villes européennes – remplaçant une recherche manuelle fastidieuse.

---

## ⚡ Technologies transversales

| Domaine | Outils / Langages |
|---------|-------------------|
| Langages | Python, JavaScript/Node.js, HTML/CSS |
| Asynchrone | `asyncio`, `httpx` |
| Blockchain | Solana, Jupiter, Helius, `solders`, `solana-py` |
| Bots Telegram | `aiogram 3.x` (FSM, claviers) |
| APIs & données | REST, JSON-LD, CSV, scraping avec reprise |
| Versionnage | Git, loguru, environnements Debian |