# 📖 Guía de Usuario - OSINT Searcher

## 🎯 Introducción

OSINT Searcher es una herramienta avanzada de inteligencia de fuentes abiertas que permite realizar búsquedas especializadas, análisis de dominios, Google Dorking automatizado y generación de reportes profesionales.

## 🚀 Inicio Rápido

### 1. Acceso al Sistema

**Interfaz Web:**
- Abrir navegador en `http://localhost:5000`
- Usar las credenciales por defecto: `admin` / `admin123`

**Modo Consola:**
- Ejecutar `python MCP.py --console`
- Seguir las instrucciones en pantalla

### 2. Tipos de Búsqueda Disponibles

#### 🔍 Búsqueda General
- **Cuándo usar**: Para obtener información general sobre un tema
- **Cómo usar**: Ingresar términos de búsqueda y seleccionar "Búsqueda General"
- **Ejemplo**: "cybersecurity trends 2025"

#### 🌐 Análisis de Dominio
- **Cuándo usar**: Para analizar la infraestructura de un dominio
- **Cómo usar**: Ingresar un dominio (ej: example.com)
- **Qué obtienes**: WHOIS, DNS, SSL, subdominios, tecnologías

#### 📡 Análisis de IP
- **Cuándo usar**: Para obtener información sobre una dirección IP
- **Cómo usar**: Ingresar una IP (ej: 8.8.8.8)
- **Qué obtienes**: Geolocalización, ISP, ASN, puertos

#### 🕵️ Google Dorking
- **Cuándo usar**: Para búsquedas especializadas y detección de información sensible
- **Cómo usar**: Seleccionar categorías específicas
- **Categorías disponibles**:
  - **Archivos Confidenciales**: PDFs, DOCs, XLS con información sensible
  - **Directorios Expuestos**: Listados de archivos y directorios
  - **Información Corporativa**: Datos empresariales y empleados
  - **Redes Sociales**: Perfiles y menciones en redes sociales
  - **Errores de Aplicaciones**: Páginas de error que revelan información

## 🛡️ Interpretación de Resultados

### Niveles de Riesgo
- **🟢 BAJO**: Información pública normal
- **🟡 MEDIO**: Información que podría ser sensible
- **🟠 ALTO**: Información potencialmente peligrosa
- **🔴 CRÍTICO**: Información que requiere atención inmediata

### Qué Hacer con los Resultados
1. **Revisar cada resultado manualmente**
2. **Verificar la veracidad de la información**
3. **Documentar hallazgos importantes**
4. **Tomar medidas correctivas si es necesario**

## 📊 Generación de Reportes

### Formatos Disponibles
- **HTML**: Interactivo con gráficos
- **PDF**: Profesional para presentaciones
- **Excel**: Análisis de datos
- **CSV**: Datos tabulares

### Cómo Generar Reportes
1. Realizar búsquedas
2. Ir a "Historial" → "Generar Reporte"
3. Seleccionar período y formato
4. Descargar el archivo generado

## �️ Herramientas CLI Integradas

### Instalación de Herramientas
La plataforma incluye un conjunto completo de herramientas OSINT CLI que se pueden instalar automáticamente:

```bash
# Instalar todas las herramientas recomendadas
bash install_osint_tools.sh

# Ver herramientas disponibles
python -c "import osint_cli_tools; osint_cli_tools.list_tools()"
```

### Herramientas Principales

#### 🔍 Reconocimiento de Dominios
- **Subfinder**: Enumeración de subdominios
- **Amass**: Mapeo de superficie de ataque
- **Assetfinder**: Búsqueda de activos
- **Gobuster**: Fuerza bruta de subdominios

#### 🌐 Análisis de Red
- **Nmap**: Escaneo de puertos y servicios
- **Masscan**: Escaneo rápido de gran escala
- **Httpx**: Sondeo HTTP/HTTPS
- **Nuclei**: Escáner de vulnerabilidades

#### 📊 Análisis de Datos
- **ExifTool**: Extracción de metadatos
- **Whois**: Información de dominio
- **Dig**: Consultas DNS avanzadas
- **Waybackurls**: URLs del archivo web

#### 🔎 Búsqueda Especializada
- **TheHarvester**: Recolección de emails e información
- **Recon-ng**: Framework de reconocimiento
- **Maltego**: Análisis de enlaces (comunidad)
- **Spiderfoot**: Automatización OSINT

Para más información, consulta `docs/OSINT_CLI_TOOLS.md`

## �🔧 Consejos de Uso

### Mejores Prácticas
1. **Usar términos específicos**: Mejores resultados con consultas precisas
2. **Combinar tipos de búsqueda**: Usar múltiples enfoques
3. **Verificar información**: Siempre confirmar datos importantes
4. **Documentar proceso**: Mantener registro de búsquedas realizadas
5. **Usar herramientas CLI**: Aprovechar las herramientas especializadas integradas
6. **Configurar APIs**: Obtener claves API para mejores resultados

### Limitaciones y Consideraciones
- **Rate Limiting**: Evitar hacer demasiadas búsquedas muy rápido
- **Términos de Uso**: Respetar términos de servicio de motores de búsqueda
- **Privacidad**: No buscar información personal sin autorización
- **Legalidad**: Usar solo para fines legítimos y éticos
- **Dependencias**: Algunas herramientas requieren instalación adicional

### ✨ Nueva Funcionalidad: Búsqueda Asistida por IA

OSINT Searcher ahora incluye una potente función de búsqueda asistida por Inteligencia Artificial. Esta te permite describir tu objetivo de investigación en lenguaje natural, y la IA se encargará de:
1.  **Interpretar tu solicitud**: Entenderá qué o a quién buscas y qué tipo de información necesitas.
2.  **Orquestar las búsquedas**: Ejecutará automáticamente las herramientas OSINT relevantes.
3.  **Generar un resumen**: Te proporcionará un resumen ejecutivo de los hallazgos.

**Cómo usar la Búsqueda IA:**
1.  En la interfaz web, ve a la página de "Búsqueda".
2.  Selecciona la pestaña "Búsqueda IA" (generalmente marcada con un ícono de ✨ o 🧠).
3.  En el campo de texto (prompt), describe tu investigación. Sé tan específico como puedas.
    *   **Ejemplo de prompt para una empresa**: "Investiga a la empresa 'Soluciones Digitales Avanzadas SAS' con NIT 900.123.456-7 ubicada en Bogotá. Necesito información sobre sus registros comerciales, directivos principales y cualquier noticia reciente sobre brechas de seguridad. Utiliza Google Dorks si es pertinente."
    *   **Ejemplo de prompt para una persona**: "Busca información sobre 'Laura Valderrama', correo electrónico 'laura.v@email.com', que es ingeniera de software en Medellín. Me interesan sus perfiles profesionales en redes sociales y publicaciones técnicas."
    *   **Ejemplo de prompt para un tema**: "Genera un informe sobre las últimas tácticas de phishing dirigidas al sector financiero en América Latina durante el último trimestre."
4.  Haz clic en "Procesar con IA".
5.  Los resultados incluirán:
    *   La **interpretación** que hizo la IA de tu prompt.
    *   Un **resumen ejecutivo** de los hallazgos.
    *   Una **muestra de los resultados crudos** obtenidos por las herramientas OSINT.

**Configuración (Importante):**
Para utilizar la funcionalidad de IA, necesitas configurar tu propia API Key de OpenAI.
1.  Localiza el archivo `config/ia_config.json` en la carpeta de instalación de OSINT Searcher.
2.  Abre el archivo y reemplaza `"TU_API_KEY_DE_OPENAI_AQUI"` con tu API Key válida de OpenAI.
    ```json
    {
      "openai_api_key": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", // Tu clave aquí
      "default_model_name": "gpt-3.5-turbo",
      // ... otras configuraciones ...
    }
    ```
3.  Guarda el archivo. La funcionalidad de IA debería estar activa la próxima vez que uses la herramienta o reinicies el servidor.

**Consejos para prompts efectivos:**
*   **Claridad**: Indica claramente el objetivo principal (persona, empresa, dominio, tema).
*   **Detalles**: Proporciona cualquier dato conocido (NIT, correo, URLs, nombres específicos).
*   **Necesidades**: Especifica qué tipo de información buscas (financiera, técnica, reputacional, legal).
*   **Fuentes (opcional)**: Si tienes idea de dónde buscar (ej. "bases de datos gubernamentales", "foros técnicos").
*   **Dorking**: Menciona si quieres que se usen técnicas de Google Dorking.

## �️ Herramientas CLI Integradas

### Instalación de Herramientas

La plataforma incluye un conjunto completo de herramientas OSINT CLI que se pueden instalar automáticamente:

```bash
# Instalar todas las herramientas recomendadas
bash install_osint_tools.sh

# Ver herramientas disponibles
python -c "import osint_cli_tools; osint_cli_tools.list_tools()"
```

### Herramientas Principales

#### 🔍 Reconocimiento de Dominios

- **Subfinder**: Enumeración de subdominios
- **Amass**: Mapeo de superficie de ataque
- **Assetfinder**: Búsqueda de activos
- **Gobuster**: Fuerza bruta de subdominios

#### 🌐 Análisis de Red

- **Nmap**: Escaneo de puertos y servicios
- **Masscan**: Escaneo rápido de gran escala
- **Httpx**: Sondeo HTTP/HTTPS
- **Nuclei**: Escáner de vulnerabilidades

#### 📊 Análisis de Datos

- **ExifTool**: Extracción de metadatos
- **Whois**: Información de dominio
- **Dig**: Consultas DNS avanzadas
- **Waybackurls**: URLs del archivo web

#### 🔎 Búsqueda Especializada

- **TheHarvester**: Recolección de emails e información
- **Recon-ng**: Framework de reconocimiento
- **Maltego**: Análisis de enlaces (comunidad)
- **Spiderfoot**: Automatización OSINT

Para más información, consulta `docs/OSINT_CLI_TOOLS.md`

## �🚨 Casos de Uso Comunes

### 1. Auditoría de Seguridad

```bash
1. Análisis de dominio corporativo
2. Google Dorking para archivos sensibles
3. Revisión de información expuesta
4. Generación de reporte con recomendaciones
```

### 2. Investigación Competitiva
```
1. Búsqueda general sobre la empresa
2. Análisis de redes sociales
3. Información corporativa
4. Reporte comparativo
```

### 3. Verificación de Identidad Digital
```
1. Búsqueda de nombre/empresa
2. Análisis de redes sociales
3. Verificación de datos públicos
4. Reporte de presencia digital
```

## 📞 Soporte y Ayuda

### Problemas Comunes

**Error de conexión:**
- Verificar conexión a internet
- Comprobar que el servidor esté ejecutándose

**Resultados limitados:**
- Algunos motores pueden tener restricciones
- Intentar con diferentes términos de búsqueda

**Reportes no se generan:**
- Verificar que hay datos para el período seleccionado
- Comprobar permisos de escritura en carpeta exports/

### Logs y Depuración
Los logs se encuentran en la carpeta `logs/` y contienen información detallada sobre errores y operaciones.

## 🔒 Consideraciones Éticas y Legales

### Uso Responsable
- Solo buscar información que sea de dominio público
- No utilizar para acoso o actividades maliciosas
- Respetar la privacidad de las personas
- Cumplir con las leyes locales sobre privacidad

### Términos de Servicio
- Respetar los términos de uso de los motores de búsqueda
- No realizar actividades automatizadas excesivas
- Usar User-Agents apropiados
- Mantener delays entre búsquedas

---

*Esta guía es un documento vivo que se actualiza constantemente. Para más información, consulta el README.md del proyecto.*
