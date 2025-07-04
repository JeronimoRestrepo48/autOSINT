# 🛠️ Integración de Herramientas CLI OSINT

## 📋 Resumen

Este documento describe la integración de herramientas CLI OSINT de código abierto en la plataforma OSINTSearcher, proporcionando un ecosistema completo para investigación de inteligencia de fuentes abiertas.

## 🎯 Objetivo

Proporcionar una plataforma unificada que combine:
- **Interfaz Web Intuitiva**: Para usuarios que prefieren interfaces gráficas
- **Herramientas CLI Especializadas**: Para investigadores técnicos
- **Automatización**: Para flujos de trabajo repetitivos
- **Reportes Profesionales**: Para presentar resultados

## 🔧 Herramientas Integradas

### Instalación Automática

```bash
# Instalar todas las herramientas
bash install_osint_tools.sh

# Verificar instalación
python -c "from osint_cli_tools import verify_installation; verify_installation()"
```

### Categorías de Herramientas

#### 1. **Reconocimiento de Dominios** (15 herramientas)
- **Subfinder**: Enumeración de subdominios
- **Amass**: Mapeo de superficie de ataque
- **Assetfinder**: Búsqueda de activos
- **Gobuster**: Fuerza bruta de subdominios
- **Sublist3r**: Enumeración con múltiples fuentes
- **Knockpy**: Enumeración con diccionario
- **Findomain**: Búsqueda rápida
- **Chaos**: Base de datos de subdominios
- **Puredns**: Validación DNS rápida
- **Shuffledns**: Resolución DNS masiva
- **Altdns**: Generación de subdominios
- **Dnsrecon**: Reconocimiento DNS
- **Fierce**: Enumeración de dominios
- **Dnsgen**: Generación de subdominios
- **Massdns**: Resolución DNS masiva

#### 2. **Análisis de Red** (12 herramientas)
- **Nmap**: Escaneo de puertos y servicios
- **Masscan**: Escaneo rápido de gran escala
- **Rustscan**: Escaneo ultrarrápido
- **Naabu**: Enumeración de puertos
- **Zmap**: Escaneo de internet
- **Unicornscan**: Escaneo de puertos
- **Prips**: Generación de rangos IP
- **Fping**: Ping masivo
- **Hping3**: Ping personalizado
- **Traceroute**: Trazado de rutas
- **Mtr**: Diagnóstico de red
- **Netdiscover**: Descubrimiento de hosts

#### 3. **Análisis Web** (18 herramientas)
- **Httpx**: Sondeo HTTP/HTTPS
- **Nuclei**: Escáner de vulnerabilidades
- **Gospider**: Web crawler
- **Hakrawler**: Web crawler rápido
- **Katana**: Crawling y análisis web
- **Waybackurls**: URLs del archivo web
- **Gau**: Obtención de URLs
- **Unfurl**: Análisis de URLs
- **Dirsearch**: Búsqueda de directorios
- **FFUF**: Fuzzing web rápido
- **Wfuzz**: Fuzzing web
- **Dirb**: Búsqueda de directorios
- **Aquatone**: Reconocimiento visual
- **Httprobe**: Verificación HTTP
- **Meg**: Búsqueda de rutas
- **Feroxbuster**: Búsqueda de contenido
- **Gobuster**: Fuerza bruta web
- **Whatweb**: Identificación de tecnologías

#### 4. **Redes Sociales** (10 herramientas)
- **Sherlock**: Búsqueda de usernames
- **Maigret**: Búsqueda de perfiles sociales
- **Twint**: Scraping de Twitter
- **Instaloader**: Descarga de Instagram
- **Socialscan**: Verificación de usernames
- **Whatsapp-scanner**: Análisis de WhatsApp
- **Holehe**: Verificación de cuentas por email
- **Nexfil**: Búsqueda de perfiles
- **Blackbird**: Búsqueda de usuarios
- **Userrecon**: Reconocimiento de usuarios

#### 5. **Análisis de Emails** (8 herramientas)
- **TheHarvester**: Recolección de emails
- **Holehe**: Verificación de cuentas
- **Mosint**: Análisis de emails
- **Infoga**: Recolección de información
- **Buster**: Verificación de emails
- **Crosslinked**: Enumeración de LinkedIn
- **EmailHarvester**: Recolección de emails
- **H8mail**: Búsqueda de filtraciones

#### 6. **Análisis de Metadatos** (6 herramientas)
- **ExifTool**: Extracción de metadatos
- **Metagoofil**: Extracción de metadatos
- **FOCA**: Análisis de metadatos
- **Exifread**: Lectura de EXIF
- **Piexif**: Manipulación de EXIF
- **Pillow**: Procesamiento de imágenes

#### 7. **Geolocalización** (7 herramientas)
- **Geospy**: Geolocalización de imágenes
- **Creepy**: Geolocalización de redes sociales
- **Photon**: Análisis de geolocalización
- **Osintgram**: Análisis de Instagram
- **Tinfoleak**: Análisis de Twitter
- **Geolocate**: Geolocalización general
- **Exifprobe**: Análisis de metadatos GPS

#### 8. **Análisis de Números** (5 herramientas)
- **PhoneInfoga**: Análisis de números telefónicos
- **Phonelib**: Validación de números
- **Numverify**: Verificación de números
- **Phonenumbers**: Análisis de números
- **Truecaller**: Identificación de llamadas

#### 9. **Frameworks y Automatización** (8 herramientas)
- **Recon-ng**: Framework de reconocimiento
- **Spiderfoot**: Automatización OSINT
- **Maltego**: Análisis de enlaces
- **Sn0int**: Framework de inteligencia
- **Raccoon**: Escáner de reconocimiento
- **Reconspider**: Automatización
- **Osintgram**: Framework de Instagram
- **Photon**: Crawler automatizado

## 🚀 Integración con la Plataforma

### Uso desde la Interfaz Web

La plataforma web automaticamente utiliza las herramientas CLI cuando están disponibles:

```python
# Ejemplo de integración automática
def analyze_domain(domain):
    results = {}
    
    # Usar Subfinder si está disponible
    if is_tool_available('subfinder'):
        results['subdomains'] = run_subfinder(domain)
    
    # Usar Amass si está disponible
    if is_tool_available('amass'):
        results['assets'] = run_amass(domain)
    
    # Usar Httpx para verificar
    if is_tool_available('httpx'):
        results['active_urls'] = run_httpx(results['subdomains'])
    
    return results
```

### Uso desde Línea de Comandos

```bash
# Análisis completo automatizado
python osint_master.py example.com --use-cli-tools

# Análisis específico
python osint_master.py example.com --tools subfinder,amass,httpx

# Análisis silencioso
python osint_master.py example.com --quiet --output results.json
```

## 📊 Flujos de Trabajo Automatizados

### 1. **Reconocimiento de Dominio Completo**

```bash
#!/bin/bash
DOMAIN=$1

# Fase 1: Enumeración de subdominios
subfinder -d $DOMAIN -o subdomains.txt
amass enum -d $DOMAIN -o amass_subdomains.txt

# Fase 2: Verificación de subdominios activos
httpx -l subdomains.txt -o active_subdomains.txt

# Fase 3: Escaneo de puertos
nmap -iL active_subdomains.txt -oN port_scan.txt

# Fase 4: Análisis de vulnerabilidades
nuclei -l active_subdomains.txt -o vulnerabilities.txt

# Fase 5: Análisis web
gospider -S active_subdomains.txt -o crawl_results/
```

### 2. **Investigación de Persona**

```bash
#!/bin/bash
USERNAME=$1

# Búsqueda en redes sociales
sherlock $USERNAME --csv --output social_profiles.csv

# Verificación de emails
holehe $USERNAME@gmail.com --output email_accounts.txt

# Análisis de perfiles
maigret $USERNAME --output detailed_profiles/
```

### 3. **Análisis de Seguridad**

```bash
#!/bin/bash
TARGET=$1

# Reconocimiento pasivo
amass enum -passive -d $TARGET -o passive_recon.txt

# Escaneo de puertos
nmap -sS -sV -O $TARGET -oN detailed_scan.txt

# Búsqueda de vulnerabilidades
nuclei -u $TARGET -severity high,critical -o critical_vulns.txt

# Análisis web
whatweb $TARGET -a 3 --output-file web_analysis.txt
```

## 🔧 Configuración y Personalización

### Archivo de Configuración

```json
{
  "cli_tools": {
    "enabled": true,
    "auto_install": true,
    "update_interval": "weekly",
    "tools": {
      "subfinder": {
        "enabled": true,
        "config": "/path/to/subfinder/config.yaml",
        "timeout": 300
      },
      "amass": {
        "enabled": true,
        "config": "/path/to/amass/config.ini",
        "timeout": 600
      },
      "nuclei": {
        "enabled": true,
        "templates": "/path/to/nuclei-templates",
        "update_templates": true
      }
    }
  }
}
```

### Variables de Entorno

```bash
# Configuración de herramientas
export OSINT_TOOLS_PATH="/opt/osint-tools"
export NUCLEI_TEMPLATES_PATH="/opt/nuclei-templates"
export WORDLISTS_PATH="/opt/wordlists"

# Configuración de APIs
export SHODAN_API_KEY="your_api_key"
export VIRUSTOTAL_API_KEY="your_api_key"
export GITHUB_TOKEN="your_token"
```

## 📈 Métricas y Monitoreo

### Estadísticas de Uso

```python
# Generar estadísticas de uso
python -c "
from osint_cli_tools import get_usage_stats
stats = get_usage_stats()
print(f'Herramientas instaladas: {stats.installed_tools}')
print(f'Herramientas activas: {stats.active_tools}')
print(f'Análisis realizados: {stats.total_analyses}')
print(f'Tiempo total de análisis: {stats.total_time}')
"
```

### Monitoreo de Rendimiento

```bash
# Verificar estado de herramientas
python -c "
from osint_cli_tools import health_check
health = health_check()
for tool, status in health.items():
    print(f'{tool}: {status}')
"
```

## 🛡️ Consideraciones de Seguridad

### Instalación Segura

```bash
# Verificar checksums antes de instalar
bash install_osint_tools.sh --verify-checksums

# Instalar solo herramientas confiables
bash install_osint_tools.sh --trusted-only

# Instalar en entorno aislado
bash install_osint_tools.sh --sandbox
```

### Uso Responsable

1. **Respeto a Rate Limits**: Configurar delays apropiados
2. **Términos de Servicio**: Cumplir con ToS de servicios
3. **Privacidad**: No violar privacidad de individuos
4. **Legalidad**: Usar solo para propósitos legítimos
5. **Ética**: Seguir principios éticos de OSINT

## 🔄 Mantenimiento y Actualizaciones

### Actualización Automática

```bash
# Actualizar todas las herramientas
bash update_osint_tools.sh

# Actualizar templates de Nuclei
nuclei -update-templates

# Actualizar wordlists
git -C /opt/wordlists/SecLists pull
```

### Limpieza de Sistema

```bash
# Limpiar archivos temporales
bash cleanup_osint_tools.sh

# Verificar integridad
bash verify_osint_tools.sh

# Reparar instalaciones
bash repair_osint_tools.sh
```

## 📚 Recursos Adicionales

### Documentación

- **[OSINT_CLI_TOOLS.md](./OSINT_CLI_TOOLS.md)**: Guía completa de herramientas
- **[ADVANCED_FEATURES.md](./ADVANCED_FEATURES.md)**: Funcionalidades avanzadas
- **[EXAMPLES.md](./EXAMPLES.md)**: Ejemplos prácticos
- **[GUIA_USUARIO.md](./GUIA_USUARIO.md)**: Guía del usuario

### Comunidad

- **GitHub**: [Repositorio del proyecto]
- **Discord**: [Canal de la comunidad]
- **Twitter**: [@OSINTSearcher]
- **Blog**: [blog.osintsearcher.com]

## 🎯 Próximos Pasos

### Desarrollos Futuros

1. **Integración con Kubernetes**: Despliegue escalable
2. **API REST**: Acceso programático a herramientas
3. **Machine Learning**: Análisis predictivo
4. **Blockchain**: Verificación de integridad
5. **Mobile App**: Aplicación móvil

### Contribuciones

```bash
# Contribuir al proyecto
git clone https://github.com/your-repo/osint-searcher.git
cd osint-searcher
git checkout -b feature/nueva-herramienta
# Realizar cambios
git commit -m "Agregar nueva herramienta OSINT"
git push origin feature/nueva-herramienta
```

---

**Desarrollado con ❤️ para la comunidad OSINT**

*Última actualización: Julio 2025*
