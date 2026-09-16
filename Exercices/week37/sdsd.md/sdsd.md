# Partage de fichiers en réseau — marche à suivre pas à pas

> Procédure réellement appliquée en laboratoire, sur des postes **Windows 11** intégrés au domaine **intranet.epfl.ch**.
> Toutes les commandes sont à exécuter dans **PowerShell lancé en tant qu'administrateur**.

| | Machine qui partage (serveur) | Machine qui se connecte (client) |
|---|---|---|
| Nom | `SCX-A104008` | `……………………` |
| Adresse IP | `128.179.203.222` | `……………………` |
| Interface | Wi-Fi EPFL | Wi-Fi EPFL |
| Profil réseau | `DomainAuthenticated` | `DomainAuthenticated` |
| Compte utilisé | `partage` (compte **local**) | identifiants du serveur |

---

## Étape 0 — Vérifications préalables

- [ ] **0.1 Relever l'adresse IP** des deux postes :
  ```powershell
  ipconfig | findstr IPv4
  ```

- [ ] **0.2 Vérifier le profil réseau** :
  ```powershell
  Get-NetConnectionProfile
  ```
  → chez nous : `NetworkCategory : DomainAuthenticated`.
  ⚠️ En environnement de domaine, le profil **ne peut pas** être basculé en *Privé* : il est imposé par le contrôleur de domaine. Toute la configuration porte donc sur le profil **Domaine**.

- [ ] **0.3 Vérifier les droits d'administrateur** :
  ```powershell
  whoami /groups | findstr /i "S-1-5-32-544"
  ```
  → doit afficher `Enabled group`. Si la ligne indique `Group used for deny only`, la console n'est pas élevée : la relancer avec **Exécuter en tant qu'administrateur**.

- [ ] **0.4 Vérifier que le réseau laisse passer SMB** — depuis le poste client, vers le futur serveur :
  ```powershell
  Test-NetConnection 128.179.203.222 -Port 445
  ```
  `TcpTestSucceeded : True` → le réseau ne bloque pas le port 445, on peut continuer sans câble croisé ni machines virtuelles.

---

## Étape 1 — Créer le compte de partage (sur le serveur)

- [ ] **1.1** Créer un compte **local** dédié :
  ```powershell
  net user partage Motdepasse1! /add
  ```

- [ ] **1.2** Empêcher l'expiration du mot de passe :
  ```powershell
  Set-LocalUser -Name partage -PasswordNeverExpires $true
  ```
  ⚠️ L'ancienne commande `wmic useraccount ... set PasswordExpires=false` **ne fonctionne plus** : `wmic` a été retiré de Windows 11. Il faut utiliser le module `Microsoft.PowerShell.LocalAccounts`.

- [ ] **1.3** Contrôler :
  ```powershell
  Get-LocalUser -Name partage | Format-List Name, Enabled, PasswordExpires
  ```
  → `Enabled : True` et `PasswordExpires` vide.

> **Pourquoi un compte local et pas le compte de domaine ?** Un compte sans mot de passe est refusé en accès réseau par défaut, et un compte local reste valable même si le poste perd le contact avec le contrôleur de domaine.

---

## Étape 2 — Créer et partager le dossier (sur le serveur)

- [ ] **2.1** Créer le dossier :
  ```powershell
  mkdir C:\Partage
  ```

- [ ] **2.2** Partager le dossier (niveau **SMB**) :
  ```powershell
  net share Partage=C:\Partage /grant:partage,CHANGE
  ```

- [ ] **2.3** Donner les droits **NTFS** :
  ```powershell
  icacls C:\Partage /grant "partage:(OI)(CI)M"
  ```
  ⚠️ Les guillemets sont **obligatoires** dans PowerShell : sans eux, `(OI)` est interprété comme une commande à exécuter et la ligne échoue avec `The term 'OI' is not recognized`. En `cmd.exe`, les guillemets ne sont pas nécessaires.
  `(OI)` = héritage aux fichiers, `(CI)` = héritage aux sous-dossiers, `M` = Modification.

- [ ] **2.4** Vérifier les **deux** niveaux :
  ```powershell
  net share Partage
  icacls C:\Partage
  ```
  Résultat attendu :
  ```
  Permission        SCX-A104008\partage, CHANGE
  C:\Partage        SCX-A104008\partage:(OI)(CI)(M)
  ```

> **Règle essentielle :** le droit effectif est **le plus restrictif** entre l'autorisation de partage (SMB) et l'autorisation NTFS. Configurer un seul des deux niveaux donne un dossier visible mais non modifiable.

---

## Étape 3 — Activer la découverte et vérifier le pare-feu (sur le serveur)

- [ ] **3.1 Interface graphique** : Paramètres → Réseau et Internet → Paramètres réseau avancés → **Paramètres de partage avancés** → déplier la section **Réseaux de domaine** :
  - Découverte de réseau : **Activé**
  - Partage de fichiers et d'imprimantes : **Activé**

- [ ] **3.2 Vérifier les règles de pare-feu** :
  ```powershell
  Get-NetFirewallRule -Group "@FirewallAPI.dll,-28502" |
    Select-Object DisplayName, Enabled, Profile, Direction | Format-Table -AutoSize
  ```
  ⚠️ Aucun espace après la virgule dans `"@FirewallAPI.dll,-28502"`, sinon : *Aucun objet MSFT_NetFirewallRule trouvé*.
  La règle à contrôler est **SMB-Entrée**, profil **Domain**, direction **Inbound** → `Enabled : True`.

- [ ] **3.3** Les activer si nécessaire :
  ```powershell
  Get-NetFirewallRule -Group "@FirewallAPI.dll,-28502" | Enable-NetFirewallRule
  ```

- [ ] **3.4 Vérifier que le service écoute bien sur IPv4** :
  ```powershell
  netstat -an | findstr ":445"
  ```
  Résultat attendu :
  ```
  TCP    0.0.0.0:445      0.0.0.0:0      LISTENING
  TCP    [::]:445         [::]:0         LISTENING
  ```
  ⚠️ `Get-NetTCPConnection -LocalPort 445 -State Listen` n'affiche parfois que la ligne IPv6 `::` et laisse croire qu'IPv4 n'écoute pas. `netstat -an` donne la vue complète — c'est lui qui fait foi.

---

## Étape 4 — Se connecter depuis le poste client

- [ ] **4.1** Purger d'éventuelles sessions précédentes :
  ```powershell
  net use * /delete /y
  ```
  Windows n'accepte **qu'un seul jeu d'identifiants par serveur distant** : une première tentative ratée bloque les suivantes.

- [ ] **4.2** Se connecter :
  ```powershell
  net use \\128.179.203.222\Partage /user:SCX-A104008\partage Motdepasse1!
  ```
  → `The command completed successfully.`

  ⚠️ Le nom d'utilisateur doit impérativement être préfixé du **nom de la machine serveur** : `SCX-A104008\partage`. Saisi seul, `partage` est interprété comme `INTRANET\partage`, compte qui n'existe pas dans le domaine → **accès refusé**.

- [ ] **4.3** Version graphique : `Win + R` → `\\128.179.203.222\Partage` → mêmes identifiants → cocher **Mémoriser mes informations d'identification**.

- [ ] **4.4** Monter un lecteur réseau permanent :
  ```powershell
  net use Z: \\128.179.203.222\Partage /user:SCX-A104008\partage Motdepasse1! /persistent:yes
  net use
  ```

- [ ] **4.5** Vérifier l'accès en lecture et en écriture :
  ```powershell
  dir \\128.179.203.222\Partage
  echo test > \\128.179.203.222\Partage\test-client.txt
  ```

---

## Étape 5 — Tests à réaliser et à documenter

| # | Depuis | Action | Résultat attendu | OK |
|---|---|---|---|---|
| 1 | Client | Créer `test-client.txt` dans le partage | Le fichier apparaît dans `C:\Partage` sur le serveur | ☐ |
| 2 | Serveur | Modifier le contenu du fichier | Modification visible côté client après **F5** | ☐ |
| 3 | Client | Créer un sous-dossier `Documents` | Visible des deux côtés | ☐ |
| 4 | Client | Supprimer un fichier **via le partage** | Suppression **définitive** — le fichier ne va dans aucune corbeille | ☐ |
| 5 | Serveur | Supprimer un fichier en local | Il disparaît aussi côté client | ☐ |
| 6 | Les deux | Ouvrir le même document Word simultanément | Le second poste l'ouvre en **lecture seule** (verrouillage SMB) | ☐ |
| 7 | Client | Copier un fichier volumineux | Transfert complet, débit conforme au lien Wi-Fi | ☐ |

📸 Faire une capture d'écran à chaque test pour le document de groupe.

---

## Étape 6 — Diagnostic en cas de problème

Commandes utilisées pendant la manipulation, dans l'ordre logique :

```powershell
# 1. Le client atteint-il le serveur sur le port SMB ?
Test-NetConnection <IP_serveur> -Port 445

# 2. Le partage existe-t-il et avec quels droits ?
net share Partage
icacls C:\Partage

# 3. Le service écoute-t-il en IPv4 et IPv6 ?
netstat -an | findstr ":445"

# 4. Le pare-feu laisse-t-il entrer SMB sur le profil du domaine ?
Get-NetFirewallRule -Group "@FirewallAPI.dll,-28502" |
  Select-Object DisplayName, Enabled, Profile, Direction | Format-Table -AutoSize

# 5. Une stratégie interdit-elle l'ouverture de session réseau aux comptes locaux ?
secedit /export /cfg "$env:TEMP\sec.inf" | Out-Null
Select-String -Path "$env:TEMP\sec.inf" -Pattern "SeDenyNetworkLogonRight"
#   → chez nous : "Invité" uniquement. Si le SID S-1-5-113 (comptes locaux)
#     y figure, aucun compte local ne peut se connecter par le réseau.

# 6. Les tentatives d'authentification échouent-elles réellement ? (sur le serveur)
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4625; StartTime=(Get-Date).AddMinutes(-5)} `
  -ErrorAction SilentlyContinue | Format-List TimeCreated, Message

# 7. Test d'authentification isolé, sans passer par le partage
net use \\<IP_serveur>\IPC$ /user:SCX-A104008\partage Motdepasse1!
#   Erreur 5  → authentification / droits
#   Erreur 53 ou 64 → blocage réseau
```

> Remarque sur l'étape 6 : `Get-WinEvent -LogName Security -MaxEvents 20 | Where-Object {$_.Id -eq 4625}` ne donne rien d'exploitable, car les 20 événements les plus récents sont filtrés **après** extraction et le journal d'un poste de domaine se remplit très vite. Il faut filtrer côté fournisseur avec `-FilterHashtable`.

---

## Étape 7 — Difficultés rencontrées et solutions

| Symptôme / message | Cause | Solution |
|---|---|---|
| `wmic : The term 'wmic' is not recognized` | `wmic` supprimé de Windows 11 | `Set-LocalUser -Name partage -PasswordNeverExpires $true` |
| `OI : The term 'OI' is not recognized` | PowerShell interprète les parenthèses comme un sous-bloc de code | Encadrer l'argument : `icacls C:\Partage /grant "partage:(OI)(CI)M"` |
| `Aucun objet MSFT_NetFirewallRule trouvé` | Espace parasite dans `"@FirewallAPI.dll, -28502"` | Écrire la valeur sans espace |
| `access is denied` à la connexion | Nom d'utilisateur saisi sans le nom de la machine → interprété comme un compte de domaine | Se connecter en `SCX-A104008\partage` |
| Le profil réseau reste sur *Domaine* | Catégorie imposée par le contrôleur de domaine | Configurer le partage sur le profil **Domaine** au lieu de chercher à passer en *Privé* |
| `Group used for deny only` sur le groupe Administrateurs | Console PowerShell non élevée (filtrage UAC) | Relancer en tant qu'administrateur |
| Le port 445 semble n'écouter qu'en IPv6 | Affichage partiel de `Get-NetTCPConnection` | Contrôler avec `netstat -an \| findstr ":445"` |
| Aucun événement 4625 dans le journal | Filtrage effectué après extraction des 20 derniers événements | Utiliser `-FilterHashtable @{LogName='Security'; Id=4625; StartTime=…}` |
| Dossier visible mais non modifiable | Un seul des deux niveaux d'autorisations configuré | Configurer **partage SMB** *et* **NTFS** |
| Conflit d'identifiants à la seconde tentative | Session SMB déjà ouverte vers le même serveur | `net use * /delete /y` puis reconnexion |

---

## Étape 8 — Points importants à retenir

- En environnement de domaine, le profil réseau est **imposé** : la configuration se fait sur le profil *Domaine*, pas sur *Privé*.
- Deux niveaux d'autorisations sous Windows — **partage SMB** et **NTFS** — et c'est le plus restrictif qui s'applique.
- Un compte **local** avec mot de passe est nécessaire ; le nom doit toujours être préfixé du nom de la machine serveur.
- Tester **d'abord par adresse IP** : cela sépare un problème de partage d'un problème de résolution de noms.
- Une suppression effectuée à travers un partage réseau est **définitive** : aucune corbeille, ni côté client, ni côté serveur.
- Deux outils qui mesurent la même chose ne donnent pas toujours la même réponse (`Get-NetTCPConnection` vs `netstat`) : croiser les sources avant de conclure à une panne.
- Plusieurs commandes issues de la documentation Windows 10 ne fonctionnent plus telles quelles sous Windows 11 (`wmic`), et la syntaxe `cmd` n'est pas toujours transposable directement dans PowerShell (`icacls`).

---

## Bonus — partage avec Linux (les deux sens)

### A. Monter le partage Windows sur Linux

```bash
sudo apt update && sudo apt install -y cifs-utils smbclient

smbclient -L //128.179.203.222 -U partage          # lister les partages

sudo mkdir -p /mnt/partage-win
sudo mount -t cifs //128.179.203.222/Partage /mnt/partage-win \
  -o username=partage,vers=3.1.1,uid=$(id -u),gid=$(id -g),\
iocharset=utf8,file_mode=0664,dir_mode=0775

touch /mnt/partage-win/essai-linux.txt              # doit apparaître dans C:\Partage
```

| Option | Rôle |
|---|---|
| `vers=3.1.1` | Force SMB 3.1.1 (chiffré et signé) |
| `uid=` / `gid=` | Sans elles, tout appartient à `root` et rien n'est modifiable |
| `file_mode` / `dir_mode` | SMB ne transporte pas les droits Unix, on les simule |
| `iocharset=utf8` | Accents corrects dans les noms de fichiers |

### B. Partage Samba sur Linux, accès depuis Windows

```bash
sudo apt install -y samba wsdd
sudo mkdir -p /srv/partage
sudo chown $USER:$USER /srv/partage && sudo chmod 2775 /srv/partage
sudo smbpasswd -a $USER && sudo smbpasswd -e $USER
```

`/etc/samba/smb.conf` :

```ini
[global]
   workgroup = WORKGROUP
   security = user
   server min protocol = SMB2_10      ; jamais SMB1
   server max protocol = SMB3_11
   map to guest = never
   unix charset = UTF-8

[partage]
   path = /srv/partage
   browseable = yes
   read only = no
   valid users = anton
   create mask = 0664
   directory mask = 0775
   vfs objects = recycle
   recycle:repository = .corbeille
```

```bash
testparm                              # vérifier la syntaxe
sudo systemctl restart smbd nmbd
sudo systemctl enable --now wsdd      # visibilité dans le voisinage réseau Windows
sudo ufw allow samba
```

Depuis Windows : `\\<IP_Linux>\partage`, compte Linux + **mot de passe `smbpasswd`** (distinct de celui de la session).

> Depuis Windows 10, la navigation du voisinage réseau reposait sur SMB1, désormais désactivé : un serveur Samba n'apparaît plus automatiquement dans l'Explorateur. `wsdd` rétablit cet affichage ; l'accès direct par `\\adresse-IP` fonctionne dans tous les cas.

### C. Différences observées

| Critère | Windows 11 | Linux (Samba) |
|---|---|---|
| Mise en place | Interface graphique ou quelques commandes, rien à installer | Installation de Samba, édition de `smb.conf`, redémarrage du service |
| Droits | Deux niveaux : partage SMB + ACL NTFS | Droits POSIX `rwx` + directives `smb.conf` |
| Comptes | Une seule base | Compte Unix **et** base Samba (`smbpasswd`) — deux mots de passe possibles |
| Sensibilité à la casse | Insensible | Sensible → deux fichiers distincts |
| Découverte réseau | Intégrée (WSD) | Nécessite `wsdd` |
| Corbeille | Aucune sur les suppressions réseau | Possible avec `vfs objects = recycle` |
| Diagnostic | Observateur d'événements, `net share` | `testparm`, `smbclient`, `journalctl -u smbd` — messages plus précis |
| Reproductibilité | Réglages répartis entre plusieurs fenêtres | Un seul fichier texte, sauvegardable et versionnable |

**Conclusion :** Windows est plus rapide à mettre en œuvre grâce à l'interface, mais les contraintes du domaine (profil imposé, stratégies de groupe) compliquent le diagnostic. Linux demande plus de configuration initiale mais centralise tout dans un fichier et fournit des messages d'erreur nettement plus exploitables. Les deux systèmes coopèrent sans difficulté tant que l'on reste en **SMB2/SMB3** et que l'on passe par **l'adresse IP**.

---

## Checklist avant de rendre

- [ ] Les 7 tests de l'étape 5 sont réalisés et capturés
- [ ] Bonus Linux réalisé dans les deux sens
- [ ] Noms des membres du groupe, noms des machines et adresses IP renseignés
- [ ] Difficultés réellement rencontrées ajoutées au tableau de l'étape 7
- [ ] Document validé et signé par le formateur laboratoire
- [ ] Document joint au **Rapport de formation**