#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SolarWinds Network Performance Monitor - Simulation POO
Implémentation complète du système de monitoring réseau basé sur la POO

Filière: Réseaux, Système, Sécurité et Cybersécurité
Date: 2026
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple
from enum import Enum
from datetime import datetime, timedelta
import random
import time
from abc import ABC, abstractmethod
import json


# ==================== ENUMS ====================

class DeviceStatus(Enum):
    """Énumération des états possibles d'un appareil"""
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    UNREACHABLE = "UNREACHABLE"
    DEGRADED = "DEGRADED"


class DeviceType(Enum):
    """Types d'appareils réseau"""
    ROUTER = "ROUTER"
    SWITCH = "SWITCH"
    SERVER = "SERVER"
    FIREWALL = "FIREWALL"


class AlertSeverity(Enum):
    """Niveaux de sévérité des alertes"""
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    EMERGENCY = "EMERGENCY"


class AlertStatus(Enum):
    """Statuts possibles des alertes"""
    ACTIVE = "ACTIVE"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    RESOLVED = "RESOLVED"


class InterfaceStatus(Enum):
    """Statuts des interfaces réseau"""
    UP = "UP"
    DOWN = "DOWN"
    DISABLED = "DISABLED"


# ==================== CLASSES DE BASE ====================

@dataclass
class NetworkInterface:
    """Représente une interface réseau (port) d'un appareil"""
    interface_id: str
    interface_name: str
    bandwidth_usage: float = 0.0  # en %
    packet_loss: float = 0.0  # en %
    latency: float = 0.0  # en ms
    mtu: int = 1500
    status: InterfaceStatus = InterfaceStatus.UP
    last_error: Optional[str] = None
    
    def collect_metrics(self):
        """Collecte les métriques de l'interface"""
        self.bandwidth_usage = random.uniform(10, 95)
        self.packet_loss = random.uniform(0, 5)
        self.latency = random.uniform(1, 50)
        
    def is_healthy(self) -> bool:
        """Vérifie si l'interface fonctionne normalement"""
        return (self.status == InterfaceStatus.UP and 
                self.bandwidth_usage < 85 and 
                self.packet_loss < 2)
    
    def get_performance_data(self) -> Dict:
        """Retourne un dictionnaire des données de performance"""
        return {
            "interface_id": self.interface_id,
            "bandwidth_usage": round(self.bandwidth_usage, 2),
            "packet_loss": round(self.packet_loss, 2),
            "latency": round(self.latency, 2),
            "status": self.status.value
        }


@dataclass
class Metric:
    """Représente une métrique collectée du réseau"""
    metric_id: str
    metric_name: str
    value: float
    timestamp: datetime
    unit: str
    device_id: str
    interface_id: Optional[str] = None
    
    def is_valid(self) -> bool:
        """Vérifie si la métrique est valide"""
        return self.value >= 0 and isinstance(self.timestamp, datetime)
    
    def get_formatted_value(self) -> str:
        """Retourne la valeur formatée avec unité"""
        return f"{round(self.value, 2)} {self.unit}"
    
    def is_anomaly(self) -> bool:
        """Détecte si la valeur est anormale (heuristique simple)"""
        if self.metric_name == "cpu_usage":
            return self.value > 95
        elif self.metric_name == "bandwidth_usage":
            return self.value > 90
        elif self.metric_name == "packet_loss":
            return self.value > 5
        elif self.metric_name == "latency":
            return self.value > 100
        return False
    
    def to_dict(self) -> Dict:
        """Convertit la métrique en dictionnaire"""
        return {
            "metric_id": self.metric_id,
            "metric_name": self.metric_name,
            "value": round(self.value, 2),
            "timestamp": self.timestamp.isoformat(),
            "unit": self.unit,
            "device_id": self.device_id,
            "interface_id": self.interface_id
        }


@dataclass
class NetworkDevice:
    """Classe de base pour tous les appareils réseau"""
    device_id: str
    ip_address: str
    hostname: str
    device_type: DeviceType
    status: DeviceStatus = DeviceStatus.ONLINE
    mac_address: str = ""
    interfaces: List[NetworkInterface] = field(default_factory=list)
    last_seen_time: datetime = field(default_factory=datetime.now)
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    
    def get_status(self) -> DeviceStatus:
        """Retourne le statut courant de l'appareil"""
        return self.status
    
    def update_metrics(self, metrics: List[Metric]):
        """Met à jour les métriques de l'appareil"""
        for metric in metrics:
            if metric.device_id == self.device_id:
                if metric.metric_name == "cpu_usage":
                    self.cpu_usage = metric.value
                elif metric.metric_name == "memory_usage":
                    self.memory_usage = metric.value
    
    def is_online(self) -> bool:
        """Vérifie si l'appareil est connecté"""
        return self.status == DeviceStatus.ONLINE
    
    def add_interface(self, interface: NetworkInterface):
        """Ajoute une interface réseau"""
        self.interfaces.append(interface)
    
    def get_interfaces(self) -> List[NetworkInterface]:
        """Retourne la liste des interfaces"""
        return self.interfaces
    
    def simulate_status(self):
        """Simule un changement aléatoire du statut"""
        chance = random.random()
        if chance < 0.02:  # 2% de chance de changement
            self.status = random.choice([DeviceStatus.OFFLINE, DeviceStatus.DEGRADED])
        elif chance < 0.05:  # Retour à online
            self.status = DeviceStatus.ONLINE
        
        self.cpu_usage = random.uniform(10, 80)
        self.memory_usage = random.uniform(20, 85)
        self.last_seen_time = datetime.now()
    
    def to_dict(self) -> Dict:
        """Convertit l'appareil en dictionnaire"""
        return {
            "device_id": self.device_id,
            "ip_address": self.ip_address,
            "hostname": self.hostname,
            "device_type": self.device_type.value,
            "status": self.status.value,
            "cpu_usage": round(self.cpu_usage, 2),
            "memory_usage": round(self.memory_usage, 2)
        }


@dataclass
class Router(NetworkDevice):
    """Classe représentant un routeur"""
    routing_protocol: str = "OSPF"
    throughput: float = 100.0  # Gbps
    
    def get_routing_table(self) -> List[Tuple[str, str]]:
        """Récupère la table de routage simulée"""
        return [
            ("192.168.1.0/24", "eth0"),
            ("192.168.2.0/24", "eth1"),
            ("10.0.0.0/8", "eth2")
        ]
    
    def forward_packet(self, dest_ip: str) -> bool:
        """Simule l'acheminement d'un paquet"""
        return random.random() > 0.05  # 95% de succès


@dataclass
class Switch(NetworkDevice):
    """Classe représentant un commutateur"""
    vlan_count: int = 10
    mac_table_size: int = 4096
    backplane_speed: float = 48.0  # Gbps
    
    def get_vlan_table(self) -> List[Dict]:
        """Retourne la table VLAN simulée"""
        return [
            {"vlan_id": i, "name": f"VLAN_{i}"} 
            for i in range(1, min(self.vlan_count + 1, 5))
        ]
    
    def forward_frame(self, mac_dest: str) -> bool:
        """Simule l'acheminement d'une trame Ethernet"""
        return random.random() > 0.02  # 98% de succès


@dataclass
class Alert:
    """Représente une alerte système"""
    alert_id: str
    severity: AlertSeverity
    message: str
    triggered_time: datetime
    resolved_time: Optional[datetime] = None
    status: AlertStatus = AlertStatus.ACTIVE
    device_id: Optional[str] = None
    metric_name: Optional[str] = None
    
    def trigger(self):
        """Déclenche l'alerte"""
        self.status = AlertStatus.ACTIVE
        self.triggered_time = datetime.now()
    
    def resolve(self):
        """Résout l'alerte"""
        self.status = AlertStatus.RESOLVED
        self.resolved_time = datetime.now()
    
    def get_severity(self) -> AlertSeverity:
        """Retourne le niveau de sévérité"""
        return self.severity
    
    def to_dict(self) -> Dict:
        """Convertit l'alerte en dictionnaire"""
        return {
            "alert_id": self.alert_id,
            "severity": self.severity.value,
            "message": self.message,
            "status": self.status.value,
            "triggered_time": self.triggered_time.isoformat(),
            "device_id": self.device_id
        }


@dataclass
class AlertRule:
    """Représente une règle d'alerte"""
    rule_id: str
    metric_name: str
    condition: str  # "GREATER_THAN", "LESS_THAN", "EQUALS"
    threshold: float
    enabled: bool = True
    severity: AlertSeverity = AlertSeverity.WARNING
    
    def evaluate(self, metric: Metric) -> bool:
        """Évalue si une métrique viole la règle"""
        if not self.enabled or metric.metric_name != self.metric_name:
            return False
        
        if self.condition == "GREATER_THAN":
            return metric.value > self.threshold
        elif self.condition == "LESS_THAN":
            return metric.value < self.threshold
        elif self.condition == "EQUALS":
            return metric.value == self.threshold
        return False
    
    def matches(self, metric: Metric) -> bool:
        """Vérifie si la règle s'applique à la métrique"""
        return self.enabled and metric.metric_name == self.metric_name


# ==================== CLASSE SNMP ====================

@dataclass
class SNMPAgent:
    """Agent SNMP sur chaque appareil"""
    agent_id: str
    device_id: str
    ip_address: str
    
    def respond(self, request: Dict) -> Dict:
        """Simule une réponse SNMP"""
        return {
            "device_id": self.device_id,
            "cpu_usage": random.uniform(20, 80),
            "memory_usage": random.uniform(30, 85),
            "uptime": random.randint(1000000, 10000000)
        }
    
    def query(self, oid: str) -> Optional[str]:
        """Simule une requête SNMP OID"""
        # Simulation : retourner des informations système
        descriptions = {
            "1.3.6.1.2.1.1.1.0": f"Cisco Router {self.device_id}",
            "1.3.6.1.2.1.1.5.0": f"router-{self.device_id}",
        }
        return descriptions.get(oid, None)


@dataclass
class SNMPCollector:
    """Collecteur SNMP pour sonder les appareils"""
    collector_id: str
    devices: List[NetworkDevice] = field(default_factory=list)
    poll_interval: int = 60  # secondes
    metrics: List[Metric] = field(default_factory=list)
    is_running: bool = False
    
    def poll(self) -> List[Metric]:
        """Lance le sondage de tous les appareils"""
        new_metrics = []
        
        for device in self.devices:
            if device.is_online():
                metrics = self.collect_metrics_from_device(device)
                new_metrics.extend(metrics)
                self.metrics.extend(metrics)
        
        return new_metrics
    
    def collect_metrics_from_device(self, device: NetworkDevice) -> List[Metric]:
        """Collecte les métriques d'un appareil spécifique"""
        device.simulate_status()
        metrics = []
        
        # Métrique CPU
        cpu_metric = Metric(
            metric_id=f"cpu_{device.device_id}_{datetime.now().timestamp()}",
            metric_name="cpu_usage",
            value=device.cpu_usage,
            timestamp=datetime.now(),
            unit="%",
            device_id=device.device_id
        )
        metrics.append(cpu_metric)
        
        # Métrique Mémoire
        memory_metric = Metric(
            metric_id=f"mem_{device.device_id}_{datetime.now().timestamp()}",
            metric_name="memory_usage",
            value=device.memory_usage,
            timestamp=datetime.now(),
            unit="%",
            device_id=device.device_id
        )
        metrics.append(memory_metric)
        
        # Métriques d'interfaces
        for interface in device.interfaces:
            interface.collect_metrics()
            
            bw_metric = Metric(
                metric_id=f"bw_{interface.interface_id}_{datetime.now().timestamp()}",
                metric_name="bandwidth_usage",
                value=interface.bandwidth_usage,
                timestamp=datetime.now(),
                unit="%",
                device_id=device.device_id,
                interface_id=interface.interface_id
            )
            metrics.append(bw_metric)
            
            latency_metric = Metric(
                metric_id=f"lat_{interface.interface_id}_{datetime.now().timestamp()}",
                metric_name="latency",
                value=interface.latency,
                timestamp=datetime.now(),
                unit="ms",
                device_id=device.device_id,
                interface_id=interface.interface_id
            )
            metrics.append(latency_metric)
        
        return metrics
    
    def add_device(self, device: NetworkDevice):
        """Ajoute un appareil à sonder"""
        self.devices.append(device)
    
    def start_polling(self):
        """Lance le polling continu"""
        self.is_running = True
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Collecteur {self.collector_id} démarré")
    
    def stop_polling(self):
        """Arrête le polling"""
        self.is_running = False
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Collecteur {self.collector_id} arrêté")


# ==================== DÉCOUVERTE RÉSEAU ====================

@dataclass
class NetworkTopologyMap:
    """Carte de la topologie réseau"""
    devices: List[NetworkDevice] = field(default_factory=list)
    connections: List[Tuple[str, str]] = field(default_factory=list)
    
    def add_node(self, device: NetworkDevice):
        """Ajoute un nœud à la topologie"""
        if device not in self.devices:
            self.devices.append(device)
    
    def add_connection(self, device1_id: str, device2_id: str):
        """Ajoute une connexion entre deux appareils"""
        connection = (device1_id, device2_id)
        if connection not in self.connections:
            self.connections.append(connection)
    
    def build_topology(self, devices: List[NetworkDevice]):
        """Construit la topologie réseau"""
        self.devices = devices
        self.connections.clear()
        
        # Simule des connexions
        for i, device in enumerate(devices):
            if i < len(devices) - 1:
                self.add_connection(device.device_id, devices[i + 1].device_id)
    
    def visualize(self) -> str:
        """Retourne une représentation textuelle de la topologie"""
        result = "=== TOPOLOGIE RÉSEAU ===\n"
        result += f"Appareils: {len(self.devices)}\n"
        for device in self.devices:
            result += f"  - {device.hostname} ({device.ip_address}) [{device.status.value}]\n"
        return result


@dataclass
class NetworkDiscovery:
    """Effectue la découverte automatique des appareils réseau"""
    ip_range: str
    discovered_devices: List[NetworkDevice] = field(default_factory=list)
    topology: Optional[NetworkTopologyMap] = None
    
    def discover_network(self) -> List[NetworkDevice]:
        """Découvre les appareils dans une plage IP"""
        # Simulation : créer quelques appareils
        self.discovered_devices.clear()
        
        devices = [
            Router(
                device_id="R1",
                ip_address="192.168.1.1",
                hostname="router-main",
                device_type=DeviceType.ROUTER
            ),
            Switch(
                device_id="S1",
                ip_address="192.168.1.2",
                hostname="switch-floor1",
                device_type=DeviceType.SWITCH
            ),
            NetworkDevice(
                device_id="SRV1",
                ip_address="192.168.1.10",
                hostname="server-prod",
                device_type=DeviceType.SERVER
            ),
            NetworkDevice(
                device_id="SRV2",
                ip_address="192.168.1.11",
                hostname="server-backup",
                device_type=DeviceType.SERVER
            ),
        ]
        
        # Ajouter des interfaces
        devices[0].add_interface(NetworkInterface("eth0", "Ethernet0"))
        devices[0].add_interface(NetworkInterface("eth1", "Ethernet1"))
        devices[1].add_interface(NetworkInterface("gi0", "GigabitEthernet0"))
        devices[1].add_interface(NetworkInterface("gi1", "GigabitEthernet1"))
        
        self.discovered_devices = devices
        self.topology = NetworkTopologyMap()
        self.topology.build_topology(devices)
        
        return devices
    
    def query_device_info(self, ip_address: str) -> Optional[Dict]:
        """Récupère les infos d'un appareil"""
        return {
            "ip": ip_address,
            "hostname": f"device-{ip_address.split('.')[-1]}",
            "type": DeviceType.SERVER
        }


# ==================== MOTEUR D'ALERTE ====================

@dataclass
class AlertEngine:
    """Moteur d'alerte du système"""
    alert_rules: List[AlertRule] = field(default_factory=list)
    active_alerts: List[Alert] = field(default_factory=list)
    all_alerts: List[Alert] = field(default_factory=list)
    
    def evaluate_metrics(self, metrics: List[Metric]):
        """Évalue toutes les métriques contre les règles"""
        for rule in self.alert_rules:
            if rule.enabled:
                for metric in metrics:
                    if rule.matches(metric):
                        if rule.evaluate(metric):
                            self.trigger_alert(rule, metric)
    
    def trigger_alert(self, rule: AlertRule, metric: Metric):
        """Déclenche une alerte"""
        alert = Alert(
            alert_id=f"alert_{metric.device_id}_{datetime.now().timestamp()}",
            severity=rule.severity,
            message=f"[{rule.metric_name.upper()}] Seuil dépassé: {metric.get_formatted_value()}",
            triggered_time=datetime.now(),
            device_id=metric.device_id,
            metric_name=rule.metric_name
        )
        alert.trigger()
        
        # Vérifier si une alerte similaire existe déjà
        existing = [a for a in self.active_alerts if a.device_id == alert.device_id and a.metric_name == alert.metric_name]
        if not existing:
            self.active_alerts.append(alert)
            self.all_alerts.append(alert)
    
    def resolve_alert(self, alert_id: str):
        """Résout une alerte"""
        for alert in self.active_alerts:
            if alert.alert_id == alert_id:
                alert.resolve()
                self.active_alerts.remove(alert)
    
    def add_alert_rule(self, rule: AlertRule):
        """Ajoute une nouvelle règle d'alerte"""
        self.alert_rules.append(rule)
    
    def get_active_alerts_summary(self) -> Dict:
        """Retourne un résumé des alertes actives"""
        by_severity = {}
        for alert in self.active_alerts:
            severity = alert.severity.value
            if severity not in by_severity:
                by_severity[severity] = 0
            by_severity[severity] += 1
        return by_severity


# ==================== BASE DE DONNÉES ====================

@dataclass
class Database:
    """Gestionnaire de base de données"""
    metrics: List[Metric] = field(default_factory=list)
    alerts: List[Alert] = field(default_factory=list)
    
    def store_metric(self, metric: Metric):
        """Stocke une métrique"""
        if metric.is_valid():
            self.metrics.append(metric)
    
    def store_metrics(self, metrics: List[Metric]):
        """Stocke plusieurs métriques"""
        for metric in metrics:
            self.store_metric(metric)
    
    def store_alert(self, alert: Alert):
        """Stocke une alerte"""
        self.alerts.append(alert)
    
    def query_metrics(self, device_id: str, metric_name: Optional[str] = None) -> List[Metric]:
        """Récupère les métriques pour un appareil"""
        results = [m for m in self.metrics if m.device_id == device_id]
        if metric_name:
            results = [m for m in results if m.metric_name == metric_name]
        return results
    
    def get_latest_metrics(self, device_id: str, count: int = 10) -> List[Metric]:
        """Récupère les dernières métriques"""
        metrics = [m for m in self.metrics if m.device_id == device_id]
        return sorted(metrics, key=lambda m: m.timestamp, reverse=True)[:count]


# ==================== DASHBOARD ====================

@dataclass
class Dashboard:
    """Interface de visualisation du système"""
    network_map: Optional[NetworkTopologyMap] = None
    alerts: List[Alert] = field(default_factory=list)
    metrics_summary: Dict = field(default_factory=dict)
    
    def update_network_map(self, devices: List[NetworkDevice]):
        """Met à jour la carte réseau"""
        if self.network_map is None:
            self.network_map = NetworkTopologyMap()
        self.network_map.build_topology(devices)
    
    def display_alerts(self, alerts: List[Alert]):
        """Affiche les alertes"""
        self.alerts = alerts
    
    def update_performance_charts(self, metrics: List[Metric]):
        """Met à jour les graphiques de performance"""
        for metric in metrics:
            if metric.metric_name not in self.metrics_summary:
                self.metrics_summary[metric.metric_name] = []
            self.metrics_summary[metric.metric_name].append(metric.value)
    
    def render(self) -> str:
        """Affiche l'état du dashboard"""
        output = "\n" + "="*60 + "\n"
        output += "          SOLARWINDS NETWORK PERFORMANCE MONITOR\n"
        output += "="*60 + "\n\n"
        
        if self.network_map:
            output += self.network_map.visualize()
            output += "\n"
        
        output += f"[ALERTES] Actives: {len(self.alerts)}\n"
        for alert in self.alerts[:5]:
            output += f"  ⚠ [{alert.severity.value}] {alert.message}\n"
        
        output += "\n[MÉTRIQUES]\n"
        for metric_name, values in list(self.metrics_summary.items())[:5]:
            avg_value = sum(values) / len(values) if values else 0
            output += f"  - {metric_name}: {avg_value:.2f}\n"
        
        output += "\n" + "="*60 + "\n"
        return output


# ==================== SYSTÈME PRINCIPAL ====================

@dataclass
class NPMSystem:
    """Système complet SolarWinds NPM"""
    collector: Optional[SNMPCollector] = None
    discovery: Optional[NetworkDiscovery] = None
    alert_engine: Optional[AlertEngine] = None
    database: Optional[Database] = None
    dashboard: Optional[Dashboard] = None
    is_running: bool = False
    cycle_count: int = 0
    
    def initialize(self):
        """Initialise le système"""
        print("[INIT] Initialisation du système NPM...")
        
        # Découverte réseau
        self.discovery = NetworkDiscovery(ip_range="192.168.1.0/24")
        devices = self.discovery.discover_network()
        print(f"[INIT] {len(devices)} appareils découverts")
        
        # Collecteur SNMP
        self.collector = SNMPCollector(collector_id="COLLECTOR_1")
        for device in devices:
            self.collector.add_device(device)
        self.collector.start_polling()
        
        # Moteur d'alerte
        self.alert_engine = AlertEngine()
        self.alert_engine.add_alert_rule(AlertRule(
            rule_id="rule_cpu",
            metric_name="cpu_usage",
            condition="GREATER_THAN",
            threshold=80,
            severity=AlertSeverity.WARNING
        ))
        self.alert_engine.add_alert_rule(AlertRule(
            rule_id="rule_memory",
            metric_name="memory_usage",
            condition="GREATER_THAN",
            threshold=85,
            severity=AlertSeverity.CRITICAL
        ))
        self.alert_engine.add_alert_rule(AlertRule(
            rule_id="rule_bandwidth",
            metric_name="bandwidth_usage",
            condition="GREATER_THAN",
            threshold=90,
            severity=AlertSeverity.WARNING
        ))
        
        # Base de données
        self.database = Database()
        
        # Dashboard
        self.dashboard = Dashboard()
        self.dashboard.update_network_map(devices)
        
        print("[INIT] Système NPM initialisé avec succès\n")
    
    def run(self, cycles: int = 5):
        """Lance la simulation du système"""
        self.is_running = True
        self.initialize()
        
        print(f"[RUN] Démarrage de la simulation ({cycles} cycles de 60 secondes)\n")
        
        for cycle in range(cycles):
            self.cycle_count = cycle + 1
            print(f"\n{'='*60}")
            print(f"CYCLE {self.cycle_count}/{cycles}")
            print(f"{'='*60}")
            print(f"[{datetime.now().strftime('%H:%M:%S')}]", end=" ")
            
            # Étape 1 : Collecte des métriques
            print("Collecte SNMP...", end=" ")
            metrics = self.collector.poll()
            print(f"✓ ({len(metrics)} métriques)")
            
            # Étape 2 : Stockage en base
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Stockage en BD...", end=" ")
            self.database.store_metrics(metrics)
            print(f"✓ ({len(self.database.metrics)} total)")
            
            # Étape 3 : Évaluation des alertes
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Évaluation alertes...", end=" ")
            self.alert_engine.evaluate_metrics(metrics)
            print(f"✓ ({len(self.alert_engine.active_alerts)} actives)")
            
            # Étape 4 : Mise à jour du dashboard
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Mise à jour dashboard...", end=" ")
            self.dashboard.update_network_map(self.collector.devices)
            self.dashboard.display_alerts(self.alert_engine.active_alerts)
            self.dashboard.update_performance_charts(metrics)
            print("✓")
            
            # Affichage du dashboard
            print(self.dashboard.render())
            
            # Détection changements réseau (optionnel)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Vérification topologie...", end=" ")
            new_devices = self.discovery.discover_network()
            print(f"✓ ({len(new_devices)} appareils)")
            
            # Pause avant prochain cycle
            if cycle < cycles - 1:
                print(f"[PAUSE] Attente 3 secondes avant prochain cycle...")
                time.sleep(3)
        
        self.stop()
    
    def stop(self):
        """Arrête le système proprement"""
        self.is_running = False
        if self.collector:
            self.collector.stop_polling()
        print("\n[STOP] Système NPM arrêté")
        print(f"[STAT] Cycles exécutés: {self.cycle_count}")
        print(f"[STAT] Métriques collectées: {len(self.database.metrics)}")
        print(f"[STAT] Alertes générées: {len(self.alert_engine.all_alerts)}")
    
    def export_report(self, filename: str):
        """Exporte un rapport JSON"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "cycles": self.cycle_count,
            "devices": [d.to_dict() for d in self.collector.devices],
            "metrics_count": len(self.database.metrics),
            "alerts": [a.to_dict() for a in self.alert_engine.all_alerts[:10]],
            "alerts_summary": self.alert_engine.get_active_alerts_summary()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n[EXPORT] Rapport sauvegardé dans {filename}")


# ==================== POINT D'ENTRÉE ====================

if __name__ == "__main__":
    print("\n" + "█"*60)
    print("█  SOLARWINDS NETWORK PERFORMANCE MONITOR - SIMULATION POO  █")
    print("█"*60)
    print("\nFilière: Réseaux, Système, Sécurité et Cybersécurité")
    print("Sujet: Modélisation POO d'un système réseau\n")
    
    # Créer et lancer le système
    npm_system = NPMSystem()
    npm_system.run(cycles=5)
    
    # Exporter le rapport
    npm_system.export_report("npm_report.json")
    
    print("\n" + "█"*60)
    print("█  SIMULATION TERMINÉE                                    █")
    print("█"*60 + "\n")
