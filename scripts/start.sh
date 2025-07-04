#!/bin/bash

# 🔍 OSINT Platform - Script de Inicio
# Configuración automática y lanzamiento del servidor

echo "🔍 =========================================="
echo "   OSINT Platform v2.0.0 - Inicio"
echo "=========================================="

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    echo "   Instala Python 3.8 o superior"
    exit 1
fi

echo "✅ Python detectado: $(python3 --version)"

# Verificar pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 no está instalado"
    echo "   Instala pip3 para Python 3"
    exit 1
fi

echo "✅ pip3 detectado"

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "🔧 Creando entorno virtual..."
    python3 -m venv venv
    echo "✅ Entorno virtual creado"
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Verificar e instalar dependencias
echo "📦 Verificando dependencias..."
if [ ! -f "venv/pyvenv.cfg" ] || [ requirements.txt -nt venv/pyvenv.cfg ]; then
    echo "📦 Instalando/actualizando dependencias..."
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "✅ Dependencias instaladas"
fi

# Crear directorios necesarios
echo "📁 Creando directorios..."
mkdir -p data logs exports config

# Verificar configuración
if [ ! -f "config/.env" ]; then
    echo "⚙️  Creando archivo de configuración..."
    cp config/.env.template config/.env
    echo "⚠️  Por favor, edita config/.env con tus configuraciones"
fi

# Inicializar base de datos
echo "🗄️  Inicializando base de datos..."
python3 -c "
try:
    from src.models.database import db_manager
    db_manager.create_tables()
    print('✅ Base de datos inicializada')
except Exception as e:
    print(f'⚠️  Error iniciando BD: {e}')
"

# Verificar integridad de archivos
echo "🔍 Verificando integridad de archivos..."
if [ -f "src/osint_advanced.py" ] && [ -f "src/osint_specialized.py" ]; then
    echo "✅ Módulos OSINT encontrados"
else
    echo "⚠️  Algunos módulos OSINT no se encontraron"
fi

# Configurar variables de entorno
export FLASK_ENV=production
export FLASK_DEBUG=false
export HOST=${HOST:-0.0.0.0}
export PORT=${PORT:-5000}

echo ""
echo "🎉 Configuración completada!"
echo "🌐 Iniciando servidor en http://${HOST}:${PORT}"
echo ""
echo "Para acceder a la plataforma:"
echo "  📱 Interfaz web: http://${HOST}:${PORT}"
echo "  🔐 Registro: http://${HOST}:${PORT}/register"
echo "  🔑 Login: http://${HOST}:${PORT}/login"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo "=========================================="
echo ""

# Iniciar la aplicación
python3 app.py
    echo "❌ pip3 no está instalado"
    echo "   Instala pip para Python 3"
    exit 1
fi

echo "✅ pip detectado"

# Instalar dependencias
echo ""
echo "📦 Instalando dependencias..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Error instalando dependencias"
    echo "   Verifica el archivo requirements.txt"
    exit 1
fi

echo "✅ Dependencias instaladas correctamente"

# Verificar configuración
if [ ! -f "osint_config.json" ]; then
    echo ""
    echo "⚙️  Generando configuración inicial..."
    python3 MCP.py --generate-config
    echo "✅ Configuración creada: osint_config.json"
    echo ""
    echo "🔧 IMPORTANTE: Edita osint_config.json con tus credenciales"
    echo "   - email_username: Tu email"
    echo "   - email_password: Contraseña de aplicación"
    echo "   - API keys opcionales para servicios especializados"
    echo ""
    read -p "¿Deseas editar la configuración ahora? (y/N): " edit_config
    
    if [[ $edit_config =~ ^[Yy]$ ]]; then
        if command -v nano &> /dev/null; then
            nano osint_config.json
        elif command -v vim &> /dev/null; then
            vim osint_config.json
        elif command -v code &> /dev/null; then
            code osint_config.json
        else
            echo "📝 Edita manualmente: osint_config.json"
        fi
    fi
else
    echo "✅ Configuración existente encontrada"
fi

# Crear directorios necesarios
mkdir -p templates static logs exports

echo ""
echo "🚀 =========================================="
echo "   Opciones de Inicio"
echo "=========================================="
echo "1. 🌐 Interfaz Web (Recomendado)"
echo "2. 💻 Modo Consola"
echo "3. 🔧 Solo configuración"
echo "4. ❌ Salir"
echo ""

read -p "Selecciona una opción (1-4): " option

case $option in
    1)
        echo ""
        echo "🌐 Iniciando interfaz web..."
        echo "   Accede a: http://localhost:5000"
        echo "   Usuario: admin"
        echo "   Contraseña: admin123 (cambiar en configuración)"
        echo ""
        echo "🛑 Presiona Ctrl+C para detener el servidor"
        echo ""
        python3 MCP.py --web-only
        ;;
    2)
        echo ""
        echo "💻 Iniciando modo consola..."
        echo ""
        python3 MCP.py
        ;;
    3)
        echo ""
        echo "🔧 Configuración completada"
        echo "   Ejecuta: python3 MCP.py para iniciar"
        ;;
    4)
        echo ""
        echo "👋 ¡Hasta luego!"
        exit 0
        ;;
    *)
        echo ""
        echo "❌ Opción inválida"
        echo "   Ejecuta: python3 MCP.py para iniciar manualmente"
        exit 1
        ;;
esac
