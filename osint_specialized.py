#!/usr/bin/env python3
"""
Herramientas OSINT especializadas para casos específicos
"""

import requests
import json
import hashlib
import base64
import re
import time
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import concurrent.futures
import subprocess
import os
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class LeakChecker:
    """Verificador de filtraciones de datos"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def check_email_breaches(self, email: str) -> Dict[str, Any]:
        """Verifica si un email aparece en filtraciones conocidas"""
        results = {
            'email': email,
            'breaches': [],
            'paste_sites': [],
            'total_breaches': 0
        }
        
        # Simular verificación con servicios públicos
        try:
            # HaveIBeenPwned API (requiere API key para uso completo)
            # Usando la versión gratuita sin API key
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
            
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                breaches = response.json()
                for breach in breaches:
                    results['breaches'].append({
                        'name': breach.get('Name', ''),
                        'title': breach.get('Title', ''),
                        'breach_date': breach.get('BreachDate', ''),
                        'data_classes': breach.get('DataClasses', []),
                        'verified': breach.get('IsVerified', False)
                    })
                results['total_breaches'] = len(breaches)
            
        except Exception as e:
            logger.error(f"Error verificando filtraciones: {e}")
        
        return results
    
    def check_domain_reputation(self, domain: str) -> Dict[str, Any]:
        """Verifica la reputación de un dominio"""
        results = {
            'domain': domain,
            'safe_browsing': {},
            'malware_detected': False,
            'phishing_detected': False,
            'reputation_score': 0
        }
        
        try:
            # Verificar con Google Safe Browsing (requiere API key)
            # Simulamos la verificación
            results['safe_browsing'] = {
                'status': 'unknown',
                'last_check': datetime.now().isoformat()
            }
            
            # Verificar con VirusTotal (requiere API key)
            # Simulamos la verificación
            results['virustotal'] = {
                'status': 'unknown',
                'last_check': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error verificando reputación: {e}")
        
        return results

class PastebinSearcher:
    """Buscador en sitios de pastebin"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Sitios de pastebin conocidos
        self.pastebin_sites = [
            'https://pastebin.com',
            'https://paste.ee',
            'https://justpaste.it',
            'https://dpaste.com',
            'https://controlc.com',
            'https://ideone.com',
            'https://codepad.org',
            'https://ghostbin.com'
        ]
    
    def search_pastes(self, query: str) -> List[Dict[str, Any]]:
        """Busca en múltiples sitios de pastebin"""
        results = []
        
        # Búsqueda en Google con site: operators
        search_queries = [
            f'site:pastebin.com "{query}"',
            f'site:paste.ee "{query}"',
            f'site:justpaste.it "{query}"',
            f'site:dpaste.com "{query}"'
        ]
        
        for search_query in search_queries:
            try:
                google_results = self._search_google(search_query)
                results.extend(google_results)
            except Exception as e:
                logger.error(f"Error buscando en Google: {e}")
        
        return results
    
    def _search_google(self, query: str) -> List[Dict[str, Any]]:
        """Busca en Google con query específico"""
        results = []
        
        try:
            url = "https://www.google.com/search"
            params = {
                'q': query,
                'num': 10,
                'hl': 'es'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extraer resultados usando parsing de texto
            import re
            
            # Buscar patrones de títulos y enlaces
            title_pattern = r'<h3[^>]*>([^<]+)</h3>'
            link_pattern = r'<a[^>]+href="([^"]+)"'
            
            titles = re.findall(title_pattern, response.text, re.IGNORECASE)
            links = re.findall(link_pattern, response.text, re.IGNORECASE)
            
            # Combinar títulos y enlaces
            for i, title in enumerate(titles[:10]):
                title_clean = re.sub(r'<[^>]+>', '', title).strip()
                link = links[i] if i < len(links) else ''
                
                # Limpiar enlace de Google
                if '/url?q=' in link:
                    link = link.split('/url?q=')[1].split('&')[0]
                
                if title_clean and len(title_clean) > 5:
                    results.append({
                        'title': title_clean,
                        'url': link,
                        'source': 'google_search',
                        'query': query
                    })
        
        except Exception as e:
            logger.error(f"Error en búsqueda Google: {e}")
        
        return results

class GitHubInvestigator:
    """Investigador de GitHub"""
    
    def __init__(self, github_token: Optional[str] = None):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        if github_token:
            self.session.headers['Authorization'] = f'token {github_token}'
    
    def investigate_user(self, username: str) -> Dict[str, Any]:
        """Investiga un usuario de GitHub"""
        results = {
            'username': username,
            'profile': {},
            'repositories': [],
            'organizations': [],
            'activity': [],
            'emails': [],
            'ssh_keys': []
        }
        
        try:
            # Información del perfil
            profile_url = f"https://api.github.com/users/{username}"
            response = self.session.get(profile_url, timeout=10)
            
            if response.status_code == 200:
                profile = response.json()
                results['profile'] = {
                    'name': profile.get('name', ''),
                    'bio': profile.get('bio', ''),
                    'location': profile.get('location', ''),
                    'email': profile.get('email', ''),
                    'company': profile.get('company', ''),
                    'blog': profile.get('blog', ''),
                    'twitter': profile.get('twitter_username', ''),
                    'public_repos': profile.get('public_repos', 0),
                    'followers': profile.get('followers', 0),
                    'following': profile.get('following', 0),
                    'created_at': profile.get('created_at', ''),
                    'updated_at': profile.get('updated_at', '')
                }
        except Exception as e:
            logger.error(f"Error obteniendo perfil: {e}")
        
        try:
            # Repositorios
            repos_url = f"https://api.github.com/users/{username}/repos"
            response = self.session.get(repos_url, timeout=10)
            
            if response.status_code == 200:
                repos = response.json()
                for repo in repos[:20]:  # Limitar a 20 repos
                    results['repositories'].append({
                        'name': repo.get('name', ''),
                        'description': repo.get('description', ''),
                        'language': repo.get('language', ''),
                        'stars': repo.get('stargazers_count', 0),
                        'forks': repo.get('forks_count', 0),
                        'created_at': repo.get('created_at', ''),
                        'updated_at': repo.get('updated_at', ''),
                        'clone_url': repo.get('clone_url', ''),
                        'html_url': repo.get('html_url', '')
                    })
        except Exception as e:
            logger.error(f"Error obteniendo repositorios: {e}")
        
        try:
            # Organizaciones
            orgs_url = f"https://api.github.com/users/{username}/orgs"
            response = self.session.get(orgs_url, timeout=10)
            
            if response.status_code == 200:
                orgs = response.json()
                for org in orgs:
                    results['organizations'].append({
                        'name': org.get('login', ''),
                        'description': org.get('description', ''),
                        'url': org.get('html_url', '')
                    })
        except Exception as e:
            logger.error(f"Error obteniendo organizaciones: {e}")
        
        try:
            # Buscar emails en commits
            results['emails'] = self._extract_emails_from_commits(username)
        except Exception as e:
            logger.error(f"Error extrayendo emails: {e}")
        
        return results
    
    def _extract_emails_from_commits(self, username: str) -> List[str]:
        """Extrae emails de commits públicos"""
        emails = set()
        
        try:
            # Obtener eventos públicos
            events_url = f"https://api.github.com/users/{username}/events/public"
            response = self.session.get(events_url, timeout=10)
            
            if response.status_code == 200:
                events = response.json()
                for event in events:
                    if event.get('type') == 'PushEvent':
                        commits = event.get('payload', {}).get('commits', [])
                        for commit in commits:
                            author = commit.get('author', {})
                            email = author.get('email', '')
                            if email and '@' in email:
                                emails.add(email)
        except Exception as e:
            logger.error(f"Error extrayendo emails: {e}")
        
        return list(emails)
    
    def search_code(self, query: str) -> List[Dict[str, Any]]:
        """Busca código en GitHub"""
        results = []
        
        try:
            search_url = "https://api.github.com/search/code"
            params = {
                'q': query,
                'per_page': 30
            }
            
            response = self.session.get(search_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                items = data.get('items', [])
                
                for item in items:
                    results.append({
                        'name': item.get('name', ''),
                        'path': item.get('path', ''),
                        'sha': item.get('sha', ''),
                        'url': item.get('html_url', ''),
                        'repository': item.get('repository', {}).get('full_name', ''),
                        'score': item.get('score', 0)
                    })
        except Exception as e:
            logger.error(f"Error buscando código: {e}")
        
        return results

class CertificateAnalyzer:
    """Analizador de certificados SSL/TLS"""
    
    def __init__(self):
        self.session = requests.Session()
    
    def analyze_certificate(self, domain: str) -> Dict[str, Any]:
        """Analiza el certificado SSL de un dominio"""
        results = {
            'domain': domain,
            'certificate_info': {},
            'transparency_logs': [],
            'chain_analysis': {},
            'security_assessment': {}
        }
        
        try:
            # Obtener información del certificado
            import ssl
            import socket
            
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    if cert:
                        results['certificate_info'] = {
                            'subject': {k: v for (k, v) in cert.get('subject', [])},
                            'issuer': {k: v for (k, v) in cert.get('issuer', [])},
                            'version': cert.get('version'),
                            'serial_number': cert.get('serialNumber'),
                            'not_before': cert.get('notBefore'),
                            'not_after': cert.get('notAfter'),
                            'subject_alt_names': [x[1] for x in cert.get('subjectAltName', [])]
                        }
                    else:
                        results['certificate_info'] = {'error': 'No certificate found'}
        except Exception as e:
            results['certificate_info'] = {'error': str(e)}
        
        try:
            # Buscar en Certificate Transparency logs
            ct_logs = self._search_ct_logs(domain)
            results['transparency_logs'] = ct_logs
        except Exception as e:
            results['transparency_logs'] = {'error': str(e)}
        
        return results
    
    def _search_ct_logs(self, domain: str) -> List[Dict[str, Any]]:
        """Busca en Certificate Transparency logs"""
        results = []
        
        try:
            # Usar crt.sh API
            url = f"https://crt.sh/?q={domain}&output=json"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                for cert in data:
                    results.append({
                        'id': cert.get('id', ''),
                        'logged_at': cert.get('entry_timestamp', ''),
                        'not_before': cert.get('not_before', ''),
                        'not_after': cert.get('not_after', ''),
                        'common_name': cert.get('common_name', ''),
                        'issuer_name': cert.get('issuer_name', ''),
                        'name_value': cert.get('name_value', '')
                    })
        except Exception as e:
            logger.error(f"Error buscando en CT logs: {e}")
        
        return results[:50]  # Limitar resultados

class DNSAnalyzer:
    """Analizador avanzado de DNS"""
    
    def __init__(self):
        self.session = requests.Session()
    
    def comprehensive_dns_analysis(self, domain: str) -> Dict[str, Any]:
        """Análisis completo de DNS"""
        results = {
            'domain': domain,
            'basic_records': {},
            'mx_analysis': {},
            'ns_analysis': {},
            'txt_analysis': {},
            'reverse_dns': {},
            'dns_history': {}
        }
        
        try:
            # Registros básicos
            results['basic_records'] = self._get_basic_records(domain)
        except Exception as e:
            logger.error(f"Error obteniendo registros básicos: {e}")
        
        try:
            # Análisis MX
            results['mx_analysis'] = self._analyze_mx_records(domain)
        except Exception as e:
            logger.error(f"Error analizando MX: {e}")
        
        try:
            # Análisis NS
            results['ns_analysis'] = self._analyze_ns_records(domain)
        except Exception as e:
            logger.error(f"Error analizando NS: {e}")
        
        try:
            # Análisis TXT
            results['txt_analysis'] = self._analyze_txt_records(domain)
        except Exception as e:
            logger.error(f"Error analizando TXT: {e}")
        
        return results
    
    def _get_basic_records(self, domain: str) -> Dict[str, Any]:
        """Obtiene registros DNS básicos"""
        import dns.resolver
        
        records = {}
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA', 'PTR']
        
        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                records[record_type] = [str(rdata) for rdata in answers]
            except:
                records[record_type] = []
        
        return records
    
    def _analyze_mx_records(self, domain: str) -> Dict[str, Any]:
        """Analiza registros MX"""
        import dns.resolver
        
        mx_info = {
            'records': [],
            'providers': [],
            'security_features': []
        }
        
        try:
            answers = dns.resolver.resolve(domain, 'MX')
            for mx in answers:
                # mx.to_text() returns something like '10 mail.example.com.'
                parts = mx.to_text().split()
                preference = int(parts[0]) if parts else None
                exchange = parts[1].rstrip('.') if len(parts) > 1 else ''
                mx_info['records'].append({
                    'preference': preference,
                    'exchange': exchange
                })
                
                # Detectar proveedores conocidos
                exchange_lower = exchange.lower()
                if 'google' in exchange_lower:
                    mx_info['providers'].append('Google Workspace')
                elif 'outlook' in exchange_lower or 'office365' in exchange_lower:
                    mx_info['providers'].append('Microsoft 365')
                elif 'mail.protection.outlook' in exchange_lower:
                    mx_info['providers'].append('Microsoft Defender')
        except:
            pass
        
        return mx_info
    
    def _analyze_ns_records(self, domain: str) -> Dict[str, Any]:
        """Analiza registros NS"""
        import dns.resolver
        
        ns_info = {
            'records': [],
            'providers': [],
            'locations': []
        }
        
        try:
            answers = dns.resolver.resolve(domain, 'NS')
            for ns in answers:
                ns_server = str(ns).lower()
                ns_info['records'].append(ns_server)
                
                # Detectar proveedores conocidos
                if 'cloudflare' in ns_server:
                    ns_info['providers'].append('Cloudflare')
                elif 'awsdns' in ns_server:
                    ns_info['providers'].append('AWS Route 53')
                elif 'googledomains' in ns_server:
                    ns_info['providers'].append('Google Domains')
        except:
            pass
        
        return ns_info
    
    def _analyze_txt_records(self, domain: str) -> Dict[str, Any]:
        """Analiza registros TXT"""
        import dns.resolver
        
        txt_info = {
            'records': [],
            'spf': [],
            'dmarc': [],
            'dkim': [],
            'verification': []
        }
        
        try:
            answers = dns.resolver.resolve(domain, 'TXT')
            for txt in answers:
                txt_value = str(txt).strip('"')
                txt_info['records'].append(txt_value)
                
                # Clasificar registros TXT
                if txt_value.startswith('v=spf1'):
                    txt_info['spf'].append(txt_value)
                elif txt_value.startswith('v=DMARC1'):
                    txt_info['dmarc'].append(txt_value)
                elif 'k=rsa' in txt_value:
                    txt_info['dkim'].append(txt_value)
                elif any(x in txt_value for x in ['google-site-verification', 'facebook-domain-verification']):
                    txt_info['verification'].append(txt_value)
        except:
            pass
        
        return txt_info

class ExifAnalyzer:
    """Analizador de metadatos EXIF"""
    
    def __init__(self):
        self.session = requests.Session()
    
    def analyze_image_url(self, image_url: str) -> Dict[str, Any]:
        """Analiza metadatos EXIF de una imagen desde URL"""
        results = {
            'url': image_url,
            'metadata': {},
            'location': {},
            'device_info': {},
            'timestamp': {}
        }
        
        try:
            # Descargar imagen
            response = self.session.get(image_url, timeout=10)
            if response.status_code == 200:
                # Guardar temporalmente
                temp_file = '/tmp/temp_image.jpg'
                with open(temp_file, 'wb') as f:
                    f.write(response.content)
                
                # Analizar EXIF
                exif_data = self._extract_exif(temp_file)
                results.update(exif_data)
                
                # Limpiar archivo temporal
                os.remove(temp_file)
        
        except Exception as e:
            results['error'] = str(e)
        
        return results
    
    def _extract_exif(self, image_path: str) -> Dict[str, Any]:
        """Extrae metadatos EXIF usando herramientas del sistema"""
        try:
            # Usar exiftool si está disponible
            result = subprocess.run(['exiftool', '-j', image_path], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)[0]
                return {
                    'metadata': data,
                    'location': self._extract_location(data),
                    'device_info': self._extract_device_info(data),
                    'timestamp': self._extract_timestamp(data)
                }
        except:
            pass
        
        # Método alternativo con PIL
        try:
            from PIL import Image
            from PIL.ExifTags import TAGS
            
            image = Image.open(image_path)
            exif_data = image.getexif()
            
            if exif_data:
                metadata = {}
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    metadata[tag] = value
                
                return {
                    'metadata': metadata,
                    'location': self._extract_location(metadata),
                    'device_info': self._extract_device_info(metadata),
                    'timestamp': self._extract_timestamp(metadata)
                }
        except:
            pass
        
        return {'error': 'No se pudo extraer metadatos EXIF'}
    
    def _extract_location(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Extrae información de ubicación"""
        location = {}
        
        # Buscar coordenadas GPS
        if 'GPSLatitude' in metadata and 'GPSLongitude' in metadata:
            location['has_gps'] = True
            location['latitude'] = metadata.get('GPSLatitude', '')
            location['longitude'] = metadata.get('GPSLongitude', '')
        
        return location
    
    def _extract_device_info(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Extrae información del dispositivo"""
        device_info = {}
        
        device_info['make'] = metadata.get('Make', '')
        device_info['model'] = metadata.get('Model', '')
        device_info['software'] = metadata.get('Software', '')
        
        return device_info
    
    def _extract_timestamp(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Extrae información de timestamp"""
        timestamp_info = {}
        
        timestamp_info['date_time'] = metadata.get('DateTime', '')
        timestamp_info['date_time_original'] = metadata.get('DateTimeOriginal', '')
        timestamp_info['date_time_digitized'] = metadata.get('DateTimeDigitized', '')
        
        return timestamp_info

class OSINTSpecializedTools:
    """Herramientas OSINT especializadas"""
    
    def __init__(self):
        self.leak_checker = LeakChecker()
        self.pastebin_searcher = PastebinSearcher()
        self.github_investigator = GitHubInvestigator()
        self.certificate_analyzer = CertificateAnalyzer()
        self.dns_analyzer = DNSAnalyzer()
        self.exif_analyzer = ExifAnalyzer()
    
    def comprehensive_email_investigation(self, email: str) -> Dict[str, Any]:
        """Investigación completa de email"""
        results = {
            'email': email,
            'breach_check': {},
            'pastebin_search': [],
            'github_search': [],
            'domain_analysis': {}
        }
        
        # Verificar filtraciones
        results['breach_check'] = self.leak_checker.check_email_breaches(email)
        
        # Buscar en pastebins
        results['pastebin_search'] = self.pastebin_searcher.search_pastes(email)
        
        # Buscar en GitHub
        results['github_search'] = self.github_investigator.search_code(email)
        
        # Analizar dominio
        domain = email.split('@')[1] if '@' in email else ''
        if domain:
            results['domain_analysis'] = self.dns_analyzer.comprehensive_dns_analysis(domain)
        
        return results
    
    def investigate_data_leak(self, query: str) -> Dict[str, Any]:
        """Investiga posibles filtraciones de datos"""
        results = {
            'query': query,
            'pastebin_results': [],
            'github_results': [],
            'breach_databases': []
        }
        
        # Buscar en pastebins
        results['pastebin_results'] = self.pastebin_searcher.search_pastes(query)
        
        # Buscar en GitHub
        results['github_results'] = self.github_investigator.search_code(query)
        
        return results
    
    def analyze_suspicious_domain(self, domain: str) -> Dict[str, Any]:
        """Analiza un dominio sospechoso"""
        results = {
            'domain': domain,
            'reputation': {},
            'certificate_analysis': {},
            'dns_analysis': {},
            'historical_data': {}
        }
        
        # Verificar reputación
        results['reputation'] = self.leak_checker.check_domain_reputation(domain)
        
        # Analizar certificado
        results['certificate_analysis'] = self.certificate_analyzer.analyze_certificate(domain)
        
        # Analizar DNS
        results['dns_analysis'] = self.dns_analyzer.comprehensive_dns_analysis(domain)
        
        return results
