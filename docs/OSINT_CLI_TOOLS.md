# 🛠️ Herramientas OSINT CLI Open Source

Esta es una colección completa de herramientas de línea de comandos (CLI) open source para reconocimiento e inteligencia de fuentes abiertas (OSINT), organizadas por categorías.

## 📋 Índice

- [Reconocimiento de Dominios y DNS](#reconocimiento-de-dominios-y-dns)
- [Enumeración de Subdominios](#enumeración-de-subdominios)
- [Descubrimiento de Puertos y Servicios](#descubrimiento-de-puertos-y-servicios)
- [Análisis de Redes Sociales](#análisis-de-redes-sociales)
- [Búsqueda de Emails y Usuarios](#búsqueda-de-emails-y-usuarios)
- [Análisis de Metadatos](#análisis-de-metadatos)
- [Reconocimiento Web](#reconocimiento-web)
- [Geolocalización](#geolocalización)
- [Análisis de Imágenes](#análisis-de-imágenes)
- [Investigación de Personas](#investigación-de-personas)
- [Análisis de Redes](#análisis-de-redes)
- [Herramientas de Automatización](#herramientas-de-automatización)
- [Frameworks Completos](#frameworks-completos)

---

## 🌐 Reconocimiento de Dominios y DNS

### **dig**
```bash
# Información básica DNS
dig example.com

# Consulta específica de registros
dig example.com MX
dig example.com NS
dig example.com TXT

# Transferencia de zona
dig @ns1.example.com example.com AXFR

# Búsqueda inversa
dig -x 8.8.8.8
```

### **nslookup**
```bash
# Consulta básica
nslookup example.com

# Consulta de registros específicos
nslookup -type=MX example.com
nslookup -type=NS example.com
```

### **host**
```bash
# Información del host
host example.com

# Información específica
host -t MX example.com
host -t TXT example.com
```

### **dnsrecon**
**Instalación:**
```bash
git clone https://github.com/darkoperator/dnsrecon.git
cd dnsrecon
pip3 install -r requirements.txt
```

**Uso:**
```bash
# Enumeración completa
python3 dnsrecon.py -d example.com

# Transferencia de zona
python3 dnsrecon.py -d example.com -t axfr

# Fuerza bruta de subdominios
python3 dnsrecon.py -d example.com -t brt -D subdomains.txt
```

### **dnsenum**
**Instalación:**
```bash
apt-get install dnsenum
# o
git clone https://github.com/fwaeytens/dnsenum.git
```

**Uso:**
```bash
# Enumeración completa
dnsenum example.com

# Con archivo de wordlist personalizado
dnsenum --dnsserver 8.8.8.8 -f subdomains.txt example.com
```

### **fierce**
**Instalación:**
```bash
pip3 install fierce
```

**Uso:**
```bash
# Enumeración de subdominios
fierce --domain example.com

# Con DNS específico
fierce --dns-servers 8.8.8.8 --domain example.com
```

---

## 🔍 Enumeración de Subdominios

### **Subfinder**
**Instalación:**
```bash
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
```

**Uso:**
```bash
# Búsqueda básica
subfinder -d example.com

# Salida a archivo
subfinder -d example.com -o subdomains.txt

# Múltiples dominios
subfinder -dL domains.txt -o results.txt

# Con APIs configuradas
subfinder -d example.com -config config.yaml
```

### **Assetfinder**
**Instalación:**
```bash
go install github.com/tomnomnom/assetfinder@latest
```

**Uso:**
```bash
# Búsqueda básica
assetfinder example.com

# Solo subdominios
assetfinder --subs-only example.com
```

### **Findomain**
**Instalación:**
```bash
wget https://github.com/Findomain/Findomain/releases/latest/download/findomain-linux
chmod +x findomain-linux
sudo mv findomain-linux /usr/local/bin/findomain
```

**Uso:**
```bash
# Búsqueda básica
findomain -t example.com

# Salida a archivo
findomain -t example.com -o

# Monitoreo continuo
findomain -t example.com -m
```

### **Amass**
**Instalación:**
```bash
go install github.com/OWASP/Amass/v3/...@latest
```

**Uso:**
```bash
# Enumeración pasiva
amass enum -passive -d example.com

# Enumeración activa
amass enum -active -d example.com

# Con APIs
amass enum -config config.ini -d example.com

# Análisis de infraestructura
amass intel -d example.com
```

### **Knock**
**Instalación:**
```bash
git clone https://github.com/guelfoweb/knock.git
cd knock
python setup.py install
```

**Uso:**
```bash
# Búsqueda de subdominios
python knock.py example.com

# Con wordlist personalizada
python knock.py -w wordlist.txt example.com
```

### **Sublist3r**
**Instalación:**
```bash
git clone https://github.com/aboul3la/Sublist3r.git
cd Sublist3r
pip install -r requirements.txt
```

**Uso:**
```bash
# Búsqueda básica
python sublist3r.py -d example.com

# Con brute force
python sublist3r.py -d example.com -b

# Múltiples threads
python sublist3r.py -d example.com -t 100
```

---

## 🔌 Descubrimiento de Puertos y Servicios

### **Nmap**
```bash
# Escaneo básico
nmap example.com

# Escaneo de puertos específicos
nmap -p 80,443,22 example.com

# Escaneo de servicios
nmap -sV example.com

# Escaneo sigiloso
nmap -sS example.com

# Scripts de enumeración
nmap --script vuln example.com
nmap --script http-enum example.com
```

### **Masscan**
**Instalación:**
```bash
git clone https://github.com/robertdavidgraham/masscan.git
cd masscan
make
sudo make install
```

**Uso:**
```bash
# Escaneo rápido
sudo masscan -p1-65535 example.com --rate=1000

# Puertos específicos
sudo masscan -p80,443 10.0.0.0/8 --rate=10000
```

### **Rustscan**
**Instalación:**
```bash
wget https://github.com/RustScan/RustScan/releases/latest/download/rustscan_2.1.1_amd64.deb
sudo dpkg -i rustscan_2.1.1_amd64.deb
```

**Uso:**
```bash
# Escaneo rápido
rustscan -a example.com

# Con nmap integrado
rustscan -a example.com -- -sV -sC
```

---

## 📱 Análisis de Redes Sociales

### **Sherlock**
**Instalación:**
```bash
git clone https://github.com/sherlock-project/sherlock.git
cd sherlock
pip3 install -r requirements.txt
```

**Uso:**
```bash
# Búsqueda de usuario
python3 sherlock username

# Múltiples usuarios
python3 sherlock user1 user2 user3

# Con timeout personalizado
python3 sherlock --timeout 10 username
```

### **Social Mapper**
**Instalación:**
```bash
git clone https://github.com/Greenwolf/social_mapper.git
cd social_mapper
pip3 install -r requirements.txt
```

**Uso:**
```bash
# Búsqueda por nombre
python3 social_mapper.py -f name -n "John Doe" -m fast

# Búsqueda por email
python3 social_mapper.py -f email -e "john@example.com" -m thorough
```

### **TweetScraper**
**Instalación:**
```bash
git clone https://github.com/taspinar/twitterscraper.git
cd twitterscraper
pip install twitterscraper
```

**Uso:**
```bash
# Scraping de tweets
twitterscraper "keyword" -l 100 -o tweets.json

# Por usuario
twitterscraper "from:username" -l 50
```

### **InstagramOSINT**
**Instalación:**
```bash
git clone https://github.com/sc1341/InstagramOSINT.git
cd InstagramOSINT
pip3 install -r requirements.txt
```

**Uso:**
```bash
# Información de usuario
python3 main.py -u username

# Descargar imágenes
python3 main.py -u username -d
```

---

## 📧 Búsqueda de Emails y Usuarios

### **theHarvester**
**Instalación:**
```bash
git clone https://github.com/laramies/theHarvester.git
cd theHarvester
pip3 install -r requirements.txt
```

**Uso:**
```bash
# Búsqueda en múltiples fuentes
python3 theHarvester.py -d example.com -b all

# Fuente específica
python3 theHarvester.py -d example.com -b google

# Limitar resultados
python3 theHarvester.py -d example.com -l 500 -b bing
```

### **Hunter.io CLI**
**Instalación:**
```bash
npm install -g hunter.io
```

**Uso:**
```bash
# Buscar emails en dominio
hunter domain-search --domain example.com

# Verificar email
hunter email-verifier --email test@example.com
```

### **h8mail**
**Instalación:**
```bash
pip3 install h8mail
```

**Uso:**
```bash
# Búsqueda básica
h8mail -t target@example.com

# Múltiples targets
h8mail -t targets.txt

# Con APIs configuradas
h8mail -t target@example.com -c config.ini
```

### **Holehe**
**Instalación:**
```bash
pip3 install holehe
```

**Uso:**
```bash
# Verificar si email está registrado en servicios
holehe test@example.com

# Múltiples emails
holehe -f emails.txt
```

---

## 📄 Análisis de Metadatos

### **ExifTool**
**Instalación:**
```bash
apt-get install libimage-exiftool-perl
# o
wget https://exiftool.org/ExifTool-12.44.tar.gz
```

**Uso:**
```bash
# Extraer metadatos
exiftool image.jpg

# Eliminar metadatos
exiftool -all= image.jpg

# Buscar archivos con GPS
exiftool -gps:all -r directory/
```

### **FOCA**
**Instalación:**
```bash
git clone https://github.com/ElevenPaths/FOCA.git
```

### **MetaGoofil**
**Instalación:**
```bash
git clone https://github.com/laramies/metagoofil.git
cd metagoofil
pip3 install -r requirements.txt
```

**Uso:**
```bash
# Búsqueda de documentos
python3 metagoofil.py -d example.com -t pdf,doc,xls -l 100 -n 50 -o downloads -f results.html
```

---

## 🌐 Reconocimiento Web

### **Gobuster**
**Instalación:**
```bash
go install github.com/OJ/gobuster/v3@latest
```

**Uso:**
```bash
# Enumeración de directorios
gobuster dir -u http://example.com -w /usr/share/wordlists/dirb/common.txt

# Enumeración de subdominios
gobuster dns -d example.com -w subdomains.txt

# Enumeración de VHosts
gobuster vhost -u http://example.com -w vhosts.txt
```

### **ffuf**
**Instalación:**
```bash
go install github.com/ffuf/ffuf@latest
```

**Uso:**
```bash
# Fuzzing de directorios
ffuf -w wordlist.txt -u http://example.com/FUZZ

# Fuzzing de subdominios
ffuf -w subdomains.txt -u http://FUZZ.example.com

# Fuzzing de parámetros
ffuf -w params.txt -u http://example.com/?FUZZ=test
```

### **dirb**
```bash
# Escaneo básico
dirb http://example.com

# Con wordlist personalizada
dirb http://example.com /path/to/wordlist.txt

# Con extensiones específicas
dirb http://example.com -X .php,.html,.txt
```

### **dirsearch**
**Instalación:**
```bash
git clone https://github.com/maurosoria/dirsearch.git
cd dirsearch
pip3 install -r requirements.txt
```

**Uso:**
```bash
# Búsqueda básica
python3 dirsearch.py -u http://example.com

# Con extensiones específicas
python3 dirsearch.py -u http://example.com -e php,html,js

# Múltiples threads
python3 dirsearch.py -u http://example.com -t 50
```

### **WhatWeb**
**Instalación:**
```bash
gem install whatweb
```

**Uso:**
```bash
# Análisis básico
whatweb example.com

# Análisis agresivo
whatweb -a 3 example.com

# Múltiples sitios
whatweb -i urls.txt
```

### **httpx**
**Instalación:**
```bash
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
```

**Uso:**
```bash
# Verificar hosts activos
httpx -l hosts.txt

# Con información detallada
httpx -l hosts.txt -title -status-code -content-length

# Screenshots
httpx -l hosts.txt -screenshot
```

---

## 🗺️ Geolocalización

### **IP2Location**
**Instalación:**
```bash
pip3 install IP2Location
```

**Uso:**
```bash
python3 -c "import IP2Location; db = IP2Location.IP2Location(); print(db.get_all('8.8.8.8'))"
```

### **GeoIP**
```bash
# Con geoiplookup
geoiplookup 8.8.8.8

# Con whois
whois 8.8.8.8
```

### **IPinfo**
**Instalación:**
```bash
npm install -g node-ipinfo
```

**Uso:**
```bash
# Información de IP
ipinfo 8.8.8.8

# Información detallada
ipinfo 8.8.8.8 --json
```

---

## 🖼️ Análisis de Imágenes

### **TinEye CLI**
**Instalación:**
```bash
pip install tineye-api
```

### **Google Images CLI**
**Instalación:**
```bash
pip install google-images-search
```

### **Reverse Image Search**
**Instalación:**
```bash
git clone https://github.com/kitplummer/reverse-image-search.git
```

---

## 👤 Investigación de Personas

### **Pipl CLI**
**Instalación:**
```bash
pip install pipl-api
```

### **Spokeo CLI**
(API comercial - requiere suscripción)

### **TruePeopleSearch**
```bash
# Uso manual con curl
curl -s "https://www.truepeoplesearch.com/results?name=John%20Doe"
```

---

## 🔗 Análisis de Redes

### **Wireshark CLI (tshark)**
```bash
# Captura de tráfico
tshark -i eth0 -w capture.pcap

# Análisis de archivo
tshark -r capture.pcap -Y "http"

# Estadísticas
tshark -r capture.pcap -q -z conv,ip
```

### **Netstat**
```bash
# Conexiones activas
netstat -tulpn

# Tabla de routing
netstat -rn
```

### **ss**
```bash
# Socket statistics
ss -tulpn

# Conexiones TCP establecidas
ss -t state established
```

---

## 🤖 Herramientas de Automatización

### **Recon-ng**
**Instalación:**
```bash
git clone https://github.com/lanmaster53/recon-ng.git
cd recon-ng
pip3 install -r REQUIREMENTS
```

**Uso:**
```bash
# Iniciar framework
python3 recon-ng

# Comandos dentro del framework
[recon-ng][default] > marketplace install all
[recon-ng][default] > modules load recon/domains-hosts/hackertarget
[recon-ng][default] > options set SOURCE example.com
[recon-ng][default] > run
```

### **Spiderfoot**
**Instalación:**
```bash
git clone https://github.com/smicallef/spiderfoot.git
cd spiderfoot
pip3 install -r requirements.txt
```

**Uso:**
```bash
# Modo CLI
python3 sf.py -s example.com -t example.com

# Modo web
python3 sf.py -l 127.0.0.1:5001
```

### **OSRFRAMEWORK**
**Instalación:**
```bash
pip3 install osrframework
```

**Uso:**
```bash
# Búsqueda de usuarios
usufy.py -n username

# Búsqueda de dominios
domainfy.py -n example

# Búsqueda de emails
mailfy.py -n username
```

---

## 🏗️ Frameworks Completos

### **Maltego**
```bash
# Instalación en Kali Linux
apt-get update && apt-get install maltego
```

### **OSINT Framework**
```bash
git clone https://github.com/lockfale/OSINT-Framework.git
cd OSINT-Framework
# Abrir index.html en navegador
```

### **Shodan CLI**
**Instalación:**
```bash
pip install shodan
```

**Uso:**
```bash
# Configurar API key
shodan init YOUR_API_KEY

# Búsqueda básica
shodan search apache

# Información de host
shodan host 8.8.8.8

# Escaneo de red
shodan scan submit 198.20.70.114/24
```

### **Censys CLI**
**Instalación:**
```bash
pip install censys
```

**Uso:**
```bash
# Configurar credenciales
censys config

# Búsqueda de hosts
censys search "service.name: HTTP"

# Información de host específico
censys view 8.8.8.8
```

---

## 📦 Instalación Masiva

### Script de Instalación Automática

```bash
#!/bin/bash
# install_osint_tools.sh

echo "🔧 Instalando herramientas OSINT CLI..."

# Actualizar sistema
sudo apt-get update -y

# Herramientas básicas del sistema
sudo apt-get install -y git curl wget python3 python3-pip golang-go nodejs npm

# DNS Tools
sudo apt-get install -y dnsutils dnsrecon dnsenum fierce

# Network Tools
sudo apt-get install -y nmap masscan

# Python tools
pip3 install theHarvester h8mail holehe IP2Location shodan censys

# Go tools
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/tomnomnom/assetfinder@latest
go install github.com/OWASP/Amass/v3/...@latest
go install github.com/OJ/gobuster/v3@latest
go install github.com/ffuf/ffuf@latest
go install github.com/projectdiscovery/httpx/cmd/httpx@latest

# GitHub repositories
cd /opt
sudo git clone https://github.com/sherlock-project/sherlock.git
sudo git clone https://github.com/laramies/metagoofil.git
sudo git clone https://github.com/maurosoria/dirsearch.git
sudo git clone https://github.com/lanmaster53/recon-ng.git
sudo git clone https://github.com/smicallef/spiderfoot.git

echo "✅ Instalación completada!"
```

---

## 🔧 Configuración de APIs

### **APIs Recomendadas:**

1. **Shodan**: https://shodan.io
2. **Censys**: https://censys.io
3. **VirusTotal**: https://virustotal.com
4. **Hunter.io**: https://hunter.io
5. **SecurityTrails**: https://securitytrails.com
6. **Pipl**: https://pipl.com

### **Archivo de Configuración:**

```yaml
# ~/.config/osint/config.yaml
apis:
  shodan_key: "YOUR_SHODAN_API_KEY"
  censys_id: "YOUR_CENSYS_ID"
  censys_secret: "YOUR_CENSYS_SECRET"
  virustotal_key: "YOUR_VT_API_KEY"
  hunter_key: "YOUR_HUNTER_API_KEY"
  securitytrails_key: "YOUR_ST_API_KEY"
```

---

## 📚 Recursos Adicionales

### **Wordlists:**
- SecLists: https://github.com/danielmiessler/SecLists
- FuzzDB: https://github.com/fuzzdb-project/fuzzdb
- PayloadsAllTheThings: https://github.com/swisskyrepo/PayloadsAllTheThings

### **Documentación:**
- OSINT Framework: https://osintframework.com
- Awesome OSINT: https://github.com/jivoi/awesome-osint

---

**⚠️ Disclaimer:** Estas herramientas deben usarse únicamente con fines legítimos y éticos. Siempre obtenga autorización adecuada antes de realizar pruebas en sistemas que no sean de su propiedad.
