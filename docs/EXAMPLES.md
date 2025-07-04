# 🔍 OSINT Searcher - Ejemplos de Uso

Este documento contiene ejemplos prácticos de cómo usar OSINT Searcher para diferentes tipos de investigaciones.

## 🚀 Inicio Rápido

### Instalación de Herramientas CLI

```bash
# Instalar todas las herramientas OSINT CLI
bash install_osint_tools.sh

# Verificar instalación
python -c "import osint_cli_tools; osint_cli_tools.verify_installation()"
```

### Opción 1: Script Automático

```bash
./start.sh
```

### Opción 2: Manual

```bash
# Instalar dependencias
pip install -r requirements.txt

# Iniciar interfaz web
python MCP.py --web

# O modo consola
python MCP.py
```

### Opción 3: Uso de Herramientas CLI Directamente

```bash
# Enumeración de subdominios
subfinder -d example.com

# Escaneo de puertos
nmap -sS -sV example.com

# Análisis web
httpx -l domains.txt

# Búsqueda de vulnerabilidades
nuclei -u example.com
```

## � Ejemplos de Herramientas CLI

### Reconocimiento de Dominios

#### Subfinder - Enumeración de Subdominios
```bash
# Enumeración básica
subfinder -d example.com

# Con múltiples dominios
subfinder -dL domains.txt -o subdomains.txt

# Con resolución DNS
subfinder -d example.com -r -o active_subdomains.txt
```

#### Amass - Mapeo de Superficie de Ataque
```bash
# Enumeración pasiva
amass enum -passive -d example.com

# Enumeración activa
amass enum -active -d example.com -o amass_results.txt

# Con configuración personalizada
amass enum -config amass_config.yaml -d example.com
```

### Análisis de Red

#### Nmap - Escaneo de Puertos
```bash
# Escaneo básico
nmap example.com

# Escaneo de servicios
nmap -sS -sV -O example.com

# Escaneo de vulnerabilidades
nmap --script vuln example.com

# Escaneo de rango
nmap -sS 192.168.1.0/24
```

#### Httpx - Sondeo HTTP/HTTPS
```bash
# Verificar URLs activas
httpx -l urls.txt

# Con headers personalizados
httpx -l urls.txt -H "User-Agent: CustomAgent"

# Detectar tecnologías
httpx -l urls.txt -tech-detect
```

### Análisis de Vulnerabilidades

#### Nuclei - Escaneo de Vulnerabilidades
```bash
# Escaneo básico
nuclei -u example.com

# Con templates específicos
nuclei -u example.com -t cves/ -t vulnerabilities/

# Escaneo de lista de URLs
nuclei -l urls.txt -o nuclei_results.txt
```

### Búsqueda de Información

#### TheHarvester - Recolección de Emails
```bash
# Búsqueda en Google
theHarvester -d example.com -b google

# Múltiples fuentes
theHarvester -d example.com -b google,bing,duckduckgo

# Con límite de resultados
theHarvester -d example.com -b all -l 100
```

#### Sherlock - Búsqueda de Usernames
```bash
# Búsqueda básica
sherlock username

# Con timeout personalizado
sherlock username --timeout 10

# Exportar resultados
sherlock username --csv
```

### Análisis de Metadatos

#### ExifTool - Extracción de Metadatos
```bash
# Analizar imagen
exiftool imagen.jpg

# Extraer GPS
exiftool -gps:all imagen.jpg

# Limpiar metadatos
exiftool -all= imagen.jpg
```

## �📋 Ejemplos de Búsquedas

### 1. Investigación de Dominio

#### Análisis Completo de un Sitio Web
```bash
# Modo consola
OSINT> analyze example.com

# Búsqueda específica
OSINT> search "example.com" domain
```

**Información obtenida:**
- Registrador y fechas de registro/expiración
- Servidores DNS y registros
- Certificados SSL
- Subdominios encontrados
- Tecnologías utilizadas
- Geolocalización de servidores

#### Búsqueda de Subdominios
```bash
OSINT> search "*.example.com" domain
```

### 2. Análisis de Direcciones IP

#### Información de una IP específica
```bash
OSINT> analyze 8.8.8.8
OSINT> search "8.8.8.8" ip
```

**Datos recopilados:**
- Geolocalización (país, ciudad)
- Proveedor de internet (ISP)
- Número de sistema autónomo (ASN)
- Puertos abiertos (con Shodan)
- Servicios detectados
- Historial de seguridad

### 3. Investigación en Redes Sociales

#### Búsqueda de Perfiles
```bash
# Buscar en todas las redes sociales
OSINT> search "nombre_usuario" social

# Buscar menciones
OSINT> search "@nombre_usuario" social
```

#### Análisis de Hashtags
```bash
OSINT> search "#evento2024" social
```

### 4. Monitoreo de Noticias

#### Búsqueda de Noticias Recientes
```bash
# Últimas noticias sobre un tema
OSINT> search "empresa target" news

# Noticias específicas por fecha
OSINT> search "evento" news
```

### 5. Búsqueda de Imágenes

#### Análisis de Imágenes
```bash
OSINT> search "logo empresa" images
```

## 🌐 Uso de la Interfaz Web

### Acceso
1. Iniciar servidor: `python MCP.py --web`
2. Abrir navegador: `http://localhost:5000`
3. Login: `admin` / `admin123`

### Dashboard
- **Estadísticas en tiempo real**
- **Búsqueda rápida** desde la página principal
- **Gráficos interactivos** de resultados
- **Mapa mundial** de distribución geográfica

### Búsqueda Avanzada
1. Ir a **Búsqueda** en el menú
2. Seleccionar **tipo de búsqueda**
3. Configurar **fuentes** a consultar
4. Establecer **filtros** (idioma, fecha, etc.)
5. Habilitar **análisis profundo** si es necesario

### Gestión de Resultados
- **Visualización detallada** de cada resultado
- **Exportación** en múltiples formatos
- **Filtrado y ordenación** avanzada
- **Guardado** de búsquedas favoritas

## 📊 Generación de Reportes

### Reportes Automáticos
```bash
# Reporte de los últimos 7 días
OSINT> report 7 html

# Reporte mensual en PDF
OSINT> report 30 pdf

# Datos en Excel para análisis
OSINT> report 14 xlsx
```

### Reportes desde Web
1. Ir a **Reportes** en el menú
2. Seleccionar **período** de tiempo
3. Elegir **formato** de exportación
4. Configurar **filtros** específicos
5. **Generar y descargar**

### Tipos de Reportes Disponibles

#### HTML Interactivo
- Gráficos con Chart.js
- Mapas interactivos con Plotly
- Diseño responsivo
- Enlaces clickeables

#### PDF Profesional
- Formato empresarial
- Tablas estructuradas
- Gráficos estáticos
- Metadatos completos

#### Excel Avanzado
- Múltiples hojas de cálculo
- Gráficos integrados
- Datos pivot
- Formato profesional

#### CSV para Análisis
- Datos tabulares
- Compatible con herramientas de análisis
- Formato universal
- Fácil importación

## 🔍 Casos de Uso Reales

### 1. Due Diligence Empresarial

#### Objetivo: Investigar una empresa antes de una inversión

```bash
# Búsqueda general de la empresa
OSINT> search "NombreEmpresa Ltd" general

# Análisis de su sitio web
OSINT> analyze empresa.com

# Búsqueda en noticias
OSINT> search "NombreEmpresa controversia" news

# Búsqueda en redes sociales
OSINT> search "NombreEmpresa" social

# Generar reporte completo
OSINT> report 90 pdf
```

**Información obtenida:**
- Presencia online y reputación
- Infraestructura tecnológica
- Menciones en medios
- Actividad en redes sociales
- Posibles riesgos o controversias

### 2. Investigación de Seguridad

#### Objetivo: Evaluar la superficie de ataque de una organización

```bash
# Análisis de dominio principal
OSINT> analyze target.com

# Búsqueda de subdominios
OSINT> search "*.target.com" domain

# Análisis de IPs asociadas
OSINT> analyze 192.168.1.1

# Búsqueda de información sensible expuesta
OSINT> search "site:target.com password" general
```

**Resultados del análisis:**
- Puertos abiertos y servicios expuestos
- Certificados SSL y su validez
- Subdominios no protegidos
- Información sensible indexada
- Posibles vectores de ataque

### 3. Investigación de Personas

#### Objetivo: Verificar la identidad de una persona

```bash
# Búsqueda general
OSINT> search "Juan Pérez Madrid" general

# Redes sociales
OSINT> search "juan.perez" social

# Búsqueda profesional
OSINT> search "Juan Pérez ingeniero" general

# Verificación en noticias
OSINT> search "Juan Pérez" news
```

**Información recopilada:**
- Perfiles en redes sociales
- Historial profesional
- Menciones públicas
- Posible ubicación geográfica
- Conexiones y asociaciones

### 4. Monitoreo de Marca

#### Objetivo: Vigilar la reputación online de una marca

```bash
# Configurar búsqueda recurrente
OSINT> search "MiMarca opiniones" general

# Monitoreo en redes sociales
OSINT> search "#MiMarca" social

# Seguimiento de noticias
OSINT> search "MiMarca" news

# Análisis de competencia
OSINT> search "alternativa MiMarca" general
```

**Métricas obtenidas:**
- Menciones positivas/negativas
- Tendencias de opinión
- Actividad de la competencia
- Oportunidades de mejora
- Alertas tempranas de crisis

## ⚙️ Configuración Avanzada

### APIs Especializadas

#### Shodan (Análisis de dispositivos conectados)
```json
{
  "shodan_api_key": "TU_API_KEY_SHODAN"
}
```

**Beneficios:**
- Información detallada de puertos abiertos
- Servicios y versiones detectadas
- Vulnerabilidades conocidas
- Dispositivos IoT expuestos

#### VirusTotal (Análisis de seguridad)
```json
{
  "virustotal_api_key": "TU_API_KEY_VIRUSTOTAL"
}
```

**Capacidades:**
- Reputación de dominios/IPs
- Detección de malware
- Análisis de URLs sospechosas
- Histórico de amenazas

#### Twitter API (Análisis social avanzado)
```json
{
  "twitter_bearer_token": "TU_BEARER_TOKEN"
}
```

**Funcionalidades:**
- Búsqueda en tiempo real
- Análisis de sentimientos
- Métricas de engagement
- Redes de influencia

### Configuración de Alertas

#### Ejemplo: Monitoreo Continuo
```json
{
  "alerts": [
    {
      "name": "Monitoreo Marca",
      "query": "MiEmpresa",
      "search_type": "general",
      "frequency": "daily",
      "notification_methods": ["email", "telegram"]
    },
    {
      "name": "Seguridad Dominio",
      "query": "mi-dominio.com",
      "search_type": "domain", 
      "frequency": "weekly",
      "notification_methods": ["email"]
    }
  ]
}
```

## 🛡️ Consideraciones de Seguridad

### Buenas Prácticas

1. **Rate Limiting**: No exceder límites de APIs
2. **Rotación de IPs**: Usar proxies si es necesario
3. **User Agents**: Rotar identificadores de navegador
4. **Timeouts**: Configurar timeouts apropiados

### Consideraciones Legales

1. **Términos de Servicio**: Respetar ToS de cada plataforma
2. **Privacidad**: No violar la privacidad de personas
3. **Jurisdicción**: Conocer las leyes locales
4. **Uso Ético**: Usar solo para propósitos legítimos

### Anonimato y Privacidad

```json
{
  "proxy_config": {
    "enabled": true,
    "proxy_list": ["proxy1:port", "proxy2:port"],
    "rotation_interval": 300
  },
  "tor_config": {
    "enabled": false,
    "socks_port": 9050
  }
}
```

## 📈 Optimización y Rendimiento

### Configuración de Rendimiento

```json
{
  "performance": {
    "max_concurrent_requests": 10,
    "request_timeout": 30,
    "retry_attempts": 3,
    "rate_limit_delay": 1.0,
    "cache_enabled": true,
    "cache_ttl": 3600
  }
}
```

### Monitoreo de Recursos

```bash
# Ver estadísticas del sistema
OSINT> stats

# Información de base de datos
OSINT> db-info

# Estado de las APIs
OSINT> api-status
```

## 🔧 Troubleshooting

### Problemas Comunes

#### Error: "No se pueden instalar dependencias"
```bash
# Actualizar pip
pip install --upgrade pip

# Instalar con usuario
pip install --user -r requirements.txt

# Usar entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

#### Error: "Puerto 5000 ocupado"
```json
{
  "web_port": 8080
}
```

#### Error: "APIs no responden"
```bash
# Verificar conectividad
curl -I https://www.google.com

# Verificar DNS
nslookup google.com

# Probar con proxy
export HTTP_PROXY=http://proxy:port
```

#### Error: "Base de datos corrupta"
```bash
# Backup actual
cp osint_data.db osint_data.db.backup

# Resetear base de datos
rm osint_data.db
python MCP.py
```

### Logs y Debugging

```bash
# Ver logs detallados
tail -f logs/osint.log

# Modo debug
python MCP.py --debug

# Verificar configuración
python MCP.py --check-config
```

## 📞 Soporte y Comunidad

### Recursos Adicionales

- **Documentación**: Wiki completa del proyecto
- **Videos**: Tutoriales paso a paso
- **Ejemplos**: Casos de uso reales
- **Templates**: Plantillas de reportes

### Obtener Ayuda

1. **GitHub Issues**: Reportar bugs y solicitar features
2. **Documentación**: Consultar la wiki del proyecto
3. **Comunidad**: Unirse a Discord/Telegram
4. **Email**: Contacto directo para soporte premium

### Contribuir al Proyecto

```bash
# Fork del repositorio
git clone https://github.com/tuusuario/osint-searcher.git

# Crear rama feature
git checkout -b nueva-funcionalidad

# Realizar cambios y commit
git commit -m "Agregar nueva funcionalidad"

# Enviar pull request
git push origin nueva-funcionalidad
```

---

**📝 Nota**: Este documento se actualiza constantemente. Consulta la versión más reciente en el repositorio del proyecto.

**⚖️ Legal**: Usa esta herramienta de manera ética y legal. Los usuarios son responsables del cumplimiento de todas las leyes aplicables.
