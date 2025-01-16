# InfluxDB Datenkollektor

Dieses Skript sammelt Daten von verschiedenen Geräten (Temperatursensoren, Leistungsmessern und Luftqualitätsmonitoren) und speichert sie in einer InfluxDB-Datenbank.

## Funktionen

- Abruf von Temperatur-, Leistungs- und Luftqualitätsdaten über HTTP-Endpunkte.
- Parsen und Validieren der empfangenen JSON-Daten.
- Speichern der Daten in einem InfluxDB-Bucket für weitere Visualisierung und Analyse.

## Anforderungen

- **Python** 3.7+
- Installierte Python-Bibliotheken:
  - `requests`
  - `influxdb-client`
- Eine laufende **InfluxDB**-Instanz.

## Konfiguration

Das Skript benötigt eine `config.json`-Datei für die Konfiguration. Ein Beispiel:

```json
{
  "temperature_ip_addresses": ["192.168.1.10", "192.168.1.11"],
  "power_ip_addresses": ["192.168.1.20", "192.168.1.21"],
  "air_quality_ip_addresses": ["192.168.1.30", "192.168.1.31"],
  "influxdb_token": "your-influxdb-token"
}
```

### Konfigurationsfelder

- **temperature_ip_addresses**: Liste der IP-Adressen von Temperatursensoren.
- **power_ip_addresses**: Liste der IP-Adressen von Leistungsmessgeräten.
- **air_quality_ip_addresses**: Liste der IP-Adressen von Luftqualitätsmonitoren.
- **influxdb_token**: API-Token für die Authentifizierung bei InfluxDB.

## Nutzung

1. Stelle sicher, dass die Abhängigkeiten installiert sind:
   ```bash
   pip install requests influxdb-client
   ```
2. Erstelle die `config.json`-Datei basierend auf der oben gezeigten Vorlage.
3. Starte das Skript:
   ```bash
   python script_name.py
   ```

## Ablauf

1. Das Skript lädt die Konfiguration aus `config.json`.
2. Es ruft Daten von den in der Konfiguration angegebenen Geräten ab.
3. Die Daten werden in einem definierten InfluxDB-Bucket gespeichert.
4. Fehler werden in der Konsole angezeigt.

## Beispielausgabe

```plaintext
Current temperature at 192.168.1.10: 22.5°C
Temperature data from 192.168.1.10 written to InfluxDB.
Current power at 192.168.1.20: 150W
Power data from 192.168.1.20 written to InfluxDB.
Current air data at 192.168.1.30: {'score': 95, 'co2': 450, ...}
Air quality data from 192.168.1.30 written to InfluxDB.
```

## Fehlerbehandlung

- **Fehler beim Abrufen der Daten**:  
  Wenn keine Verbindung hergestellt werden kann oder die Antwort nicht im erwarteten Format ist, wird eine Fehlermeldung angezeigt.
- **Fehler beim Schreiben in die InfluxDB**:  
  Bei Problemen mit der Datenbankverbindung oder falschen Daten wird eine entsprechende Fehlermeldung ausgegeben.

