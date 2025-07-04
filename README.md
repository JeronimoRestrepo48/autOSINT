# 🔍 OSINT Searcher - Plataforma Avanzada de Inteligencia de Fuentes Abiertas

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-red.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

Una plataforma completa de OSINT (Open Source Intelligence) desarrollada en Python con Flask, diseñada específicamente para investigaciones en Colombia. Incluye herramientas avanzadas de reconocimiento, enumeración y análisis de inteligencia de fuentes abiertas.

## 🌟 Características

### 🔐 Gestión de Usuarios
- ✅ Registro de usuarios con verificación por email
- ✅ Autenticación segura con sesiones
- ✅ Perfiles de usuario personalizables
- ✅ Roles y permisos (Analista, Admin, Viewer)

### � Capacidades OSINT
- ✅ **Análisis de Dominios**: DNS, WHOIS, subdominios, tecnologías
- ✅ **Análisis de IPs**: Geolocalización, puertos, servicios
- ✅ **Análisis de Emails**: Validación, breaches, redes sociales
- ✅ **Análisis de Usernames**: Búsqueda en múltiples plataformas
- ✅ **Análisis de Teléfonos**: Validación, país, operador
- ✅ **Análisis de Empresas**: Información corporativa, empleados
- ✅ **Análisis de Personas**: Redes sociales, información pública

### 📊 Reportes y Visualización
- ✅ Reportes automáticos en HTML, JSON, CSV, TXT
- ✅ Envío de reportes por email
- ✅ Visualizaciones interactivas
- ✅ Gráficos y estadísticas

### ⏰ Automatización
- ✅ Búsquedas programadas (diarias, semanales, mensuales)
- ✅ Notificaciones automáticas por email
- ✅ Ejecutión en segundo plano
- ✅ Historial completo de búsquedas

### 🌐 Interfaz Web
- ✅ Dashboard moderno y responsive
- ✅ Interfaz intuitiva y fácil de usar
- ✅ Panel de administración
- ✅ API REST completa
- **Reportes profesionales**: HTML, PDF, JSON con gráficos y recomendaciones
- **Interfaz web moderna** con dashboard interactivo
- **APIs integradas**: Shodan, VirusTotal, Censys, SecurityTrails, y más
- **Arquitectura modular** robusta con manejo de errores avanzado

### 🛠️ Herramientas CLI Integradas

Esta plataforma incluye **más de 100 herramientas OSINT CLI** de código abierto, organizadas en categorías:

#### 📋 Categorías Principales
- **🔍 Reconocimiento de Dominios** (15 herramientas): Subfinder, Amass, Assetfinder, Gobuster, etc.
- **🌐 Análisis de Red** (12 herramientas): Nmap, Masscan, Httpx, Nuclei, etc.
- **🕸️ Análisis Web** (18 herramientas): Gospider, Waybackurls, Dirsearch, etc.
- **📱 Redes Sociales** (10 herramientas): Sherlock, Maigret, Twint, etc.
- **📧 Análisis de Emails** (8 herramientas): TheHarvester, Holehe, Mosint, etc.
- **📊 Análisis de Metadatos** (6 herramientas): ExifTool, Metagoofil, etc.
- **🌍 Geolocalización** (7 herramientas): Geospy, Creepy, Photon, etc.
- **📞 Análisis de Números** (5 herramientas): PhoneInfoga, Phonelib, etc.
- **🤖 Automatización** (8 herramientas): Recon-ng, Spiderfoot, Maltego, etc.

#### 🚀 Instalación Automática
```bash
# Instalar todas las herramientas CLI
bash install_osint_tools.sh

# Instalar por categorías
bash install_osint_tools.sh --domains
bash install_osint_tools.sh --network
bash install_osint_tools.sh --social
```

Para documentación completa, consulta **[`docs/OSINT_CLI_TOOLS.md`](docs/OSINT_CLI_TOOLS.md)**

### 🛠️ Herramientas Incluidas

#### Reconocimiento y Enumeración
- **Enumeración de subdominios** (brute force, CT logs, motores de búsqueda)
- **Escaneo de puertos** con Nmap (opcional)
- **Análisis DNS completo** (todos los tipos de registros)
- **Análisis de certificados SSL/TLS**
- **Detección de tecnologías web**

#### Investigación Social
- **Búsqueda en 20+ plataformas** sociales
- **Análisis de GitHub** (perfiles, repositorios, emails)
- **Investigación de usernames** multiplataforma
- **Análisis de números telefónicos** (geolocalización, operador)

#### Análisis de Amenazas
- **Verificación de filtraciones** (HaveIBeenPwned)
- **Búsqueda en pastebins** (múltiples sitios)
- **Análisis de reputación** de dominios
- **Búsqueda en Certificate Transparency**

#### Investigación Corporativa
- **Análisis financiero** (empresas públicas)
- **Búsqueda de noticias** corporativas
- **Análisis de empleados** públicos
- **Mapeo de infraestructura**

#### Análisis Forense
- **Metadatos EXIF** de imágenes
- **Geolocalización** de IPs
- **Análisis histórico** (Wayback Machine)
- **Análisis de subdominios** históricos

#### Reportes Avanzados
- **Múltiples Formatos**: HTML, PDF, Excel, CSV
- **Gráficos Integrados**: Charts.js, Plotly para visualizaciones
- **Análisis Estadístico**: Tendencias, distribución geográfica
- **Envío Automático**: Reportes diarios por email

## 🔧 Últimas Correcciones y Mejoras

### ✅ Correcciones Implementadas (Enero 2025)
- **Corrección de errores de BeautifulSoup**: Manejo robusto de elementos HTML
- **Mejora en manejo de librerías opcionales**: nmap, paramiko con try/except
- **Corrección de API phonenumbers**: Importación correcta del módulo timezone
- **Mejora en parsing de certificados SSL**: Manejo seguro de estructuras de datos
- **Optimización de Wayback Machine**: Uso de CDX API para mayor estabilidad
- **Código más robusto**: Manejo de excepciones mejorado en todo el proyecto

### 🛡️ Características de Robustez
- **Manejo de dependencias opcionales**: El sistema funciona sin herramientas externas
- **Parsing HTML mejorado**: Múltiples métodos de extracción de datos
- **Timeouts configurables**: Evita bloqueos en requests
- **Logs detallados**: Debugging y monitoreo completo
- **Validación de datos**: Verificación de tipos y estructuras

### 🔒 Seguridad y APIs
- **Integración con APIs**: Shodan, VirusTotal, Censys
- **Escaneo de Vulnerabilidades**: Análisis básico de seguridad
- **Autenticación Web**: Login seguro para interfaz web
- **Logs Detallados**: Seguimiento completo de actividades

## 📦 Instalación

### Requisitos Previos
- Python 3.8 o superior
- Conexión a internet
- (Opcional) APIs keys para servicios especializados

### Instalación Automática

**Usando el script de instalación (Recomendado)**:
```bash
git clone <repository-url>
cd OSINTSearcher
chmod +x install.sh
./install.sh
```

### Instalación Manual

1. **Clonar el repositorio**:
```bash
git clone <repository-url>
cd OSINTSearcher
```

2. **Instalar dependencias**:
```bash
python MCP.py --install-deps

# Opción 2: Manual  
pip install -r requirements.txt
```

3. **Configurar el sistema**:

```bash
# Primera ejecución (genera configuración)
python MCP.py
```

4. **Editar configuración**:

```bash
nano osint_config.json
```

## ⚙️ Configuración

### Configuración Básica (`osint_config.json`)

```json
{
  "email_smtp_server": "smtp.gmail.com",
  "email_smtp_port": 587,
  "email_username": "tu_email@gmail.com",
  "email_password": "tu_contraseña_app",
  "email_recipients": ["destinatario@ejemplo.com"],
  
  "web_interface_enabled": true,
  "web_port": 5000,
  "web_host": "localhost",
  "web_auth_enabled": true,
  "web_username": "admin",
  
  "max_results_per_source": 20,
  "enable_deep_search": true,
  "search_engines": ["google", "bing", "duckduckgo", "yandex"]
}
```

### APIs Opcionales

```json
{
  "shodan_api_key": "tu_api_key_shodan",
  "virustotal_api_key": "tu_api_key_virustotal",
  "censys_api_id": "tu_censys_id",
  "censys_api_secret": "tu_censys_secret",
  "twitter_bearer_token": "tu_twitter_token"
}
```

## 🖥️ Uso

### Interfaz Web
```bash
# Iniciar con interfaz web
python MCP.py --web

# Solo interfaz web (sin consola)
python MCP.py --web-only
```

Acceder a: `http://localhost:5000`

### Modo Consola
```bash
# Iniciar en modo consola
python MCP.py

# Comandos disponibles:
# search <query> [tipo]     - Realizar búsqueda
# analyze <target>          - Análisis completo
# report [días] [formato]   - Generar reporte
# history [límite]          - Ver historial
# stats                     - Estadísticas
# web                       - Iniciar interfaz web
# quit                      - Salir
```

### Ejemplos de Uso

#### Búsqueda General
```bash
OSINT> search "example.com" general
```

#### Análisis de Dominio
```bash
OSINT> analyze example.com
OSINT> search "example.com" domain
```

#### Análisis de IP
```bash
OSINT> analyze 8.8.8.8
OSINT> search "8.8.8.8" ip
```

#### Búsqueda en Redes Sociales
```bash
OSINT> search "nombre_usuario" social
```

#### Generar Reportes
```bash
OSINT> report 7 html        # Últimos 7 días en HTML
OSINT> report 30 pdf        # Últimos 30 días en PDF
OSINT> report 1 xlsx        # Último día en Excel
```

## 📋 Tipos de Búsqueda

### 1. Búsqueda General (`general`)
- Múltiples motores de búsqueda
- Análisis de contenido
- Puntuación de relevancia
- Filtrado por idioma y fecha

### 2. Análisis de Dominio (`domain`)
- **WHOIS**: Registrador, fechas, contactos
- **DNS**: Registros A, AAAA, MX, TXT, NS
- **SSL**: Certificados, emisor, validez
- **Subdominios**: Enumeración automática
- **Tecnologías**: Stack tecnológico detectado

### 3. Análisis de IP (`ip`)
- **Geolocalización**: País, ciudad, ISP
- **ASN**: Número de sistema autónomo
- **Puertos**: Escaneo con Shodan (si disponible)
- **Servicios**: Detección de servicios activos
- **Reputación**: Análisis de seguridad

### 4. Redes Sociales (`social`)
- **Twitter**: Tweets, perfiles, menciones
- **Instagram**: Posts, hashtags
- **LinkedIn**: Perfiles profesionales
- **Facebook**: Páginas públicas

### 5. Noticias (`news`)
- **Google News**: Artículos recientes
- **Filtrado por fecha**: Últimos días/semanas
- **Múltiples idiomas**
- **Análisis de sentimiento**

### 6. Imágenes (`images`)
- **Búsqueda inversa**: Google Images
- **Metadatos**: EXIF, ubicación
- **Reconocimiento**: Objetos, texto

### 4. Google Dorking Avanzado (`dork`)

El sistema incluye un motor de Google Dorking automatizado que genera y ejecuta búsquedas especializadas para encontrar información específica sobre un objetivo.

#### Categorías de Dorking Disponibles

- **documentos**: Busca archivos PDF, DOC, XLS, PPT relacionados con el objetivo
- **bases_datos**: Identifica archivos de bases de datos expuestos
- **camaras**: Encuentra cámaras web y sistemas de vigilancia
- **archivos_sensibles**: Busca archivos de configuración, logs, backups
- **informacion_personal**: Localiza información personal y contactos
- **vulnerabilidades**: Identifica posibles fallos de seguridad
- **directorios**: Encuentra directorios listados y archivos expuestos
- **autenticacion**: Busca formularios y sistemas de login

#### Ejemplos de Uso del Google Dorking

##### Interfaz Web
1. Selecciona "Google Dorking" en el tipo de búsqueda
2. Ingresa el dominio objetivo (ej: "example.com")
3. Selecciona las categorías de interés
4. Ejecuta la búsqueda y revisa los resultados con niveles de riesgo

##### Modo Consola
```bash
OSINT> dork example.com documentos
OSINT> dork example.com bases_datos,archivos_sensibles
OSINT> dork example.com all  # Ejecuta todas las categorías
```

#### Interpretación de Resultados

Los resultados del dorking incluyen:
- **Nivel de Riesgo**: BAJO, MEDIO, ALTO, CRÍTICO
- **Tipo de Contenido**: Categoría del dork utilizado
- **URL Encontrada**: Enlace directo al contenido
- **Descripción**: Explicación del tipo de información encontrada
- **Recomendaciones**: Sugerencias para mitigar riesgos encontrados

#### Dorks Automáticos Generados

El sistema genera automáticamente dorks como:
- `site:example.com filetype:pdf`
- `site:example.com inurl:admin`
- `site:example.com "index of"`
- `site:example.com intext:"password"`
- `site:example.com filetype:sql`

## 📊 Dashboard y Reportes

### Dashboard Web
- **Estadísticas en Tiempo Real**: Gráficos interactivos
- **Búsqueda Rápida**: Interfaz intuitiva
- **Resultados Visuales**: Mapas, gráficos, tablas
- **Exportación Directa**: Múltiples formatos

### Tipos de Reportes

#### 1. HTML Interactivo
- Gráficos con Chart.js
- Mapas interactivos
- Diseño responsivo
- Exportable

#### 2. PDF Profesional
- Formato empresarial
- Tablas y gráficos
- Metadatos completos
- Listo para imprimir

#### 3. Excel Avanzado
- Múltiples hojas
- Gráficos integrados
- Datos estructurados
- Análisis estadístico

#### 4. CSV Simple
- Datos tabulares
- Compatible con análisis
- Importación fácil
- Formato universal

## 🔧 API y Integración

### Endpoints Web API

```bash
# Realizar búsqueda
POST /api/search
{
  "query": "ejemplo.com",
  "search_type": "domain",
  "max_results": 20
}

# Exportar resultados
GET /api/export/{search_id}/{format}

# Obtener estadísticas
GET /api/stats

# Historial
GET /api/history
```

### Integración con APIs Externas

#### Shodan
```json
{
  "shodan_api_key": "TU_API_KEY"
}
```
- Información de puertos abiertos
- Servicios detectados
- Vulnerabilidades conocidas

#### VirusTotal
```json
{
  "virustotal_api_key": "TU_API_KEY"
}
```
- Análisis de dominios/IPs maliciosos
- Reputación de URLs
- Detección de malware

#### Censys
```json
{
  "censys_api_id": "TU_ID",
  "censys_api_secret": "TU_SECRET"
}
```
- Escaneo de internet
- Certificados SSL
- Dispositivos expuestos

## 🛡️ Seguridad y Privacidad

### Buenas Prácticas
- **Rate Limiting**: Evita ser bloqueado por servicios
- **Rotación de User-Agents**: Múltiples identidades
- **Timeouts Configurables**: Evita bloqueos
- **Logs Detallados**: Auditoría completa

### Consideraciones Legales
- Respeta los términos de servicio
- Usa solo fuentes públicas
- No realices actividades ilegales
- Considera la privacidad de terceros

## 🔍 Casos de Uso

### 1. Investigación de Seguridad
- Análisis de infraestructura
- Detección de vulnerabilidades
- Monitoreo de amenazas
- Auditorías de seguridad

### 2. Investigación Corporativa
- Due diligence
- Análisis de competencia
- Investigación de marca
- Monitoreo de reputación

### 3. Investigación Legal
- Recopilación de evidencias
- Verificación de información
- Análisis de activos digitales
- Investigación de fraudes

### 4. Periodismo Investigativo
- Verificación de fuentes
- Investigación de personas
- Análisis de conexiones
- Fact-checking

## 🐛 Solución de Problemas

### Problemas Comunes

#### Error de Dependencias
```bash
# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

#### Problemas de Red
```bash
# Verificar conectividad
python -c "import requests; print(requests.get('https://google.com').status_code)"
```

#### Base de Datos Corrupta
```bash
# Resetear base de datos
rm osint_data.db
python MCP.py
```

#### Interfaz Web No Funciona
```bash
# Verificar puerto
netstat -tulpn | grep :5000

# Cambiar puerto en configuración
{
  "web_port": 8080
}
```

## 📈 Roadmap

### Versión Actual (1.0)
- ✅ Búsquedas básicas y avanzadas
- ✅ Interfaz web moderna
- ✅ Reportes múltiples formatos
- ✅ Integración APIs principales

### Próximas Versiones

#### v1.1
- 🔄 Búsqueda en tiempo real
- 🔄 Alertas automáticas
- 🔄 API REST completa
- 🔄 Plugins personalizables

#### v1.2
- 🔄 Machine Learning para relevancia
- 🔄 Análisis de sentimientos avanzado
- 🔄 Búsqueda en Dark Web
- 🔄 Reconocimiento facial

#### v1.3
- 🔄 Distribución en Docker
- 🔄 Escalabilidad horizontal
- 🔄 Base de datos avanzada
- 🔄 Integración con SIEM

## 🤝 Contribución

### Cómo Contribuir
1. Fork del repositorio
2. Crear rama feature
3. Realizar cambios
4. Enviar pull request

### Áreas de Mejora
- Nuevos motores de búsqueda
- APIs adicionales
- Mejoras de UI/UX
- Optimización de rendimiento
- Documentación expandida

## � Documentación Completa

### 📋 Guías Principales
- **[`docs/OSINT_CLI_TOOLS.md`](docs/OSINT_CLI_TOOLS.md)**: Guía completa de herramientas CLI OSINT
- **[`docs/GUIA_USUARIO.md`](docs/GUIA_USUARIO.md)**: Guía detallada del usuario
- **[`docs/ADVANCED_FEATURES.md`](docs/ADVANCED_FEATURES.md)**: Funcionalidades avanzadas
- **[`docs/EXAMPLES.md`](docs/EXAMPLES.md)**: Ejemplos prácticos de uso
- **[`docs/CLI_TOOLS_INTEGRATION.md`](docs/CLI_TOOLS_INTEGRATION.md)**: Integración de herramientas CLI

### 🎯 Contenido Destacado
- **100+ herramientas CLI** documentadas con ejemplos
- **Flujos de trabajo** automatizados
- **Scripts de instalación** para todas las herramientas
- **Configuración de APIs** y claves de acceso
- **Casos de uso reales** con ejemplos paso a paso

### 📖 Documentación Técnica
- **Instalación** y configuración
- **Uso de APIs** especializadas
- **Personalización** de herramientas
- **Troubleshooting** común
- **Mejores prácticas** de seguridad

## �📄 Licencia

Este proyecto está bajo licencia MIT. Ver archivo `LICENSE` para más detalles.

## 📞 Soporte

### Documentación
- **Wiki del proyecto**: Documentación completa actualizada
- **Ejemplos de código**: Casos de uso reales
- **Videos tutoriales**: Próximamente
- **FAQ detallado**: En la wiki del proyecto

### Comunidad
- **GitHub Issues**: Reportar bugs y solicitar features
- **Discord/Telegram**: Próximamente
- **Stack Overflow**: Tag `osint-searcher`
- **Reddit**: r/OSINT

---

**⚠️ Disclaimer**: Esta herramienta está diseñada para uso ético y legal en investigaciones de fuentes abiertas. Los usuarios son responsables de cumplir con todas las leyes y regulaciones aplicables.

**🔒 Privacidad**: Respeta la privacidad de las personas y organizaciones. Usa esta herramienta de manera responsable y ética.
