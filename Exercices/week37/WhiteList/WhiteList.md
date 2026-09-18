# Challenge Whitelist

## But du jeu
Tu dois faire en sorte que dans Ubuntu (dans VirtualBox), seuls ces 3 sites soient accessibles :
- galaxus.ch
- youtube.ch    
- notion.com

Tout le reste doit être bloqué.

On va utiliser :
- **Squid** : un proxy qui filtre les sites.
- **nftables** : un pare-feu qui empêche de contourner le proxy.

⚠️ **Important** : tout se passe **dans la machine virtuelle Ubuntu**. Windows 11 ne sera pas modifié.

---

## Étape 1 : Créer la VM Ubuntu
1. Télécharge Ubuntu 22.04 ou 24.04 (fichier ISO).
2. Ouvre VirtualBox.
3. Clique sur "Nouvelle".
4. Nom : Ubuntu-Whitelist, Type : Linux, Version : Ubuntu (64-bit).
5. Mémoire : 4096 Mo (4 Go). Disque : 25 Go.
6. Dans "Réseau", laisse **NAT** (par défaut).
7. Installe Ubuntu normalement.

---

## Étape 2 : Ouvrir un terminal
Dans Ubuntu, fais `Ctrl+Alt+T` pour ouvrir le terminal.

---

## Étape 3 : Mettre à jour le système
Tape :
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install squid conntrack -y
sudo systemctl restart squid
sudo systemctl enable squid
    