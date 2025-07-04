#!/usr/bin/env python3
"""
Módulo de funcionalidades OSINT avanzadas
Integra múltiples herramientas open source para investigación digital
"""

import asyncio
import json
import logging
import subprocess
import re
import socket
import ssl
import hashlib
import base64
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup
import dns.resolver
import whois
import ipwhois
try:
    import nmap
except ImportError:
    nmap = None
try:
    import paramiko
except ImportError:
    paramiko = None
import phonenumbers
from phonenumbers import geocoder, carrier
import yfinance
from geopy.geocoders import Nominatim
import builtwith
import waybackpy
import tldextract
import vt
import shodan
import censys
import threading
import time
import os
import concurrent.futures
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SubdomainEnumerator:
    """Enumerador de subdominios usando múltiples técnicas"""
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.found_subdomains = set()
        
    def enumerate_subdomains(self, domain: str) -> List[Dict[str, Any]]:
        """Enumera subdominios usando múltiples técnicas"""
        results = []
        
        # Técnica 1: Sublist3r simulado (brute force con wordlist)
        logger.info(f"Buscando subdominios para {domain}")
        
        # Wordlist común de subdominios
        common_subdomains = [
            'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk',
            'ns2', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'api', 'admin', 'mobile',
            'dev', 'test', 'staging', 'beta', 'app', 'blog', 'support', 'forum', 'store',
            'shop', 'secure', 'vpn', 'cdn', 'static', 'assets', 'images', 'media', 'docs',
            'help', 'portal', 'login', 'dashboard', 'control', 'panel', 'news', 'events',
            'calendar', 'wiki', 'git', 'svn', 'backup', 'old', 'new', 'temp', 'demo',
            'development', 'production', 'staging', 'sandbox', 'cloud', 'web', 'server',
            'host', 'files', 'downloads', 'uploads', 'share', 'public', 'private', 'internal'
        ]
        
        def check_subdomain(subdomain: str) -> Optional[Dict[str, Any]]:
            """Verifica si un subdominio existe"""
            try:
                full_domain = f"{subdomain}.{domain}"
                ip = socket.gethostbyname(full_domain)
                
                # Verificar si es accesible vía HTTP/HTTPS
                urls_to_test = [f"http://{full_domain}", f"https://{full_domain}"]
                for url in urls_to_test:
                    try:
                        response = requests.get(url, timeout=5, verify=False)
                        if response.status_code == 200:
                            return {
                                'subdomain': full_domain,
                                'ip': ip,
                                'status': 'active',
                                'protocol': 'https' if url.startswith('https') else 'http',
                                'status_code': response.status_code,
                                'title': self._extract_title(response.text),
                                'server': response.headers.get('Server', ''),
                                'technology': self._detect_technology(response.text, dict(response.headers))
                            }
                    except:
                        continue
                
                return {
                    'subdomain': full_domain,
                    'ip': ip,
                    'status': 'exists',
                    'protocol': 'unknown'
                }
            except:
                return None
        
        # Usar ThreadPoolExecutor para paralelizar las verificaciones
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(check_subdomain, sub) for sub in common_subdomains]
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)
        
        # Técnica 2: Búsqueda en Certificate Transparency Logs
        ct_results = self._search_certificate_transparency(domain)
        results.extend(ct_results)
        
        # Técnica 3: Búsqueda en motores de búsqueda
        search_results = self._search_engines_subdomains(domain)
        results.extend(search_results)
        
        return results
    
    def _extract_title(self, html: str) -> str:
        """Extrae el título de una página HTML"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.find('title')
            return title.text.strip() if title else ''
        except:
            return ''
    
    def _detect_technology(self, html: str, headers: Dict[str, str]) -> List[str]:
        """Detecta tecnologías usadas en el sitio web"""
        technologies = []
        
        # Detectar por headers
        server = headers.get('Server', '').lower()
        if 'nginx' in server:
            technologies.append('Nginx')
        elif 'apache' in server:
            technologies.append('Apache')
        elif 'cloudflare' in server:
            technologies.append('Cloudflare')
        
        # Detectar por contenido HTML
        html_lower = html.lower()
        if 'wordpress' in html_lower or 'wp-content' in html_lower:
            technologies.append('WordPress')
        elif 'drupal' in html_lower:
            technologies.append('Drupal')
        elif 'joomla' in html_lower:
            technologies.append('Joomla')
        elif 'react' in html_lower:
            technologies.append('React')
        elif 'vue' in html_lower:
            technologies.append('Vue.js')
        elif 'angular' in html_lower:
            technologies.append('Angular')
        
        return technologies
    
    def _search_certificate_transparency(self, domain: str) -> List[Dict[str, Any]]:
        """Busca subdominios en Certificate Transparency logs"""
        results = []
        try:
            # Usar crt.sh API
            url = f"https://crt.sh/?q=%.{domain}&output=json"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                subdomains = set()
                
                for cert in data:
                    names = cert.get('name_value', '').split('\n')
                    for name in names:
                        if name.endswith(f'.{domain}') and name != domain:
                            subdomains.add(name)
                
                for subdomain in subdomains:
                    try:
                        ip = socket.gethostbyname(subdomain)
                        results.append({
                            'subdomain': subdomain,
                            'ip': ip,
                            'status': 'found_in_ct',
                            'source': 'certificate_transparency'
                        })
                    except:
                        results.append({
                            'subdomain': subdomain,
                            'ip': 'N/A',
                            'status': 'found_in_ct',
                            'source': 'certificate_transparency'
                        })
        except Exception as e:
            logger.error(f"Error buscando en CT logs: {e}")
        
        return results
    
    def _search_engines_subdomains(self, domain: str) -> List[Dict[str, Any]]:
        """Busca subdominios usando motores de búsqueda"""
        results = []
        
        # Google dorking para subdominios
        dorks = [
            f"site:*.{domain}",
            f"site:{domain} -www",
            f"inurl:{domain}"
        ]
        
        for dork in dorks:
            try:
                url = "https://www.google.com/search"
                params = {'q': dork, 'num': 20}
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                response = requests.get(url, params=params, headers=headers, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extraer URLs de los resultados
                for link in soup.find_all('a', href=True):
                    try:
                        href = getattr(link, 'attrs', {}).get('href', '')
                        if href and isinstance(href, str) and 'url?q=' in href:
                            actual_url = href.split('url?q=')[1].split('&')[0]
                            parsed = urlparse(actual_url)
                            if parsed.netloc.endswith(f'.{domain}'):
                                results.append({
                                    'subdomain': parsed.netloc,
                                    'ip': 'N/A',
                                    'status': 'found_in_search',
                                    'source': 'google_search',
                                    'url': actual_url
                                })
                    except (AttributeError, IndexError, TypeError):
                        continue
                        continue
            except Exception as e:
                logger.error(f"Error en búsqueda de motor: {e}")
        
        return results

class NetworkScanner:
    """Scanner de red usando nmap y otras herramientas"""
    
    def __init__(self):
        if nmap:
            self.nm = nmap.PortScanner()
        else:
            self.nm = None
    
    def scan_host(self, host: str, ports: str = "1-1000") -> Dict[str, Any]:
        """Escanea un host específico"""
        if not self.nm:
            return {'host': host, 'error': 'nmap no está disponible'}
        
        try:
            logger.info(f"Escaneando host: {host}")
            
            # Realizar escaneo
            self.nm.scan(host, ports, arguments='-sV -sS -O --script vuln')
            
            results = {
                'host': host,
                'scan_time': datetime.now().isoformat(),
                'state': 'unknown',
                'ports': [],
                'os': [],
                'hostnames': [],
                'vulnerabilities': []
            }
            
            if host in self.nm.all_hosts():
                host_info = self.nm[host]
                results['state'] = host_info.state()
                
                # Información de puertos
                for protocol in host_info.all_protocols():
                    ports = host_info[protocol].keys()
                    for port in ports:
                        port_info = host_info[protocol][port]
                        results['ports'].append({
                            'port': port,
                            'protocol': protocol,
                            'state': port_info['state'],
                            'service': port_info.get('name', ''),
                            'version': port_info.get('version', ''),
                            'product': port_info.get('product', '')
                        })
                
                # Información del OS
                if 'osmatch' in host_info:
                    for os_match in host_info['osmatch']:
                        results['os'].append({
                            'name': os_match['name'],
                            'accuracy': os_match['accuracy']
                        })
                
                # Hostnames
                if 'hostnames' in host_info:
                    for hostname in host_info['hostnames']:
                        results['hostnames'].append(hostname)
                
                # Scripts de vulnerabilidades
                for port in results['ports']:
                    if 'script' in host_info[port['protocol']][port['port']]:
                        scripts = host_info[port['protocol']][port['port']]['script']
                        for script_name, script_output in scripts.items():
                            if 'vuln' in script_name.lower():
                                results['vulnerabilities'].append({
                                    'port': port['port'],
                                    'script': script_name,
                                    'output': script_output
                                })
            
            return results
        
        except Exception as e:
            logger.error(f"Error escaneando host {host}: {e}")
            return {'host': host, 'error': str(e)}
    
    def scan_network(self, network: str) -> List[Dict[str, Any]]:
        """Escanea una red completa"""
        if not self.nm:
            return [{'error': 'nmap no está disponible'}]
        
        try:
            logger.info(f"Escaneando red: {network}")
            
            # Descubrimiento de hosts
            self.nm.scan(hosts=network, arguments='-sn')
            
            results = []
            for host in self.nm.all_hosts():
                host_info = {
                    'ip': host,
                    'hostname': self.nm[host].hostname(),
                    'state': self.nm[host].state(),
                    'mac': self.nm[host]['addresses'].get('mac', ''),
                    'vendor': self.nm[host]['vendor'].get(self.nm[host]['addresses'].get('mac', ''), '')
                }
                results.append(host_info)
            
            return results
        
        except Exception as e:
            logger.error(f"Error escaneando red {network}: {e}")
            return []

class SocialMediaInvestigator:
    """Investigador de redes sociales"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def search_username(self, username: str) -> Dict[str, Any]:
        """Busca un username en múltiples plataformas"""
        platforms = {
            'github': f'https://github.com/{username}',
            'twitter': f'https://twitter.com/{username}',
            'instagram': f'https://instagram.com/{username}',
            'linkedin': f'https://linkedin.com/in/{username}',
            'facebook': f'https://facebook.com/{username}',
            'youtube': f'https://youtube.com/@{username}',
            'tiktok': f'https://tiktok.com/@{username}',
            'reddit': f'https://reddit.com/user/{username}',
            'pinterest': f'https://pinterest.com/{username}',
            'tumblr': f'https://{username}.tumblr.com',
            'medium': f'https://medium.com/@{username}',
            'telegram': f'https://t.me/{username}',
            'discord': f'https://discord.com/users/{username}',
            'twitch': f'https://twitch.tv/{username}',
            'devto': f'https://dev.to/{username}',
            'behance': f'https://behance.net/{username}',
            'dribbble': f'https://dribbble.com/{username}',
            'stackoverflow': f'https://stackoverflow.com/users/{username}',
            'soundcloud': f'https://soundcloud.com/{username}',
            'spotify': f'https://open.spotify.com/user/{username}'
        }
        
        results = {
            'username': username,
            'found_profiles': [],
            'not_found': [],
            'errors': []
        }
        
        def check_platform(platform: str, url: str) -> Optional[Dict[str, Any]]:
            """Verifica si el usuario existe en una plataforma"""
            try:
                response = self.session.get(url, timeout=10, allow_redirects=True)
                
                if response.status_code == 200:
                    # Verificaciones adicionales para evitar falsos positivos
                    content = response.text.lower()
                    
                    # Patrones que indican que el perfil no existe
                    not_found_patterns = [
                        'user not found',
                        'page not found',
                        'profile not found',
                        'account not found',
                        'this account doesn\'t exist',
                        'usuario no encontrado',
                        'perfil no encontrado'
                    ]
                    
                    if any(pattern in content for pattern in not_found_patterns):
                        return None
                    
                    # Extraer información adicional
                    soup = BeautifulSoup(response.text, 'html.parser')
                    title = soup.find('title')
                    title_text = title.text.strip() if title else ''
                    
                    # Buscar información del perfil
                    profile_info = {
                        'platform': platform,
                        'url': url,
                        'title': title_text,
                        'status_code': response.status_code,
                        'found_at': datetime.now().isoformat()
                    }
                    
                    # Extraer información específica por plataforma
                    if platform == 'github':
                        profile_info.update(self._extract_github_info(soup))
                    elif platform == 'linkedin':
                        profile_info.update(self._extract_linkedin_info(soup))
                    elif platform == 'twitter':
                        profile_info.update(self._extract_twitter_info(soup))
                    
                    return profile_info
                
                return None
            
            except Exception as e:
                return {'platform': platform, 'error': str(e)}
        
        # Usar ThreadPoolExecutor para paralelizar las verificaciones
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(check_platform, platform, url) 
                      for platform, url in platforms.items()]
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    if 'error' in result:
                        results['errors'].append(result)
                    else:
                        results['found_profiles'].append(result)
        
        return results
    
    def _extract_github_info(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extrae información específica de GitHub"""
        info = {}
        
        # Nombre real
        name_elem = soup.find('span', {'itemprop': 'name'})
        if name_elem:
            info['real_name'] = name_elem.text.strip()
        
        # Bio
        bio_elem = soup.find('div', {'class': 'user-profile-bio'})
        if bio_elem:
            info['bio'] = bio_elem.text.strip()
        
        # Repositorios
        repos_elem = soup.find('span', {'class': 'Counter'})
        if repos_elem:
            info['repositories'] = repos_elem.text.strip()
        
        return info
    
    def _extract_linkedin_info(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extrae información específica de LinkedIn"""
        info = {}
        
        # Título profesional
        title_elem = soup.find('h2', {'class': 'top-card-layout__headline'})
        if title_elem:
            info['professional_title'] = title_elem.text.strip()
        
        return info
    
    def _extract_twitter_info(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extrae información específica de Twitter"""
        info = {}
        
        # Descripción
        desc_elem = soup.find('div', {'data-testid': 'UserDescription'})
        if desc_elem:
            info['description'] = desc_elem.text.strip()
        
        return info

class PhoneNumberAnalyzer:
    """Analizador de números telefónicos"""
    
    def analyze_phone(self, phone_number: str) -> Dict[str, Any]:
        """Analiza un número telefónico"""
        try:
            # Parsear el número
            parsed = phonenumbers.parse(phone_number, None)
            
            if not phonenumbers.is_valid_number(parsed):
                return {'error': 'Número telefónico inválido'}
            
            # Información básica
            info = {
                'number': phone_number,
                'formatted': phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                'country_code': parsed.country_code,
                'national_number': parsed.national_number,
                'is_valid': True,
                'number_type': phonenumbers.number_type(parsed)
            }
            
            # Geolocalización
            location = geocoder.description_for_number(parsed, 'es')
            if location:
                info['location'] = location
            
            # Operador
            carrier_name = carrier.name_for_number(parsed, 'es')
            if carrier_name:
                info['carrier'] = carrier_name
            
            # Zona horaria - importar el módulo específico
            try:
                from phonenumbers import timezone
                timezones = timezone.time_zones_for_number(parsed)
                if timezones:
                    info['timezones'] = list(timezones)
            except ImportError:
                info['timezones'] = []
            
            return info
        
        except Exception as e:
            return {'error': str(e)}

class WebArchiveSearcher:
    """Buscador en archivos web (Wayback Machine)"""
    
    def __init__(self):
        self.session = requests.Session()
    
    def search_wayback(self, url: str) -> Dict[str, Any]:
        """Busca URL en Wayback Machine"""
        try:
            wayback = waybackpy.Url(url)
            
            # Obtener información general
            info = {
                'url': url,
                'first_archive': None,
                'last_archive': None,
                'total_archives': 0,
                'snapshots': []
            }
            
            # Obtener el primer y último snapshot
            try:
                oldest = wayback.oldest()
                info['first_archive'] = {
                    'timestamp': oldest.timestamp,
                    'archive_url': oldest.archive_url
                }
            except:
                pass
            
            try:
                newest = wayback.newest()
                info['last_archive'] = {
                    'timestamp': newest.timestamp,
                    'archive_url': newest.archive_url
                }
            except:
                pass
            
            # Obtener snapshots por año
            try:
                # Wayback Machine CDX API para obtener snapshots
                cdx_url = f"https://web.archive.org/cdx/search/cdx?url={url}&output=json&limit=50"
                response = requests.get(cdx_url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if len(data) > 1:  # Primera línea son headers
                        for row in data[1:]:
                            if len(row) >= 3:
                                timestamp = row[1]
                                archive_url = f"https://web.archive.org/web/{timestamp}/{url}"
                                info['snapshots'].append({
                                    'timestamp': timestamp,
                                    'archive_url': archive_url,
                                    'status_code': row[4] if len(row) > 4 else None
                                })
                
                info['total_archives'] = len(info['snapshots'])
            except Exception as e:
                logger.error(f"Error obteniendo snapshots: {e}")
            
            return info
        
        except Exception as e:
            return {'error': str(e)}

class TechnologyDetector:
    """Detector de tecnologías web"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def detect_technologies(self, url: str) -> Dict[str, Any]:
        """Detecta tecnologías usadas en un sitio web"""
        try:
            # Usar builtwith si está disponible
            try:
                technologies = builtwith.parse(url)
                return {
                    'url': url,
                    'technologies': technologies,
                    'source': 'builtwith'
                }
            except:
                pass
            
            # Análisis manual si builtwith no está disponible
            response = self.session.get(url, timeout=10)
            
            technologies = {
                'web_servers': [],
                'programming_languages': [],
                'javascript_frameworks': [],
                'cms': [],
                'analytics': [],
                'cdn': [],
                'other': []
            }
            
            # Análisis de headers
            headers = response.headers
            
            # Servidor web
            server = headers.get('Server', '').lower()
            if 'nginx' in server:
                technologies['web_servers'].append('Nginx')
            elif 'apache' in server:
                technologies['web_servers'].append('Apache')
            elif 'microsoft-iis' in server:
                technologies['web_servers'].append('IIS')
            
            # CDN
            if 'cloudflare' in server:
                technologies['cdn'].append('Cloudflare')
            
            # Análisis de contenido
            content = response.text.lower()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # CMS
            if 'wp-content' in content or 'wordpress' in content:
                technologies['cms'].append('WordPress')
            elif 'drupal' in content:
                technologies['cms'].append('Drupal')
            elif 'joomla' in content:
                technologies['cms'].append('Joomla')
            
            # Frameworks JavaScript
            if 'react' in content:
                technologies['javascript_frameworks'].append('React')
            if 'vue' in content:
                technologies['javascript_frameworks'].append('Vue.js')
            if 'angular' in content:
                technologies['javascript_frameworks'].append('Angular')
            if 'jquery' in content:
                technologies['javascript_frameworks'].append('jQuery')
            
            # Analytics
            if 'google-analytics' in content or 'gtag' in content:
                technologies['analytics'].append('Google Analytics')
            if 'facebook' in content and 'pixel' in content:
                technologies['analytics'].append('Facebook Pixel')
            
            # Meta tags
            for meta in soup.find_all('meta'):
                try:
                    attrs = getattr(meta, 'attrs', {})
                    name_attr = attrs.get('name', '')
                    content_attr = attrs.get('content', '')
                    
                    # Safely convert to string and then to lowercase
                    name = str(name_attr).lower() if name_attr else ''
                    content = str(content_attr).lower() if content_attr else ''
                    
                    if 'generator' in name:
                        technologies['other'].append(f"Generator: {content}")
                except (AttributeError, TypeError):
                    continue
            
            return {
                'url': url,
                'technologies': technologies,
                'source': 'manual_analysis'
            }
        
        except Exception as e:
            return {'error': str(e)}

class CompanyInvestigator:
    """Investigador de información corporativa"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def investigate_company(self, company_name: str) -> Dict[str, Any]:
        """Investiga información sobre una empresa"""
        results = {
            'company_name': company_name,
            'financial_data': {},
            'news': [],
            'social_media': [],
            'web_presence': [],
            'employees': [],
            'technologies': []
        }
        
        # Búsqueda de datos financieros (si es empresa pública)
        try:
            ticker_symbols = self._guess_ticker_symbols(company_name)
            for ticker in ticker_symbols:
                try:
                    stock = yfinance.Ticker(ticker)
                    info = stock.info
                    if info:
                        results['financial_data'][ticker] = {
                            'name': info.get('longName', ''),
                            'sector': info.get('sector', ''),
                            'industry': info.get('industry', ''),
                            'market_cap': info.get('marketCap', 0),
                            'employees': info.get('fullTimeEmployees', 0),
                            'website': info.get('website', ''),
                            'description': info.get('longBusinessSummary', '')
                        }
                except:
                    continue
        except:
            pass
        
        # Búsqueda de noticias
        try:
            news_results = self._search_news(company_name)
            results['news'] = news_results
        except:
            pass
        
        # Búsqueda de presencia web
        try:
            web_results = self._search_web_presence(company_name)
            results['web_presence'] = web_results
        except:
            pass
        
        return results
    
    def _guess_ticker_symbols(self, company_name: str) -> List[str]:
        """Intenta adivinar símbolos bursátiles"""
        # Simplificación del nombre de la empresa
        clean_name = re.sub(r'[^\w\s]', '', company_name.lower())
        words = clean_name.split()
        
        # Generar posibles símbolos
        symbols = []
        
        # Primeras letras de cada palabra
        if len(words) >= 2:
            symbols.append(''.join(word[0] for word in words).upper())
        
        # Nombre completo abreviado
        if len(words) == 1:
            symbols.append(words[0][:4].upper())
        
        # Combinaciones comunes
        for word in words:
            if len(word) >= 3:
                symbols.append(word[:3].upper())
                symbols.append(word[:4].upper())
        
        return symbols[:5]  # Limitar a 5 intentos
    
    def _search_news(self, company_name: str) -> List[Dict[str, Any]]:
        """Busca noticias sobre la empresa"""
        news_results = []
        
        try:
            # Usar Google News
            search_url = "https://news.google.com/search"
            params = {
                'q': company_name,
                'hl': 'es',
                'gl': 'ES',
                'ceid': 'ES:es'
            }
            
            response = self.session.get(search_url, params=params, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extraer noticias usando parsing de texto simple
            content = response.text
            
            # Usar expresiones regulares para extraer información básica
            import re
            
            # Buscar patrones de títulos comunes
            title_patterns = [
                r'<h3[^>]*>([^<]+)</h3>',
                r'<h4[^>]*>([^<]+)</h4>',
                r'<h2[^>]*>([^<]+)</h2>'
            ]
            
            for pattern in title_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches[:10]:
                    title = re.sub(r'<[^>]+>', '', match).strip()
                    if title and len(title) > 10:
                        news_results.append({
                            'title': title,
                            'link': '',
                            'source': 'google_news'
                        })
                        if len(news_results) >= 10:
                            break
                if len(news_results) >= 10:
                    break
                    continue
        except:
            pass
        
        return news_results
    
    def _search_web_presence(self, company_name: str) -> List[Dict[str, Any]]:
        """Busca presencia web de la empresa"""
        web_results = []
        
        # Patrones comunes de dominios
        domain_patterns = [
            company_name.replace(' ', '').lower(),
            company_name.replace(' ', '-').lower(),
            company_name.replace(' ', '_').lower(),
            ''.join(word[0] for word in company_name.split()).lower()
        ]
        
        extensions = ['.com', '.es', '.net', '.org', '.co']
        
        for pattern in domain_patterns:
            for ext in extensions:
                domain = f"{pattern}{ext}"
                try:
                    response = self.session.get(f"http://{domain}", timeout=5)
                    if response.status_code == 200:
                        web_results.append({
                            'domain': domain,
                            'status': 'active',
                            'title': self._extract_title(response.text)
                        })
                except:
                    continue
        
        return web_results
    
    def _extract_title(self, html: str) -> str:
        """Extrae el título de una página"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.find('title')
            return title.text.strip() if title else ''
        except:
            return ''

class AdvancedOSINTToolkit:
    """Toolkit principal que integra todas las herramientas OSINT"""
    
    def __init__(self):
        self.subdomain_enum = SubdomainEnumerator()
        self.network_scanner = NetworkScanner()
        self.social_investigator = SocialMediaInvestigator()
        self.phone_analyzer = PhoneNumberAnalyzer()
        self.web_archive = WebArchiveSearcher()
        self.tech_detector = TechnologyDetector()
        self.company_investigator = CompanyInvestigator()
        
        # Geolocalizador
        self.geolocator = Nominatim(user_agent="osint_toolkit")
    
    def comprehensive_domain_analysis(self, domain: str) -> Dict[str, Any]:
        """Análisis completo de dominio"""
        logger.info(f"Iniciando análisis completo del dominio: {domain}")
        
        analysis = {
            'domain': domain,
            'timestamp': datetime.now().isoformat(),
            'subdomains': [],
            'whois_info': {},
            'dns_records': {},
            'web_technologies': {},
            'wayback_data': {},
            'ssl_info': {},
            'network_scan': {}
        }
        
        try:
            # Enumeración de subdominios
            analysis['subdomains'] = self.subdomain_enum.enumerate_subdomains(domain)
        except Exception as e:
            logger.error(f"Error en enumeración de subdominios: {e}")
        
        try:
            # Información WHOIS
            w = whois.whois(domain)
            analysis['whois_info'] = {
                'registrar': w.registrar,
                'creation_date': str(w.creation_date) if w.creation_date else None,
                'expiration_date': str(w.expiration_date) if w.expiration_date else None,
                'name_servers': w.name_servers,
                'organization': w.org,
                'country': w.country
            }
        except Exception as e:
            logger.error(f"Error obteniendo WHOIS: {e}")
        
        try:
            # Registros DNS
            analysis['dns_records'] = self._get_dns_records(domain)
        except Exception as e:
            logger.error(f"Error obteniendo DNS: {e}")
        
        try:
            # Detección de tecnologías
            analysis['web_technologies'] = self.tech_detector.detect_technologies(f"https://{domain}")
        except Exception as e:
            logger.error(f"Error detectando tecnologías: {e}")
        
        try:
            # Datos de Wayback Machine
            analysis['wayback_data'] = self.web_archive.search_wayback(f"https://{domain}")
        except Exception as e:
            logger.error(f"Error buscando en Wayback: {e}")
        
        try:
            # Información SSL
            analysis['ssl_info'] = self._get_ssl_info(domain)
        except Exception as e:
            logger.error(f"Error obteniendo SSL: {e}")
        
        return analysis
    
    def _get_dns_records(self, domain: str) -> Dict[str, Any]:
        """Obtiene registros DNS"""
        records = {}
        
        record_types = ['A', 'AAAA', 'MX', 'TXT', 'NS', 'CNAME', 'SOA']
        
        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                records[record_type] = [str(rdata) for rdata in answers]
            except:
                records[record_type] = []
        
        return records
    
    def _get_ssl_info(self, domain: str) -> Dict[str, Any]:
        """Obtiene información SSL"""
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    if cert:
                        result = {}
                        
                        # Subject
                        if 'subject' in cert and cert['subject']:
                            subject_dict = {}
                            for x in cert['subject']:
                                if len(x) >= 2:
                                    subject_dict[x[0][0]] = x[0][1]
                            result['subject'] = subject_dict
                        
                        # Issuer
                        if 'issuer' in cert and cert['issuer']:
                            issuer_dict = {}
                            for x in cert['issuer']:
                                if len(x) >= 2:
                                    issuer_dict[x[0][0]] = x[0][1]
                            result['issuer'] = issuer_dict
                        
                        # Otros campos
                        result['version'] = cert.get('version', '')
                        result['not_before'] = cert.get('notBefore', '')
                        result['not_after'] = cert.get('notAfter', '')
                        result['serial_number'] = cert.get('serialNumber', '')
                        
                        # Subject Alt Names
                        san_list = cert.get('subjectAltName', [])
                        if san_list:
                            result['subject_alt_names'] = [x[1] for x in san_list if len(x) >= 2]
                        else:
                            result['subject_alt_names'] = []
                        
                        return result
                    else:
                        return {'error': 'No se pudo obtener el certificado'}
        except Exception as e:
            return {'error': str(e)}
    
    def ip_geolocation(self, ip: str) -> Dict[str, Any]:
        """Geolocalización de IP"""
        try:
            obj = ipwhois.IPWhois(ip)
            results = obj.lookup_rdap()
            
            geo_info = {
                'ip': ip,
                'country': results.get('asn_country_code', ''),
                'description': results.get('asn_description', ''),
                'cidr': results.get('asn_cidr', ''),
                'registry': results.get('asn_registry', ''),
                'network': results.get('network', {}),
                'raw_data': results
            }
            
            return geo_info
        except Exception as e:
            return {'error': str(e)}
    
    def username_investigation(self, username: str) -> Dict[str, Any]:
        """Investigación completa de username"""
        logger.info(f"Investigando username: {username}")
        
        return self.social_investigator.search_username(username)
    
    def phone_investigation(self, phone: str) -> Dict[str, Any]:
        """Investigación de número telefónico"""
        logger.info(f"Investigando número: {phone}")
        
        return self.phone_analyzer.analyze_phone(phone)
    
    def email_investigation(self, email: str) -> Dict[str, Any]:
        """Investigación de email"""
        logger.info(f"Investigando email: {email}")
        
        results = {
            'email': email,
            'domain_info': {},
            'breach_check': {},
            'social_media': {}
        }
        
        # Extraer dominio
        domain = email.split('@')[1] if '@' in email else ''
        
        if domain:
            # Analizar dominio
            results['domain_info'] = self.comprehensive_domain_analysis(domain)
            
            # Buscar el username en redes sociales
            username = email.split('@')[0]
            results['social_media'] = self.social_investigator.search_username(username)
        
        return results
    
    def company_investigation(self, company: str) -> Dict[str, Any]:
        """Investigación completa de empresa"""
        logger.info(f"Investigando empresa: {company}")
        
        return self.company_investigator.investigate_company(company)
