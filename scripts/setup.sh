#!/bin/bash
# Script de configuración inicial para la plataforma OSINT

echo "🔍 Configuración inicial de OSINT Platform"
echo "=========================================="

# Crear directorios necesarios
echo "📁 Creando directorios..."
mkdir -p data
mkdir -p logs
mkdir -p exports
mkdir -p config

# Crear archivo de configuración .env si no existe
if [ ! -f "config/.env" ]; then
    echo "⚙️  Creando archivo de configuración..."
    cp config/.env.template config/.env
    echo "✅ Archivo .env creado. Por favor, edítalo con tus configuraciones."
fi

# Verificar Python
echo "🐍 Verificando Python..."
if command -v python3 &> /dev/null; then
    echo "✅ Python3 encontrado: $(python3 --version)"
else
    echo "❌ Python3 no encontrado. Por favor instala Python 3.8 o superior."
    exit 1
fi

# Verificar pip
if command -v pip3 &> /dev/null; then
    echo "✅ pip3 encontrado"
else
    echo "❌ pip3 no encontrado. Por favor instala pip3."
    exit 1
fi

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "🔧 Creando entorno virtual..."
    python3 -m venv venv
    echo "✅ Entorno virtual creado"
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Inicializar base de datos
echo "🗄️  Inicializando base de datos..."
python3 -c "
from src.models.database import db_manager
db_manager.create_tables()
db_manager.init_default_config()
print('✅ Base de datos inicializada')
"

# Configurar permisos
echo "🔐 Configurando permisos..."
chmod +x scripts/start.sh
chmod +x scripts/setup.sh

echo ""
echo "🎉 Configuración completada!"
echo ""
echo "Para iniciar la plataforma:"
echo "  1. Activa el entorno virtual: source venv/bin/activate"
echo "  2. Configura tus credenciales en config/.env"
echo "  3. Inicia el servidor: python3 app.py"
echo "  4. O usa el script: ./scripts/start.sh"
echo ""
echo "🌐 La plataforma estará disponible en: http://localhost:5000"
echo ""
