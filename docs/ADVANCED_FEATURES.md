# OSINT SearchEngine - Herramientas Avanzadas

## 🔍 Nuevas Funcionalidades OSINT

### 1. **Enumeración de Subdominios**
- **Técnicas múltiples**: Brute force, Certificate Transparency, búsqueda en motores
- **Wordlist integrada**: 50+ subdominios comunes
- **Verificación activa**: Comprueba HTTP/HTTPS y extrae información
- **Detección de tecnologías**: Identifica servidores web, CMS, frameworks

### 2. **Análisis de Red**
- **Escaneo con Nmap**: Puertos, servicios, OS fingerprinting
- **Detección de vulnerabilidades**: Scripts NSE integrados
- **Análisis de redes**: Descubrimiento de hosts en redes
- **Información detallada**: Versiones, productos, configuraciones

### 3. **Investigación de Redes Sociales**
- **20+ plataformas**: GitHub, Twitter, Instagram, LinkedIn, etc.
- **Verificación inteligente**: Evita falsos positivos
- **Extracción de datos**: Nombres reales, biografías, ubicaciones
- **Análisis paralelo**: Verificación simultánea de múltiples plataformas

### 4. **Análisis de Números Telefónicos**
- **Geolocalización**: País, región, ciudad
- **Información del operador**: Compañía telefónica
- **Zona horaria**: Información temporal
- **Validación**: Verificación de formato y validez

### 5. **Búsqueda en Archivos Web**
- **Wayback Machine**: Historial de sitios web
- **Snapshots múltiples**: Hasta 50 capturas históricas
- **Información temporal**: Fechas de primera y última captura
- **URLs de archivo**: Enlaces directos a capturas

### 6. **Detección de Tecnologías**
- **Análisis de headers**: Servidores web, CDNs
- **Inspección de contenido**: CMS, frameworks JavaScript
- **Metadatos**: Generadores, herramientas utilizadas
- **Integración BuiltWith**: Detección avanzada cuando está disponible

### 7. **Investigación Corporativa**
- **Datos financieros**: Información bursátil (empresas públicas)
- **Búsqueda de noticias**: Últimas noticias corporativas
- **Presencia web**: Dominios relacionados
- **Empleados**: Información disponible públicamente

### 8. **Verificación de Filtraciones**
- **Base de datos de brechas**: Verificación de emails comprometidos
- **Análisis de reputación**: Dominios maliciosos
- **Fuentes múltiples**: HaveIBeenPwned, servicios adicionales
- **Historial de incidentes**: Fechas y tipos de datos comprometidos

### 9. **Búsqueda en Pastebins**
- **Múltiples sitios**: Pastebin, Paste.ee, JustPaste.it, etc.
- **Búsqueda inteligente**: Google dorking para pastebins
- **Detección de contenido**: Emails, contraseñas, datos sensibles
- **Análisis de resultados**: Clasificación por relevancia

### 10. **Investigación de GitHub**
- **Perfiles completos**: Información personal y profesional
- **Repositorios**: Análisis de código público
- **Extracción de emails**: Emails de commits públicos
- **Organizaciones**: Membresías en organizaciones
- **Búsqueda de código**: Buscar strings específicos en código

### 11. **Análisis de Certificados SSL**
- **Información completa**: Emisor, validez, Subject Alt Names
- **Certificate Transparency**: Búsqueda en logs CT
- **Análisis de cadena**: Verificación de certificados
- **Evaluación de seguridad**: Fortaleza y configuración

### 12. **Análisis DNS Avanzado**
- **Registros completos**: A, AAAA, MX, NS, TXT, CNAME, SOA, PTR
- **Análisis MX**: Detección de proveedores de email
- **Análisis NS**: Proveedores de DNS
- **Análisis TXT**: SPF, DMARC, DKIM, verificaciones

### 13. **Análisis de Metadatos EXIF**
- **Geolocalización**: Coordenadas GPS en imágenes
- **Información del dispositivo**: Marca, modelo, software
- **Timestamps**: Fechas de creación y modificación
- **Análisis desde URLs**: Procesamiento de imágenes remotas

## 🛠️ Herramientas CLI Integradas

### Instalación Automática

La plataforma incluye un script de instalación automática para más de 50 herramientas OSINT CLI:

```bash
# Instalar todas las herramientas recomendadas
bash install_osint_tools.sh

# Instalar herramientas específicas por categoría
bash install_osint_tools.sh --domains
bash install_osint_tools.sh --network
bash install_osint_tools.sh --social
```

### Categorías de Herramientas

#### 🔍 Reconocimiento de Dominios y Subdominios
- **Subfinder**: Enumeración de subdominios
- **Amass**: Mapeo de superficie de ataque
- **Assetfinder**: Búsqueda de activos
- **Gobuster**: Fuerza bruta de subdominios
- **Sublist3r**: Enumeración de subdominios con múltiples fuentes
- **Knockpy**: Enumeración de subdominios con diccionario
- **Findomain**: Búsqueda rápida de subdominios

#### 🌐 Análisis de Red y Puertos
- **Nmap**: Escaneo de puertos y servicios
- **Masscan**: Escaneo rápido de gran escala
- **Httpx**: Sondeo HTTP/HTTPS
- **Nuclei**: Escáner de vulnerabilidades
- **Shodan CLI**: Búsqueda de dispositivos conectados
- **Rustscan**: Escaneo de puertos ultrarrápido

#### 📊 Análisis de Datos y Metadatos
- **ExifTool**: Extracción de metadatos
- **Whois**: Información de dominio
- **Dig**: Consultas DNS avanzadas
- **Waybackurls**: URLs del archivo web
- **Gau**: Obtención de URLs
- **Unfurl**: Análisis de URLs

#### 🔎 Búsqueda Especializada
- **TheHarvester**: Recolección de emails e información
- **Recon-ng**: Framework de reconocimiento
- **Maltego**: Análisis de enlaces (comunidad)
- **Spiderfoot**: Automatización OSINT
- **Sherlock**: Búsqueda de usernames
- **Maigret**: Búsqueda de perfiles sociales

#### 🕸️ Análisis Web y Crawling
- **Gospider**: Web crawler
- **Hakrawler**: Web crawler rápido
- **Katana**: Crawling y análisis web
- **Dirsearch**: Búsqueda de directorios
- **FFUF**: Fuzzing web rápido

#### 📱 Redes Sociales y Personas
- **Sherlock**: Búsqueda de usernames
- **Maigret**: Búsqueda de perfiles sociales
- **Twint**: Scraping de Twitter
- **Instaloader**: Descarga de Instagram
- **Socialscan**: Verificación de usernames

#### 🔐 Análisis de Seguridad
- **Nuclei**: Escáner de vulnerabilidades
- **Naabu**: Enumeración de puertos
- **Httpx**: Sondeo HTTP
- **Subjack**: Detección de subdomain takeover
- **Aquatone**: Reconocimiento visual

#### 🌍 Geolocalización e Imágenes
- **ExifTool**: Metadatos EXIF
- **Geospy**: Geolocalización de imágenes
- **Creepy**: Geolocalización de redes sociales
- **OSINT-SPY**: Análisis de metadatos

#### 📞 Análisis de Números y Contactos
- **PhoneInfoga**: Análisis de números telefónicos
- **Infoga**: Recolección de información
- **Mosint**: Análisis de emails
- **Holehe**: Verificación de cuentas por email

#### 🤖 Automatización y Frameworks
- **Recon-ng**: Framework de reconocimiento
- **Spiderfoot**: Automatización OSINT
- **Maltego**: Análisis de enlaces
- **OSINT Framework**: Colección de herramientas
- **Sn0int**: Framework de inteligencia

Para documentación completa, consulta `docs/OSINT_CLI_TOOLS.md`

## 🛠️ Herramientas de Reconocimiento

### Herramientas de Reconocimiento

**Instalación incluida en el script:**
```bash
# Todas las herramientas se instalan automáticamente
bash install_osint_tools.sh
```

## 📊 Tipos de Búsqueda Soportados

### 1. **Dominio** (example.com)
- Enumeración de subdominios
- Análisis DNS completo
- Certificados SSL/TLS
- Tecnologías web utilizadas
- Historial en Wayback Machine

### 2. **Dirección IP** (192.168.1.1)
- Escaneo de puertos
- Geolocalización
- Información del ISP
- Servicios ejecutándose
- Vulnerabilidades conocidas

### 3. **Email** (user@example.com)
- Verificación de filtraciones
- Análisis del dominio
- Búsqueda en pastebins
- Perfiles sociales relacionados
- Búsqueda en GitHub

### 4. **Username** (username123)
- Búsqueda en 20+ plataformas
- Perfiles de GitHub
- Información personal disponible
- Actividad pública
- Conexiones y seguidores

### 5. **Número de Teléfono** (+1234567890)
- Geolocalización
- Operador/Carrier
- Zona horaria
- Validación de formato
- Tipo de línea

### 6. **Empresa** (Nombre de Empresa)
- Información financiera
- Noticias recientes
- Presencia web
- Empleados públicos
- Tecnologías utilizadas

## 🔧 Configuración Avanzada

### Archivo de Configuración (osint_config_advanced.json)
```json
{
  "api_keys": {
    "shodan_api_key": "tu_api_key",
    "virustotal_api_key": "tu_api_key",
    "github_token": "tu_token"
  },
  "osint_modules": {
    "subdomain_enumeration": {
      "enabled": true,
      "timeout": 30,
      "max_threads": 20
    },
    "social_media_search": {
      "enabled": true,
      "platforms": ["github", "twitter", "instagram"]
    }
  }
}
```

### Variables de Entorno
- `OSINT_HOME`: Directorio base de la aplicación
- `API_KEYS_FILE`: Archivo de claves API
- `WORDLIST_DIR`: Directorio de wordlists
- `OUTPUT_DIR`: Directorio de salida de reportes

## 📈 Formatos de Reporte

### 1. **HTML** (Recomendado)
- Formato visual atractivo
- Gráficos y tablas interactivas
- Navegación por secciones
- Resumen ejecutivo
- Recomendaciones de seguridad

### 2. **JSON** (Programático)
- Formato estructurado
- Fácil procesamiento
- Integración con otras herramientas
- Datos completos sin formato

### 3. **PDF** (Profesional)
- Formato imprimible
- Branding corporativo
- Tablas y gráficos
- Resumen ejecutivo

## 🚀 Uso Rápido

### Instalación
```bash
# Clonar repositorio
git clone <repo-url>
cd OSINTSearcher

# Ejecutar instalación
chmod +x install_advanced.sh
./install_advanced.sh

# Activar entorno
source activate.sh
```

### Búsquedas Básicas
```bash
# Búsqueda de dominio
python osint_master.py example.com

# Búsqueda de email
python osint_master.py user@example.com

# Búsqueda de username
python osint_master.py username123

# Búsqueda de IP
python osint_master.py 192.168.1.1
```

### Búsquedas Avanzadas
```bash
# Especificar tipo de búsqueda
python osint_master.py --type domain example.com

# Formato de reporte específico
python osint_master.py --format pdf example.com

# Configuración personalizada
python osint_master.py --config mi_config.json example.com
```

## 🔒 Consideraciones de Seguridad

### Uso Ético
- **Solo para propósitos legítimos**: Investigación de seguridad autorizada
- **Respeto a términos de servicio**: No violar ToS de plataformas
- **Límites de velocidad**: Respetar rate limits de APIs
- **Privacidad**: No almacenar datos personales innecesariamente

### Protección de Datos
- **Encriptación**: Datos sensibles encriptados
- **Logs seguros**: Registro de actividades sin datos personales
- **Configuración segura**: Claves API en archivos separados
- **Limpieza automática**: Eliminación de datos temporales

## 📚 APIs y Servicios Recomendados

### Gratuitos
- **HaveIBeenPwned**: Verificación de filtraciones
- **Certificate Transparency**: Búsqueda de certificados
- **Wayback Machine**: Archivo web histórico
- **GitHub API**: Búsqueda de código público
- **Google Public DNS**: Resolución DNS

### De Pago (Recomendados)
- **Shodan**: $59/mes - Dispositivos conectados
- **VirusTotal**: $180/mes - Análisis de malware
- **Censys**: $99/mes - Análisis de certificados
- **SecurityTrails**: $50/mes - Inteligencia DNS
- **BinaryEdge**: $100/mes - Escaneo global

## 🎯 Casos de Uso

### 1. **Auditoría de Seguridad**
- Descubrimiento de activos expuestos
- Identificación de vulnerabilidades
- Análisis de superficie de ataque
- Verificación de configuraciones

### 2. **Investigación de Amenazas**
- Análisis de dominios maliciosos
- Rastreo de atacantes
- Inteligencia de amenazas
- Análisis de campañas

### 3. **Investigación Digital**
- Búsqueda de personas
- Análisis de identidades digitales
- Verificación de información
- Investigación de fraudes

### 4. **Monitoreo de Marca**
- Detección de phishing
- Uso no autorizado de marca
- Monitoreo de redes sociales
- Análisis de reputación

## 🔄 Actualizaciones y Mantenimiento

### Actualización de Herramientas
```bash
# Actualizar nuclei templates
nuclei -update-templates

# Actualizar herramientas Go
go install -u github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

# Actualizar wordlists
git -C wordlists/SecLists pull
```

### Mantenimiento de Base de Datos
```bash
# Limpiar cache
rm -rf cache/*

# Limpiar logs antiguos
find logs/ -name "*.log" -mtime +30 -delete

# Limpiar reportes antiguos
find reports/ -name "*.html" -mtime +90 -delete
```

## 🆘 Solución de Problemas

### Problemas Comunes

1. **Error de API Key**
   - Verificar claves en `api_keys.json`
   - Comprobar límites de rate
   - Validar permisos de API

2. **Herramientas no encontradas**
   - Verificar instalación con `which <tool>`
   - Añadir al PATH si es necesario
   - Reinstalar herramientas

3. **Permisos insuficientes**
   - Usar `sudo` para instalación de sistema
   - Verificar permisos de archivos
   - Comprobar configuración de firewall

### Logs de Debugging
```bash
# Ver logs en tiempo real
tail -f logs/osint_advanced.log

# Buscar errores específicos
grep "ERROR" logs/osint_advanced.log

# Análisis de rendimiento
grep "execution_time" logs/osint_advanced.log
```

## 📞 Soporte

### Documentación
- **README.md**: Guía básica
- **EXAMPLES.md**: Ejemplos de uso
- **GUIA_USUARIO.md**: Guía detallada del usuario

### Contribución
- Reportar bugs en GitHub Issues
- Proponer nuevas funcionalidades
- Contribuir con código
- Mejorar documentación

### Contacto
- **Email**: soporte@osint-searcher.com
- **GitHub**: [Repositorio del proyecto]
- **Discord**: [Canal de soporte]

---

*Desarrollado con ❤️ para la comunidad OSINT*
