# Interconnexion : Switch 🌐💻

## Matériel requis
- Vos PC (au moins 2)
  - Ubuntu / Windows
- Câble RJ45
- Switch

---

## Exercice 1 : Ping direct entre PC

1. Reproduisez cette configuration réseau :  

> Ajoute ton prénom sur l’un des PCs et fais en sorte qu'il respecte cette configuration réseau :  

| PC  | IP à attribuer       | Nom|
|-----|----------------------|----- |
| PC0 | 192.168.1.10         | *Réservé* |
| PC1 | 192.168.1.11         | |
| PC2 | 192.168.1.12         | |
| PC3 | 192.168.1.13         | |
| PC4 | 192.168.1.14         | |
| PC5 | 192.168.1.15         | |
| PC6 | 192.168.1.16         | |
| PC7 | 192.168.1.17         | |
| PC8 | 192.168.1.18         | |
| PCx | ...                  | |

1. Configurez votre IP en **statique**.
   1. Quelle est la différence entre une ip statique et une ip dynamique ?
   2. En quoi c'est utile de configurer une machine en ip statique ?
2. Connectez un câble RJ45 directement entre deux PCs.
3. Faites un **ping** (Ubuntu puis Windows) entre vos machines.

**Questions :**  
- Que se passe-t-il lors du ping ?  
- Comment mettre l’IP en statique sous Windows et Linux ?  
- Avez vous rencontré des problèmes techniques ? Si oui, lesquelles ?
- Quelle est la différence **technique** entre ces trois mots clés :
<img width="386" height="264" alt="image" src="https://github.com/user-attachments/assets/1f3e61bc-fd4c-4aa3-b513-d83ffebff1cc" />
 

---

## Exercice 2 : Ajout d’un switch

1. Connectez plusieurs PCs à un **switch**.
2. Essayez de vous pinguer entre toutes les machines.
3. Faites un **schéma réseau** indiquant les IP et les connexions.

**Questions :**  
- Que se passe-t-il ?  
- Quels comportements réseau observez-vous ?
- Avez vous rencontré des problèmes techniques ? Si oui, lesquelles ?

---

## Exercice 3 : Tests supplémentaires

Essayez les commandes suivantes et observez les résultats :  

- [ ] `ping`  
- [ ] `nmap`  
- [ ] `tracert` / `trace route`  
- [ ] `scp`  

---

## Exercice 4 : Analyse des problèmes

1. Listez tous les problèmes éventuels rencontrés pendant les exercices.  
   1. Notez vos solutions ou hypothèses pour les résoudre.

---

## Exercice 5 : Créer un schéma réseau 

1. Créer un schéma réseau de l'infrastructure en l'état
---

# Bonus 1  : Bad Luck ? ✨✨

Trois ordinateurs sont connectés au même switch avec cette configuration.

> Reproduisez la configuration suivante et essayez de trouver le problème 🤔

| PC | Adresse IP | Masque |
|---|---|---|
| PC1 | 192.168.1.10 | 255.255.255.0 |
| PC2 | 192.168.1.20 | 255.255.0.0 |
| PC3 | 192.168.2.30 | 255.255.255.0 |

1. Reprenez le schéma créé au point 5 et montrez visuellement les erreurs.
2. Quelle commande utiliser pour tester le problème ?
3. D'où vient le problème ?
4. Est-ce que les trois ordinateurs peuvent communiquer ensemble ?
5. Expliquez pourquoi cette configuration ne fonctionne pas correctement.
6. Corrigez les paramètres réseau pour que les trois PC soient dans le même réseau.

---

# Bonus 2 : Rework ✨✨✨

Vous avez mandaté votre apprenti·e afin de résoudre le problème du `Bonus 1`.

Mais.. mais.. mais.. un autre souci est apparu à cause de la configuration suivante 🥲 :

| PC | Adresse IP | Masque |
|---|---|---|
| PC1 | 192.168.10.50 | 255.255.255.192 |
| PC2 | 192.168.10.100 | 255.255.255.192 |
| PC3 | 192.168.10.130 | 255.255.255.192 |

1. Reprenez le schéma créé au point 5 et montrez visuellement les erreurs.
2. Quelle commande utiliser pour tester le problème ?
3. D'où vient le problème ?
4. Est-ce que les trois ordinateurs peuvent communiquer ensemble ?
5. Expliquez pourquoi cette configuration ne fonctionne pas correctement.
6. Corrigez les paramètres réseau pour que les trois PC soient dans le même réseau.

💡 Astuce : prenez des notes sur chaque étape, et n’hésitez pas à dessiner vos schémas directement sur papier ou avec un outil numérique.