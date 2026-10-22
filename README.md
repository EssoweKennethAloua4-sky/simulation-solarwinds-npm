# Simulation de SolarWinds NPM en Python

Travail pratique du cours **CSC 242 – Algorithmique et programmation orientée objet**, IPNET Institute of Technology (Lomé), année 2025-2026.
Auteur : **Essowe Kenneth Aloua**.

## Le sujet

SolarWinds Network Performance Monitor (NPM) est un logiciel payant de supervision réseau. Il interroge les routeurs, commutateurs et serveurs avec le protocole SNMP, conserve les mesures et prévient quand un seuil est dépassé.

Ce projet n'installe pas ce logiciel : il en **reproduit le fonctionnement en programmation orientée objet**.

## Ce que fait le programme

1. Il découvre un petit réseau de 4 appareils : un routeur, un commutateur, un serveur de production et un serveur de sauvegarde.
2. À chaque cycle, il interroge chaque appareil comme le ferait SNMP (processeur, mémoire, bande passante, latence).
3. Il enregistre les mesures dans une base de données en mémoire.
4. Il compare chaque mesure à des seuils et lève une alerte si besoin.
5. Il affiche un tableau de bord dans le terminal, puis exporte un rapport `npm_report.json`.

| Mesure | Seuil | Gravité |
| --- | --- | --- |
| Processeur | > 80 % | Avertissement |
| Mémoire | > 85 % | Critique |
| Bande passante | > 90 % | Avertissement |

Les valeurs sont tirées au hasard : chaque exécution est différente.

## Lancer le programme

Python 3 suffit, aucune bibliothèque à installer :

```
python simulation_npm.py
```

## Organisation du code

| Bloc | Classes |
| --- | --- |
| États | `DeviceStatus`, `DeviceType`, `AlertSeverity`, `AlertStatus`, `InterfaceStatus` |
| Réseau | `NetworkDevice`, `Router`, `Switch`, `NetworkInterface`, `Metric` |
| SNMP | `SNMPAgent`, `SNMPCollector` |
| Découverte | `NetworkDiscovery`, `NetworkTopologyMap` |
| Alertes | `AlertRule`, `Alert`, `AlertEngine` |
| Stockage | `Database` |
| Pilotage | `Dashboard`, `NPMSystem` |

`Router` et `Switch` héritent de `NetworkDevice` : ils reprennent tout ce que possède un appareil réseau et ajoutent ce qui leur est propre.

## Documents

- [Tableau des classes](docs/tableau-des-classes.pdf)
- [Rapport du projet](docs/rapport.pdf)
