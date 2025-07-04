#!/usr/bin/env python3
"""
Servidor MCP para búsquedas OSINT automatizadas con reportes diarios por correo
Versión mejorada con más fuentes de búsqueda, interfaz en español y dorking avanzado
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import sqlite3
import schedule
import time
import threading
from dataclasses import dataclass, field
import requests
from bs4 import BeautifulSoup, Tag
from bs4.element import NavigableString
import re
import hashlib
from urllib.parse import urlparse, urljoin, quote
import os
from pathlib import Path
import aiofiles
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, session, flash, Response
import plotly.graph_objs as go
import plotly.utils
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps
import whois
import dns.resolver
import subprocess
import socket
import ssl
import shodan
import csv
import openpyxl
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import io

# Importar el nuevo módulo de IA
try:
    import ai_core
    AI_CORE_AVAILABLE = True
    print("INFO: Módulo ai_core cargado exitosamente.")
except ImportError as e:
    AI_CORE_AVAILABLE = False
    print(f"ADVERTENCIA: Módulo ai_core.py no encontrado o con errores de importación: {e}")
    # logging.warning(f"Módulo ai_core.py no encontrado o con errores de importación: {e}")


# Importar módulos OSINT avanzados si están disponibles
try:
    from osint_advanced import AdvancedOSINTToolkit
    ADVANCED_OSINT_AVAILABLE = True
except ImportError:
    ADVANCED_OSINT_AVAILABLE = False
    logging.warning("Módulo OSINT avanzado no disponible")

try:
    from osint_specialized import OSINTSpecializedTools
    SPECIALIZED_OSINT_AVAILABLE = True
except ImportError:
    SPECIALIZED_OSINT_AVAILABLE = False
    logging.warning("Módulo OSINT especializado no disponible")

# Importar descargador de archivos
try:
    from osint_file_downloader import OSINTFileDownloader
    FILE_DOWNLOADER_AVAILABLE = True
except ImportError:
    FILE_DOWNLOADER_AVAILABLE = False
    logging.warning("Módulo de descarga de archivos no disponible")

# Configuración del logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class OSINTConfig:
    """Configuración para búsquedas OSINT mejorada"""
    # Configuración de email
    email_smtp_server: str = "smtp.gmail.com"
    email_smtp_port: int = 587
    email_username: str = ""
    email_password: str = ""
    email_recipients: List[str] = field(default_factory=list)
    report_time: str = "08:00"
    
    # Configuración de búsqueda
    max_results_per_source: int = 20
    enable_deep_search: bool = True
    search_engines: List[str] = field(default_factory=lambda: ["google", "bing", "duckduckgo"])
    
    # APIs de servicios especializados
    shodan_api_key: str = ""
    virustotal_api_key: str = ""
    
    # Configuración de la interfaz web
    web_interface_enabled: bool = True
    web_port: int = 5000
    web_host: str = "localhost"
    web_auth_enabled: bool = True
    web_username: str = "admin"
    web_password: str = "admin123"
    web_password_hash: str = ""
    secret_key: str = "osint-server-secret-key-2025"
    
    # Configuración de reportes
    export_formats: List[str] = field(default_factory=lambda: ["html", "pdf", "xlsx", "csv"])
    include_charts: bool = True
    
    # Configuración de búsquedas especializadas
    enable_domain_analysis: bool = True
    enable_ip_analysis: bool = True
    enable_social_media_search: bool = True
    enable_news_search: bool = True
    
    # Límites y timeouts
    request_timeout: int = 30
    max_concurrent_requests: int = 10
    rate_limit_delay: float = 2.0
    
    def __post_init__(self):
        # Generar hash de contraseña si no existe
        if not self.web_password_hash:
            if self.web_password:
                self.web_password_hash = generate_password_hash(self.web_password)
            else:
                self.web_password_hash = generate_password_hash("admin123")

class GoogleDorkingEngine:
    """Motor de Google Dorking avanzado con automatizaciones y patterns especializados"""
    
    def __init__(self, config: OSINTConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # Patrones de dorking categorizados en español
        self.dork_patterns = {
            'archivos_confidenciales': [
                'filetype:pdf "confidencial"',
                'filetype:doc "contraseña"', 
                'filetype:xls "usuarios"',
                'filetype:txt "password"',
                'filetype:sql "INSERT INTO"',
                'filetype:log "error"',
                'filetype:backup',
                'filetype:old',
                'filetype:bak'
            ],
            'directorios_expuestos': [
                'intitle:"Index of" "Parent Directory"',
                'intitle:"Index of /" +passwd',
                'intitle:"Index of /" +password.txt',
                'intitle:"index of" "database"',
                'intitle:"index of" "backup"',
                'intitle:"directory listing for"'
            ],
            'informacion_corporativa': [
                'site:linkedin.com "TARGET"',
                'site:glassdoor.com "TARGET"',
                '"organigrama" OR "estructura organizacional" "TARGET"',
                'intitle:"empleados" "TARGET"',
                '"directorio telefónico" "TARGET"'
            ],
            'errores_aplicaciones': [
                'intitle:"Error" "database"',
                'intitle:"Warning" "failed"',
                'intitle:"Fatal error"',
                '"mysql_connect()" error',
                '"ORA-" Oracle error',
                '"Microsoft OLE DB Provider for ODBC Drivers error"'
            ],
            'paneles_administracion': [
                'intitle:"Admin Panel"',
                'intitle:"Login" "admin"',
                'intitle:"Dashboard" "admin"',
                'inurl:admin/login',
                'inurl:administrator',
                'inurl:wp-admin',
                'inurl:phpmyadmin'
            ],
            'redes_sociales': [
                'site:facebook.com "TARGET"',
                'site:twitter.com "TARGET"',
                'site:instagram.com "TARGET"',
                'site:linkedin.com "TARGET"',
                'site:tiktok.com "TARGET"',
                '"perfil" "TARGET"'
            ]
        }

    def generate_dorks_for_target(self, target: str, category: str = 'all') -> List[str]:
        """Genera dorks automáticamente para un objetivo específico"""
        dorks = []
        
        if category == 'all' or category == 'general':
            base_dorks = [
                f'"{target}"',
                f'site:{target}' if '.' in target else f'"{target}"',
                f'inurl:{target}',
                f'intitle:"{target}"',
                f'"{target}" filetype:pdf',
                f'"{target}" filetype:doc',
                f'"{target}" "email" OR "correo"',
                f'"{target}" "teléfono" OR "phone"'
            ]
            dorks.extend(base_dorks)
        
        if category in self.dork_patterns:
            for pattern in self.dork_patterns[category]:
                dork = pattern.replace('TARGET', target)
                dorks.append(dork)
        elif category == 'all':
            for cat_patterns in self.dork_patterns.values():
                for pattern in cat_patterns:
                    dork = pattern.replace('TARGET', target)
                    dorks.append(dork)
        
        return dorks

    def execute_dork_campaign(self, target: str, categories: Optional[List[str]] = None) -> Dict[str, Any]:
        """Ejecuta una campaña completa de dorking automatizada"""
        if categories is None:
            categories = ['general', 'archivos_confidenciales']
        
        campaign_results = {
            'target': target,
            'start_time': datetime.now().isoformat(),
            'categories': categories,
            'total_dorks': 0,
            'total_results': 0,
            'results_by_category': {},
            'high_risk_findings': [],
            'recommendations': []
        }
        
        for category in categories:
            logger.info(f"Ejecutando dorks para categoría: {category}")
            
            dorks = self.generate_dorks_for_target(target, category)
            campaign_results['total_dorks'] += len(dorks)
            
            category_results = []
            for dork in dorks[:5]:  # Limitar para evitar rate limiting
                try:
                    time.sleep(self.config.rate_limit_delay)
                    results = self._execute_single_dork(dork)
                    category_results.extend(results)
                except Exception as e:
                    logger.error(f"Error ejecutando dork '{dork}': {str(e)}")
                    continue
            
            campaign_results['results_by_category'][category] = {
                'total_results': len(category_results),
                'results': category_results
            }
            campaign_results['total_results'] += len(category_results)
        
        campaign_results['recommendations'] = self._generate_recommendations(campaign_results)
        return campaign_results

    def _execute_single_dork(self, dork: str) -> List[Dict[str, Any]]:
        """Ejecuta un dork individual y parsea los resultados"""
        try:
            search_url = "https://www.google.com/search"
            params = {
                'q': dork,
                'num': min(10, self.config.max_results_per_source),
                'hl': 'es'
            }
            
            response = self.session.get(search_url, params=params, timeout=self.config.request_timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            # Buscar divs de resultados con diferentes clases
            result_divs = soup.find_all('div', class_='g') or soup.find_all('div', class_='tF2Cxc')
            
            for result_div in result_divs:
                try:
                    # Buscar título y enlace con manejo robusto de tipos
                    title_elem = None
                    link_elem = None
                    
                    # Verificar si result_div es un Tag válido de BeautifulSoup
                    if isinstance(result_div, Tag):
                        title_elem = result_div.find('h3') or result_div.find('a')
                        link_elem = result_div.find('a')
                    
                    if title_elem and link_elem:
                        title = self._safe_get_text(title_elem)
                        url = self._safe_get_attr(link_elem, 'href')
                        
                        if url and isinstance(url, str) and url.startswith('http'):
                            results.append({
                                'title': title,
                                'url': url,
                                'description': '',
                                'source': 'google_dork',
                                'dork_used': dork,
                                'timestamp': datetime.now().isoformat(),
                                'risk_level': self._assess_risk_level(title + ' ' + url)
                            })
                            
                except Exception:
                    continue
            
            return results
            
        except Exception as e:
            logger.error(f"Error ejecutando dork '{dork}': {str(e)}")
            return []

    def _safe_get_text(self, element) -> str:
        """Extrae texto de forma segura de un elemento"""
        try:
            if hasattr(element, 'get_text'):
                return element.get_text().strip()
            else:
                return str(element).strip()
        except:
            return ""

    def _safe_get_attr(self, element, attr: str) -> str:
        """Extrae atributo de forma segura de un elemento"""
        try:
            if hasattr(element, 'get'):
                value = element.get(attr, '')
                return str(value) if value else ''
            else:
                return ""
        except:
            return ""

    def _assess_risk_level(self, content: str) -> str:
        """Evalúa el nivel de riesgo de un resultado"""
        high_risk_keywords = [
            'password', 'contraseña', 'login', 'admin', 'database',
            'confidencial', 'private', 'internal', 'backup',
            'error', 'warning', 'sql', 'dump'
        ]
        
        content_lower = content.lower()
        
        if any(keyword in content_lower for keyword in high_risk_keywords):
            return 'high'
        
        return 'low'

    def _generate_recommendations(self, campaign_results: Dict[str, Any]) -> List[str]:
        """Genera recomendaciones de seguridad"""
        recommendations = [
            "🔍 Revisar todos los resultados encontrados para identificar exposiciones de datos.",
            "🛡️ Implementar medidas de seguridad para proteger información sensible.",
            "📋 Realizar auditorías regulares de seguridad y exposición en internet.",
            "🚨 Configurar alertas automáticas para detectar nuevas exposiciones."
        ]
        
        if campaign_results['total_results'] > 0:
            recommendations.insert(0, f"⚠️ Se encontraron {campaign_results['total_results']} resultados que requieren revisión.")
        
        return recommendations

class OSINTDatabase:
    """Base de datos mejorada para almacenar resultados de búsquedas OSINT"""
    
    def __init__(self, db_path: str = "osint_data.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializa la base de datos con tablas mejoradas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de búsquedas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS searches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                search_type TEXT DEFAULT 'general',
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                results_count INTEGER DEFAULT 0,
                status TEXT DEFAULT 'pending',
                user_id TEXT DEFAULT 'anonymous'
            )
        ''')
        
        # Tabla de resultados
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                search_id INTEGER,
                source TEXT,
                result_type TEXT DEFAULT 'web',
                title TEXT,
                url TEXT,
                description TEXT,
                content TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                relevance_score REAL DEFAULT 0.0,
                risk_level TEXT DEFAULT 'low',
                FOREIGN KEY (search_id) REFERENCES searches (id)
            )
        ''')
        
        # Tabla de reportes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_type TEXT DEFAULT 'daily',
                date DATE,
                title TEXT,
                content TEXT,
                format TEXT DEFAULT 'html',
                file_path TEXT,
                sent_at DATETIME,
                status TEXT DEFAULT 'pending'
            )
        ''')
        
        # Tabla de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                role TEXT DEFAULT 'user',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_login DATETIME,
                is_active BOOLEAN DEFAULT 1,
                email_verified BOOLEAN DEFAULT 0
            )
        ''')
        
        # Tabla de configuraciones de usuario
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                setting_name TEXT NOT NULL,
                setting_value TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                UNIQUE(user_id, setting_name)
            )
        ''')
        
        # Tabla de configuraciones de reportes por usuario
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_report_configs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                report_name TEXT NOT NULL,
                report_type TEXT DEFAULT 'daily',
                frequency TEXT DEFAULT 'daily',
                email_delivery BOOLEAN DEFAULT 1,
                format TEXT DEFAULT 'html',
                search_queries TEXT,
                search_types TEXT,
                enable_dorking BOOLEAN DEFAULT 0,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Tabla de reportes generados por usuario
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                config_id INTEGER NOT NULL,
                report_title TEXT,
                report_content TEXT,
                report_format TEXT,
                file_path TEXT,
                generated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                sent_at DATETIME,
                status TEXT DEFAULT 'pending',
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (config_id) REFERENCES user_report_configs (id)
            )
        ''')
        
        # Modificar tabla de búsquedas para incluir user_id
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS searches_backup AS SELECT * FROM searches;
        ''')
        
        cursor.execute('''
            DROP TABLE IF EXISTS searches;
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS searches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER DEFAULT 1,
                query TEXT NOT NULL,
                search_type TEXT DEFAULT 'general',
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                results_count INTEGER DEFAULT 0,
                status TEXT DEFAULT 'pending',
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Restaurar datos de búsquedas con user_id por defecto
        cursor.execute('''
            INSERT INTO searches (query, search_type, timestamp, results_count, status)
            SELECT query, search_type, timestamp, results_count, status 
            FROM searches_backup;
        ''')
        
        cursor.execute('''
            DROP TABLE IF EXISTS searches_backup;
        ''')
        
        # Crear usuario administrador por defecto si no existe
        cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', ('admin',))
        if cursor.fetchone()[0] == 0:
            admin_password_hash = generate_password_hash('admin123')
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, full_name, role, is_active, email_verified)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', ('admin', 'admin@osint.local', admin_password_hash, 'Administrador', 'admin', 1, 1))
        
        conn.commit()
        conn.close()
    
    def save_search(self, query: str, search_type: str = 'general', user_id: int = 1) -> int:
        """Guarda una nueva búsqueda y retorna el ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO searches (query, search_type, user_id) VALUES (?, ?, ?)",
            (query, search_type, user_id)
        )
        
        search_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return search_id if search_id is not None else 0

    def save_results(self, search_id: int, results: List[Dict[str, Any]]):
        """Guarda los resultados de una búsqueda"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for result in results:
            cursor.execute('''
                INSERT INTO search_results 
                (search_id, source, title, url, description, content, relevance_score, risk_level)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                search_id,
                result.get('source', ''),
                result.get('title', ''),
                result.get('url', ''),
                result.get('description', ''),
                result.get('content', ''),
                result.get('relevance_score', 0.0),
                result.get('risk_level', 'low')
            ))
        
        # Actualizar contador de resultados
        cursor.execute(
            "UPDATE searches SET results_count = ?, status = 'completed' WHERE id = ?",
            (len(results), search_id)
        )
        
        conn.commit()
        conn.close()

    def get_recent_results(self, days: int = 1) -> List[Dict[str, Any]]:
        """Obtiene resultados recientes para el reporte"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        date_threshold = datetime.now() - timedelta(days=days)
        
        cursor.execute('''
            SELECT s.query, s.search_type, s.timestamp, sr.source,
                   sr.title, sr.url, sr.description, sr.relevance_score, sr.risk_level
            FROM searches s
            JOIN search_results sr ON s.id = sr.search_id
            WHERE s.timestamp >= ?
            ORDER BY s.timestamp DESC, sr.relevance_score DESC
        ''', (date_threshold,))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'query': row[0],
                'search_type': row[1],
                'timestamp': row[2],
                'source': row[3],
                'title': row[4],
                'url': row[5],
                'description': row[6],
                'relevance_score': row[7],
                'risk_level': row[8]
            })
        
        conn.close()
        return results

    def get_user_by_credentials(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Autentica un usuario y retorna sus datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, email, password_hash, full_name, role, is_active
            FROM users 
            WHERE username = ? AND is_active = 1
        ''', (username,))
        
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data and check_password_hash(user_data[3], password):
            return {
                'id': user_data[0],
                'username': user_data[1],
                'email': user_data[2],
                'full_name': user_data[4],
                'role': user_data[5],
                'is_active': user_data[6]
            }
        return None

    def register_user(self, username: str, email: str, password: str, full_name: str = '') -> bool:
        """Registra un nuevo usuario"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Verificar si el usuario ya existe
            cursor.execute('SELECT id FROM users WHERE username = ? OR email = ?', (username, email))
            if cursor.fetchone():
                conn.close()
                return False
            
            password_hash = generate_password_hash(password)
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, full_name, role, is_active)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, email, password_hash, full_name or username, 'user', 1))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error registrando usuario: {str(e)}")
            return False

    def get_user_searches(self, user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """Obtiene las búsquedas de un usuario específico"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT s.id, s.query, s.search_type, s.timestamp, s.results_count, s.status
            FROM searches s
            WHERE s.user_id = ?
            ORDER BY s.timestamp DESC
            LIMIT ?
        ''', (user_id, limit))
        
        searches = []
        for row in cursor.fetchall():
            searches.append({
                'id': row[0],
                'query': row[1],
                'search_type': row[2],
                'timestamp': row[3],
                'results_count': row[4],
                'status': row[5]
            })
        
        conn.close()
        return searches

    def save_user_report_config(self, user_id: int, config_data: Dict[str, Any]) -> bool:
        """Guarda configuración de reporte personalizado"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO user_report_configs 
                (user_id, report_name, report_type, frequency, email_delivery, format, 
                 search_queries, search_types, enable_dorking, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id,
                config_data.get('report_name', 'Mi Reporte'),
                config_data.get('report_type', 'daily'),
                config_data.get('frequency', 'daily'),
                config_data.get('email_delivery', True),
                config_data.get('format', 'html'),
                json.dumps(config_data.get('search_queries', [])),
                json.dumps(config_data.get('search_types', [])),
                config_data.get('enable_dorking', False),
                config_data.get('is_active', True)
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error guardando configuración de reporte: {str(e)}")
            return False

    def get_user_report_configs(self, user_id: int) -> List[Dict[str, Any]]:
        """Obtiene configuraciones de reportes de un usuario"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, report_name, report_type, frequency, email_delivery, format,
                   search_queries, search_types, enable_dorking, is_active, created_at
            FROM user_report_configs 
            WHERE user_id = ?
            ORDER BY created_at DESC
        ''', (user_id,))
        
        configs = []
        for row in cursor.fetchall():
            configs.append({
                'id': row[0],
                'report_name': row[1],
                'report_type': row[2],
                'frequency': row[3],
                'email_delivery': row[4],
                'format': row[5],
                'search_queries': json.loads(row[6]) if row[6] else [],
                'search_types': json.loads(row[7]) if row[7] else [],
                'enable_dorking': row[8],
                'is_active': row[9],
                'created_at': row[10]
            })
        
        conn.close()
        return configs

    def generate_user_report(self, user_id: int, config_id: int) -> Optional[Dict[str, Any]]:
        """Genera un reporte personalizado para un usuario"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Obtener configuración
            cursor.execute('''
                SELECT report_name, report_type, frequency, format, search_queries, 
                       search_types, enable_dorking
                FROM user_report_configs 
                WHERE id = ? AND user_id = ? AND is_active = 1
            ''', (config_id, user_id))
            
            config_data = cursor.fetchone()
            if not config_data:
                return None
            
            report_name, report_type, frequency, format_type, search_queries, search_types, enable_dorking = config_data
            
            # Obtener datos del usuario
            cursor.execute('SELECT email, full_name FROM users WHERE id = ?', (user_id,))
            user_data = cursor.fetchone()
            
            if not user_data:
                return None
            
            user_email, user_full_name = user_data
            
            # Generar contenido del reporte
            search_queries_list = json.loads(search_queries) if search_queries else []
            search_types_list = json.loads(search_types) if search_types else []
            
            report_content = self._generate_report_content(
                user_full_name, report_name, search_queries_list, 
                search_types_list, enable_dorking
            )
            
            # Guardar reporte
            cursor.execute('''
                INSERT INTO user_reports 
                (user_id, config_id, report_title, report_content, report_format, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, config_id, report_name, report_content, format_type, 'generated'))
            
            report_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return {
                'id': report_id,
                'title': report_name,
                'content': report_content,
                'format': format_type,
                'user_email': user_email,
                'user_name': user_full_name
            }
            
        except Exception as e:
            logger.error(f"Error generando reporte: {str(e)}")
            return None

    def _generate_report_content(self, user_name: str, report_name: str, 
                               search_queries: List[str], search_types: List[str],
                               enable_dorking: bool) -> str:
        """Genera el contenido HTML del reporte personalizado"""
        
        current_date = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        html_content = f'''
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{report_name} - Reporte OSINT</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: #333;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                    overflow: hidden;
                }}
                .header {{
                    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 2.5em;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                }}
                .header p {{
                    margin: 10px 0 0 0;
                    font-size: 1.2em;
                    opacity: 0.9;
                }}
                .content {{
                    padding: 40px;
                }}
                .section {{
                    margin-bottom: 40px;
                    padding: 20px;
                    background: #f8f9fa;
                    border-radius: 10px;
                    border-left: 5px solid #007bff;
                }}
                .section h2 {{
                    color: #007bff;
                    margin-bottom: 20px;
                    font-size: 1.5em;
                }}
                .query-item {{
                    background: white;
                    padding: 15px;
                    margin: 10px 0;
                    border-radius: 8px;
                    border: 1px solid #e9ecef;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                .query-type {{
                    display: inline-block;
                    padding: 4px 12px;
                    background: #28a745;
                    color: white;
                    border-radius: 20px;
                    font-size: 0.8em;
                    margin-bottom: 10px;
                }}
                .footer {{
                    background: #343a40;
                    color: white;
                    text-align: center;
                    padding: 20px;
                    font-size: 0.9em;
                }}
                .alert {{
                    background: #fff3cd;
                    border: 1px solid #ffeaa7;
                    border-radius: 8px;
                    padding: 15px;
                    margin: 20px 0;
                    color: #856404;
                }}
                .stats {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                    margin: 20px 0;
                }}
                .stat-card {{
                    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 10px;
                    text-align: center;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
                }}
                .stat-number {{
                    font-size: 2em;
                    font-weight: bold;
                    margin-bottom: 5px;
                }}
                .stat-label {{
                    font-size: 0.9em;
                    opacity: 0.9;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔍 {report_name}</h1>
                    <p>Reporte OSINT personalizado para {user_name}</p>
                    <p>Generado el {current_date}</p>
                </div>
                
                <div class="content">
                    <div class="stats">
                        <div class="stat-card">
                            <div class="stat-number">{len(search_queries)}</div>
                            <div class="stat-label">Consultas Configuradas</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">{len(search_types)}</div>
                            <div class="stat-label">Tipos de Búsqueda</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">{'SÍ' if enable_dorking else 'NO'}</div>
                            <div class="stat-label">Google Dorking</div>
                        </div>
                    </div>
                    
                    <div class="section">
                        <h2>📋 Configuración del Reporte</h2>
                        <div class="query-item">
                            <strong>Consultas de Búsqueda:</strong><br>
                            {', '.join(search_queries) if search_queries else 'Ninguna configurada'}
                        </div>
                        <div class="query-item">
                            <strong>Tipos de Búsqueda:</strong><br>
                            {', '.join(search_types) if search_types else 'General'}
                        </div>
                        <div class="query-item">
                            <strong>Google Dorking:</strong> {'Habilitado' if enable_dorking else 'Deshabilitado'}
                        </div>
                    </div>
                    
                    <div class="alert">
                        <strong>📢 Nota:</strong> Este es un reporte de configuración. Para obtener resultados reales, 
                        el sistema ejecutará las búsquedas según la periodicidad configurada y enviará 
                        los resultados a tu correo electrónico.
                    </div>
                    
                    <div class="section">
                        <h2>🚀 Próximos Pasos</h2>
                        <ul>
                            <li>El sistema ejecutará automáticamente las búsquedas configuradas</li>
                            <li>Recibirás notificaciones por correo cuando se generen nuevos reportes</li>
                            <li>Podrás ver el historial completo en tu panel de usuario</li>
                            <li>Los reportes incluirán análisis de riesgo y recomendaciones</li>
                        </ul>
                    </div>
                </div>
                
                <div class="footer">
                    <p>🔐 Servidor OSINT - Generado automáticamente</p>
                    <p>Para soporte técnico, contacta al administrador del sistema</p>
                </div>
            </div>
        </body>
        </html>
        '''
        
        return html_content

class EnhancedOSINTSearcher:
    """Buscador OSINT mejorado con capacidades avanzadas"""
    
    def __init__(self, config: OSINTConfig):
        self.config = config
        self.db = OSINTDatabase()
        self.dorking_engine = GoogleDorkingEngine(config)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

    def search(self, query: str, search_type: str = 'general', enable_dorking: bool = False, user_id: int = 1) -> Dict[str, Any]:
        """Realiza búsqueda OSINT completa"""
        logger.info(f"Iniciando búsqueda OSINT para: {query}")
        
        # Guardar búsqueda en BD
        search_id = self.db.save_search(query, search_type, user_id)
        
        all_results = []
        
        # Búsqueda tradicional
        traditional_results = self._traditional_search(query)
        all_results.extend(traditional_results)
        
        # Búsqueda con Google Dorking si está habilitada
        if enable_dorking:
            dorking_results = self.dorking_engine.execute_dork_campaign(query)
            for category_data in dorking_results['results_by_category'].values():
                all_results.extend(category_data['results'])
        
        # Análisis especializado según tipo
        if search_type == 'domain' and self.config.enable_domain_analysis:
            domain_results = self._analyze_domain(query)
            all_results.extend(domain_results)
        elif search_type == 'ip' and self.config.enable_ip_analysis:
            ip_results = self._analyze_ip(query)
            all_results.extend(ip_results)
        
        # Procesar y calcular relevancia
        processed_results = self._process_results(all_results, query)
        
        # Guardar resultados
        self.db.save_results(search_id, processed_results)
        
        return {
            'search_id': search_id,
            'query': query,
            'search_type': search_type,
            'total_results': len(processed_results),
            'results': processed_results,
            'timestamp': datetime.now().isoformat()
        }

    def _traditional_search(self, query: str) -> List[Dict[str, Any]]:
        """Búsqueda tradicional en motores configurados"""
        all_results = []
        
        for engine in self.config.search_engines:
            try:
                if engine == "google":
                    results = self._search_google(query)
                elif engine == "bing":
                    results = self._search_bing(query)
                elif engine == "duckduckgo":
                    results = self._search_duckduckgo(query)
                else:
                    continue
                
                all_results.extend(results)
                time.sleep(self.config.rate_limit_delay)
                
            except Exception as e:
                logger.error(f"Error en búsqueda {engine}: {str(e)}")
                continue
        
        return all_results

    def _search_google(self, query: str) -> List[Dict[str, Any]]:
        """Búsqueda básica en Google"""
        try:
            url = f"https://www.google.com/search?q={quote(query)}&num={self.config.max_results_per_source}&hl=es"
            response = self.session.get(url, timeout=self.config.request_timeout)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            results = []
            # Buscar diferentes tipos de contenedores de resultados
            result_containers = soup.find_all('div', class_='g') or soup.find_all('div', class_='tF2Cxc')
            
            for container in result_containers[:self.config.max_results_per_source]:
                try:
                    title_elem = None
                    link_elem = None
                    
                    if isinstance(container, Tag):
                        title_elem = container.find('h3')
                        link_elem = container.find('a')
                    
                    if title_elem and link_elem:
                        title = self.dorking_engine._safe_get_text(title_elem)
                        url_href = self.dorking_engine._safe_get_attr(link_elem, 'href')
                        
                        if url_href and url_href.startswith('http'):
                            results.append({
                                'source': 'google',
                                'title': title,
                                'url': url_href,
                                'description': '',
                                'content': '',
                                'relevance_score': 0.0,
                                'risk_level': 'low'
                            })
                except Exception:
                    continue
            
            return results
            
        except Exception as e:
            logger.error(f"Error en búsqueda Google: {str(e)}")
            return []

    def _search_bing(self, query: str) -> List[Dict[str, Any]]:
        """Búsqueda en Bing"""
        try:
            url = f"https://www.bing.com/search?q={quote(query)}&count={self.config.max_results_per_source}"
            response = self.session.get(url, timeout=self.config.request_timeout)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            results = []
            for container in soup.find_all('li', class_='b_algo')[:self.config.max_results_per_source]:
                try:
                    title_elem = None
                    link_elem = None
                    
                    if isinstance(container, Tag):
                        title_elem = container.find('h2')
                        if isinstance(title_elem, Tag):
                            link_elem = title_elem.find('a')
                    
                    if title_elem and link_elem:
                        title = self.dorking_engine._safe_get_text(title_elem)
                        url_href = self.dorking_engine._safe_get_attr(link_elem, 'href')
                        
                        if url_href and url_href.startswith('http'):
                            results.append({
                                'source': 'bing',
                                'title': title,
                                'url': url_href,
                                'description': '',
                                'content': '',
                                'relevance_score': 0.0,
                                'risk_level': 'low'
                            })
                except Exception:
                    continue
            
            return results
            
        except Exception as e:
            logger.error(f"Error en búsqueda Bing: {str(e)}")
            return []

    def _search_duckduckgo(self, query: str) -> List[Dict[str, Any]]:
        """Búsqueda en DuckDuckGo"""
        try:
            url = f"https://duckduckgo.com/html?q={quote(query)}"
            response = self.session.get(url, timeout=self.config.request_timeout)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            results = []
            for container in soup.find_all('div', class_='result')[:self.config.max_results_per_source]:
                try:
                    link_elem = None
                    
                    if isinstance(container, Tag):
                        link_elem = container.find('a', {'class': 'result__a'})
                    
                    if link_elem:
                        title = self.dorking_engine._safe_get_text(link_elem)
                        url_href = self.dorking_engine._safe_get_attr(link_elem, 'href')
                        
                        if url_href and url_href.startswith('http'):
                            results.append({
                                'source': 'duckduckgo',
                                'title': title,
                                'url': url_href,
                                'description': '',
                                'content': '',
                                'relevance_score': 0.0,
                                'risk_level': 'low'
                            })
                except Exception:
                    continue
            
            return results
            
        except Exception as e:
            logger.error(f"Error en búsqueda DuckDuckGo: {str(e)}")
            return []

    def _analyze_domain(self, domain: str) -> List[Dict[str, Any]]:
        """Análisis básico de dominio"""
        results = []
        
        try:
            # Obtener IP del dominio
            ip = socket.gethostbyname(domain)
            results.append({
                'source': 'domain_analysis',
                'title': f'Dirección IP de {domain}',
                'url': f'http://{ip}',
                'description': f'IP: {ip}',
                'content': '',
                'relevance_score': 1.0,
                'risk_level': 'low'
            })
        except Exception:
            pass
        
        return results

    def _analyze_ip(self, ip: str) -> List[Dict[str, Any]]:
        """Análisis básico de IP"""
        results = []
        
        try:
            # Verificar si la IP responde
            response = requests.get(f'http://{ip}', timeout=5)
            results.append({
                'source': 'ip_analysis',
                'title': f'Servidor web en {ip}',
                'url': f'http://{ip}',
                'description': f'Servidor responde con código {response.status_code}',
                'content': '',
                'relevance_score': 1.0,
                'risk_level': 'medium'
            })
        except Exception:
            pass
        
        return results

    def _process_results(self, results: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        """Procesa y mejora los resultados"""
        processed = []
        seen_urls = set()
        
        for result in results:
            url = result.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                
                # Calcular relevancia básica
                title = result.get('title', '').lower()
                description = result.get('description', '').lower()
                query_lower = query.lower()
                
                relevance = 0.0
                if query_lower in title:
                    relevance += 0.5
                if query_lower in description:
                    relevance += 0.3
                
                result['relevance_score'] = relevance
                processed.append(result)
        
        # Ordenar por relevancia
        processed.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return processed

class FlaskWebInterface:
    """Interfaz web Flask mejorada en español"""
    
    def __init__(self, osint_searcher: EnhancedOSINTSearcher, config: OSINTConfig):
        self.app = Flask(__name__)
        self.app.secret_key = config.secret_key
        self.osint_searcher = osint_searcher
        self.config = config
        
        self.setup_routes()

    def setup_routes(self):
        """Configura las rutas de la aplicación"""
        
        def require_auth():
            """Función auxiliar para verificar autenticación"""
            if self.config.web_auth_enabled and not session.get('authenticated'):
                return redirect(url_for('login'))
            return None
        
        def get_current_user():
            """Obtiene el usuario actual de la sesión"""
            if session.get('authenticated'):
                return session.get('user_data')
            return None
        
        @self.app.route('/')
        def index():
            auth_check = require_auth()
            if auth_check:
                return auth_check
            
            user = get_current_user()
            if user:
                return redirect(url_for('dashboard'))
            return redirect(url_for('login'))

        @self.app.route('/login', methods=['GET', 'POST'])
        def login():
            if request.method == 'POST':
                username = request.form.get('username')
                password = request.form.get('password')
                
                if username and password:
                    user = self.osint_searcher.db.get_user_by_credentials(username, password)
                    if user:
                        session['authenticated'] = True
                        session['user_data'] = user
                        
                        # Actualizar último login
                        conn = sqlite3.connect(self.osint_searcher.db.db_path)
                        cursor = conn.cursor()
                        cursor.execute('UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?', (user['id'],))
                        conn.commit()
                        conn.close()
                        
                        flash('¡Bienvenido! Has iniciado sesión correctamente.', 'success')
                        return redirect(url_for('dashboard'))
                    else:
                        flash('Credenciales incorrectas. Por favor, inténtalo de nuevo.', 'error')
                else:
                    flash('Por favor, completa todos los campos.', 'error')
            
            return render_template('login.html')

        @self.app.route('/register', methods=['GET', 'POST'])
        def register():
            if request.method == 'POST':
                username = request.form.get('username')
                email = request.form.get('email')
                password = request.form.get('password')
                confirm_password = request.form.get('confirm_password')
                full_name = request.form.get('full_name', '')
                
                if not all([username, email, password, confirm_password]):
                    flash('Por favor, completa todos los campos obligatorios.', 'error')
                elif password != confirm_password:
                    flash('Las contraseñas no coinciden.', 'error')
                elif not password or len(password) < 6:
                    flash('La contraseña debe tener al menos 6 caracteres.', 'error')
                else:
                    # Ensure all required fields are strings, not None
                    if username and email and password and isinstance(username, str) and isinstance(email, str) and isinstance(password, str):
                        if self.osint_searcher.db.register_user(username, email, password, full_name or ''):
                            flash('¡Registro exitoso! Ya puedes iniciar sesión.', 'success')
                            return redirect(url_for('login'))
                        else:
                            flash('Error en el registro. El usuario o email ya existe.', 'error')
                    else:
                        flash('Error en los datos proporcionados.', 'error')
            
            return render_template('register.html')

        @self.app.route('/logout')
        def logout():
            session.clear()
            flash('Has cerrado sesión correctamente.', 'info')
            return redirect(url_for('login'))

        @self.app.route('/dashboard')
        def dashboard():
            auth_check = require_auth()
            if auth_check:
                return auth_check
            
            user = get_current_user()
            if not user:
                return redirect(url_for('login'))
            
            # Obtener estadísticas del usuario
            recent_searches = self.osint_searcher.db.get_user_searches(user['id'], 10)
            report_configs = self.osint_searcher.db.get_user_report_configs(user['id'])
            
            # Generar estadísticas básicas para el dashboard
            stats = {
                'high_risk_findings': 0,
                'medium_risk_findings': 0,
                'low_risk_findings': 0,
                'total_searches': len(recent_searches) if recent_searches else 0
            }
            
            # Calcular estadísticas de riesgo basadas en las búsquedas recientes
            if recent_searches:
                for search in recent_searches:
                    # Simulación de análisis de riesgo basado en el tipo de búsqueda
                    search_type = search.get('search_type', 'basic') if isinstance(search, dict) else getattr(search, 'search_type', 'basic')
                    if search_type in ['advanced', 'government']:
                        stats['high_risk_findings'] += 1
                    elif search_type in ['business', 'news']:
                        stats['medium_risk_findings'] += 1
                    else:
                        stats['low_risk_findings'] += 1
            
            return render_template('dashboard.html', 
                                 user=user, 
                                 recent_searches=recent_searches,
                                 report_configs=report_configs,
                                 stats=stats)

        @self.app.route('/search')
        def search_page():
            auth_check = require_auth()
            if auth_check:
                return auth_check
            
            user = get_current_user()
            return render_template('search.html', user=user)

        @self.app.route('/profile')
        def profile():
            auth_check = require_auth()
            if auth_check:
                return auth_check
            
            user = get_current_user()
            return render_template('profile.html', user=user)

        @self.app.route('/api/ai_search', methods=['POST'])
        def api_ai_search():
            auth_check = require_auth()
            if auth_check and self.config.web_auth_enabled: # Proteger endpoint si la autenticación está habilitada
                return jsonify({'error': 'No autorizado'}), 401

            if not AI_CORE_AVAILABLE:
                return jsonify({'error': 'El módulo de IA no está disponible.'}), 503

            try:
                data = request.get_json()
                user_prompt = data.get('prompt', '').strip()

                if not user_prompt:
                    return jsonify({'error': 'Prompt requerido'}), 400

                user = get_current_user()
                user_id = user['id'] if user else 1 # Asignar un user_id por defecto si no hay sesión

                logger.info(f"AI Search: Recibido prompt de user_id {user_id}: '{user_prompt}'")

                # 1. Interpretar el prompt
                interpretation = ai_core.interpret_prompt_for_osint(user_prompt)
                logger.debug(f"AI Search: Interpretación: {interpretation}")
                if interpretation.get("error"):
                    return jsonify({'error': f"Error de interpretación de IA: {interpretation['error']}", 'details': interpretation.get('raw_response')}), 500

                # Añadir user_id a specific_details para que la orquestación lo use si es necesario
                interpretation.setdefault("specific_details", {})["user_id"] = user_id

                # 2. Orquestar la búsqueda OSINT
                # La instancia de osint_searcher ya está disponible como self.osint_searcher
                raw_osint_results = ai_core.orchestrate_osint_search(interpretation, self.osint_searcher)
                logger.debug(f"AI Search: Resultados crudos OSINT: {raw_osint_results[:2]}") # Loguear solo una muestra

                # Verificar si hubo error en la orquestación
                if raw_osint_results and isinstance(raw_osint_results, list) and raw_osint_results[0].get("error"):
                     return jsonify({'error': f"Error durante la búsqueda OSINT: {raw_osint_results[0]['error']}"}), 500

                # 3. Generar el resumen/reporte con IA
                summary = ai_core.generate_osint_report_summary(raw_osint_results, user_prompt, interpretation)
                logger.debug(f"AI Search: Resumen generado: {summary[:200]}...") # Loguear inicio del resumen

                # Guardar la búsqueda y los resultados (simplificado por ahora)
                # Podríamos crear un nuevo tipo de 'search' o 'report' en la BD para esto.
                # Por ahora, guardamos el prompt como query y el resumen como parte de la descripción del primer resultado.

                # search_id = self.osint_searcher.db.save_search(query=f"AI Prompt: {user_prompt[:100]}", search_type="ai_assisted", user_id=user_id)
                # self.osint_searcher.db.save_results(search_id, [{
                #     "source": "ai_summary",
                #     "title": f"Resumen de IA para: {interpretation.get('main_target', 'Prompt')}",
                #     "description": summary,
                #     "content": json.dumps({"interpretation": interpretation, "raw_results_sample": raw_osint_results[:5]}), # Guardar muestra
                #     "risk_level": "info"
                # }])


                return jsonify({
                    'success': True,
                    'interpretation': interpretation,
                    'summary': summary,
                    'raw_results_sample': raw_osint_results[:10] # Devolver una muestra de resultados crudos
                })

            except Exception as e:
                logger.error(f"Error en API AI search: {str(e)}", exc_info=True)
                return jsonify({'error': f'Error interno del servidor procesando la solicitud de IA: {str(e)}'}), 500

        @self.app.route('/reports')
        def reports():
            auth_check = require_auth()
            if auth_check:
                return auth_check
            
            user = get_current_user()
            if not user:
                return redirect(url_for('login'))
            
            report_configs = self.osint_searcher.db.get_user_report_configs(user['id'])
            return render_template('reports.html', user=user, report_configs=report_configs)

        @self.app.route('/api/search', methods=['POST'])
        def api_search():
            auth_check = require_auth()
            if auth_check and self.config.web_auth_enabled:
                return jsonify({'error': 'No autorizado'}), 401
            
            try:
                data = request.get_json()
                query = data.get('query', '').strip()
                search_type = data.get('search_type', 'general')
                enable_dorking = data.get('enable_dorking', False)
                additional_data = data.get('additional_data', {})
                
                if not query:
                    return jsonify({'error': 'Query requerida'}), 400
                
                user = get_current_user()
                user_id = user['id'] if user else 1
                
                # Construir query específico según el tipo de búsqueda
                search_query = query
                
                if search_type == 'person':
                    # Mejorar query para búsqueda de personas
                    person_id = data.get('personId', '')
                    email = data.get('email', '')
                    phone = data.get('phone', '')
                    city = data.get('city', '')
                    
                    if person_id:
                        search_query += f' {person_id}'
                    if email:
                        search_query += f' {email}'
                    if phone:
                        search_query += f' {phone}'
                    if city:
                        search_query += f' {city}'
                
                elif search_type == 'business':
                    # Mejorar query para búsqueda de empresas
                    nit = data.get('nit', '')
                    city = data.get('city', '')
                    
                    if nit:
                        search_query += f' NIT {nit}'
                    if city:
                        search_query += f' {city}'
                
                elif search_type == 'vehicle':
                    # Búsqueda específica de vehículos
                    vehicle_type = data.get('vehicleType', '')
                    brand = data.get('brand', '')
                    model = data.get('model', '')
                    
                    if vehicle_type:
                        search_query += f' {vehicle_type}'
                    if brand:
                        search_query += f' {brand}'
                    if model:
                        search_query += f' {model}'
                
                elif search_type == 'contact':
                    # Búsqueda de contactos (email, teléfono, etc.)
                    contact_email = data.get('email', '')
                    contact_phone = data.get('phone', '')
                    username = data.get('username', '')
                    domain = data.get('domain', '')
                    ip = data.get('ip', '')
                    
                    if contact_email:
                        search_query = contact_email
                    elif contact_phone:
                        search_query = contact_phone
                    elif username:
                        search_query = username
                    elif domain:
                        search_query = domain
                    elif ip:
                        search_query = ip
                
                elif search_type == 'news':
                    # Búsqueda en noticias con filtros
                    region = data.get('region', '')
                    if region:
                        search_query += f' {region}'
                
                elif search_type == 'government':
                    # Búsqueda en registros gubernamentales
                    record_type = data.get('recordType', '')
                    if record_type and record_type != 'all':
                        search_query += f' {record_type}'
                
                # Realizar la búsqueda
                results = self.osint_searcher.search(search_query, search_type, enable_dorking, user_id)
                
                # Enriquecer resultados con información específica del tipo de búsqueda
                enriched_results = []
                for result in results:
                    if isinstance(result, dict):
                        enriched_result = result.copy()
                    else:
                        # Si el result no es un dict, crear uno básico
                        enriched_result = {
                            'title': str(result),
                            'url': '',
                            'description': '',
                            'source': 'unknown'
                        }
                    
                    # Asignar nivel de riesgo basado en el tipo de búsqueda y fuente
                    if search_type in ['government', 'judicial']:
                        enriched_result['risk_level'] = 'high'
                    elif search_type in ['person', 'contact']:
                        enriched_result['risk_level'] = 'medium'
                    else:
                        enriched_result['risk_level'] = 'low'
                    
                    # Añadir metadatos específicos
                    enriched_result['search_type'] = search_type
                    enriched_result['timestamp'] = datetime.now().isoformat()
                    
                    enriched_results.append(enriched_result)
                
                return jsonify({
                    'success': True,
                    'data': enriched_results,
                    'search_type': search_type,
                    'query': search_query
                })
                
            except Exception as e:
                logger.error(f"Error en API search: {str(e)}")
                return jsonify({'error': str(e)}), 500

        @self.app.route('/api/save_report_config', methods=['POST'])
        def api_save_report_config():
            auth_check = require_auth()
            if auth_check and self.config.web_auth_enabled:
                return jsonify({'error': 'No autorizado'}), 401
            
            try:
                user = get_current_user()
                if not user:
                    return jsonify({'error': 'Usuario no autenticado'}), 401
                
                data = request.get_json()
                
                # Validar datos requeridos
                if not data.get('report_name'):
                    return jsonify({'error': 'Nombre del reporte requerido'}), 400
                
                success = self.osint_searcher.db.save_user_report_config(user['id'], data)
                
                if success:
                    return jsonify({'success': True, 'message': 'Configuración guardada correctamente'})
                else:
                    return jsonify({'error': 'Error guardando configuración'}), 500
                
            except Exception as e:
                logger.error(f"Error guardando configuración: {str(e)}")
                return jsonify({'error': str(e)}), 500

        @self.app.route('/api/generate_report/<int:config_id>', methods=['POST'])
        def api_generate_report(config_id):
            auth_check = require_auth()
            if auth_check and self.config.web_auth_enabled:
                return jsonify({'error': 'No autorizado'}), 401
            
            try:
                user = get_current_user()
                if not user:
                    return jsonify({'error': 'Usuario no autenticado'}), 401
                
                report = self.osint_searcher.db.generate_user_report(user['id'], config_id)
                
                if report:
                    return jsonify({
                        'success': True,
                        'report': report,
                        'message': 'Reporte generado correctamente'
                    })
                else:
                    return jsonify({'error': 'Error generando reporte'}), 500
                
            except Exception as e:
                logger.error(f"Error generando reporte: {str(e)}")
                return jsonify({'error': str(e)}), 500

        @self.app.route('/api/dork_campaign', methods=['POST'])
        def api_dork_campaign():
            auth_check = require_auth()
            if auth_check and self.config.web_auth_enabled:
                return jsonify({'error': 'No autorizado'}), 401
            
            try:
                data = request.get_json()
                target = data.get('target', '').strip()
                categories = data.get('categories', ['general'])
                
                if not target:
                    return jsonify({'error': 'Target requerido'}), 400
                
                results = self.osint_searcher.dorking_engine.execute_dork_campaign(target, categories)
                
                return jsonify({
                    'success': True,
                    'data': results
                })
                
            except Exception as e:
                logger.error(f"Error en dork campaign: {str(e)}")
                return jsonify({'error': str(e)}), 500

        @self.app.route('/api/dashboard/stats')
        def api_dashboard_stats():
            auth_check = require_auth()
            if auth_check:
                return jsonify({'error': 'No autorizado'}), 401
            
            try:
                user = get_current_user()
                if not user:
                    return jsonify({'error': 'Usuario no encontrado'}), 404
                
                # Obtener búsquedas recientes para calcular estadísticas reales
                recent_searches = self.osint_searcher.db.get_user_searches(user['id'], 100)
                
                # Calcular estadísticas reales
                risk_stats = {'high': 0, 'medium': 0, 'low': 0}
                
                # Calcular actividad por días de la semana
                activity_data = [0, 0, 0, 0, 0, 0, 0]  # Lun-Dom
                
                # Calcular búsquedas por tipo/región
                region_data = {'bogota': 0, 'medellin': 0, 'cali': 0, 'barranquilla': 0, 'otros': 0}
                
                if recent_searches:
                    for search in recent_searches:
                        search_type = search.get('search_type', 'basic') if isinstance(search, dict) else getattr(search, 'search_type', 'basic')
                        
                        # Clasificar por riesgo
                        if search_type in ['advanced', 'government', 'judicial']:
                            risk_stats['high'] += 1
                        elif search_type in ['business', 'news', 'academic']:
                            risk_stats['medium'] += 1
                        else:
                            risk_stats['low'] += 1
                        
                        # Calcular actividad por día (simulación básica)
                        try:
                            if hasattr(search, 'timestamp') or 'timestamp' in search:
                                timestamp = search.get('timestamp') if isinstance(search, dict) else search.timestamp
                                if timestamp:
                                    # Parsear timestamp y obtener día de la semana
                                    from datetime import datetime
                                    if isinstance(timestamp, str):
                                        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                                    else:
                                        dt = timestamp
                                    weekday = dt.weekday()  # 0=Lunes, 6=Domingo
                                    activity_data[weekday] += 1
                        except:
                            pass
                        
                        # Clasificar por región basado en el query
                        query = search.get('query', '') if isinstance(search, dict) else getattr(search, 'query', '')
                        query_lower = query.lower()
                        
                        if any(word in query_lower for word in ['bogotá', 'bogota', 'cundinamarca']):
                            region_data['bogota'] += 1
                        elif any(word in query_lower for word in ['medellín', 'medellin', 'antioquia']):
                            region_data['medellin'] += 1
                        elif any(word in query_lower for word in ['cali', 'valle']):
                            region_data['cali'] += 1
                        elif any(word in query_lower for word in ['barranquilla', 'atlántico', 'atlantico']):
                            region_data['barranquilla'] += 1
                        else:
                            region_data['otros'] += 1
                
                return jsonify({
                    'success': True,
                    'risk_stats': risk_stats,
                    'activity_data': activity_data,
                    'region_data': list(region_data.values())
                })
                
            except Exception as e:
                logger.error(f"Error en API dashboard stats: {str(e)}")
                return jsonify({'error': str(e)}), 500

        @self.app.route('/history')
        def history():
            auth_check = require_auth()
            if auth_check:
                return auth_check
            
            user = get_current_user()
            if not user:
                return redirect(url_for('login'))
            
            user_searches = self.osint_searcher.db.get_user_searches(user['id'], 50)
            return render_template('history.html', user=user, searches=user_searches)

        @self.app.route('/admin')
        def admin():
            auth_check = require_auth()
            if auth_check:
                return auth_check
            
            user = get_current_user()
            if not user or user.get('role') != 'admin':
                flash('Acceso denegado. Se requieren permisos de administrador.', 'error')
                return redirect(url_for('dashboard'))
            
            # Obtener estadísticas del sistema
            conn = sqlite3.connect(self.osint_searcher.db.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM users')
            total_users = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM searches')
            total_searches = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM user_report_configs')
            total_reports = cursor.fetchone()[0]
            
            conn.close()
            
            return render_template('admin.html', 
                                 user=user,
                                 total_users=total_users,
                                 total_searches=total_searches,
                                 total_reports=total_reports)

        @self.app.route('/test')
        def test():
            """Ruta de prueba para verificar configuración"""
            return jsonify({
                'auth_enabled': self.config.web_auth_enabled,
                'username': self.config.web_username,
                'has_password': bool(getattr(self.config, 'web_password', False)),
                'has_password_hash': bool(self.config.web_password_hash),
                'session_authenticated': session.get('authenticated', False),
                'current_user': session.get('user_data', {}).get('username', 'No user')
            })

        @self.app.errorhandler(404)
        def not_found(error):
            return render_template('error.html', 
                                 error_code=404,
                                 error_message="Página no encontrada",
                                 user=get_current_user()), 404

        @self.app.errorhandler(500)
        def internal_error(error):
            return render_template('error.html', 
                                 error_code=500,
                                 error_message="Error interno del servidor",
                                 user=get_current_user()), 500

        @self.app.route('/favicon.ico')
        def favicon():
            return send_file('static/favicon.ico', mimetype='image/vnd.microsoft.icon')

def create_config_from_json(config_path: str) -> OSINTConfig:
    """Crea configuración desde archivo JSON"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        config = OSINTConfig()
        for key, value in data.items():
            if hasattr(config, key) and not key.startswith('_'):
                setattr(config, key, value)
        
        # Generar hash de contraseña si es necesario
        if hasattr(config, 'web_password') and config.web_password and not config.web_password_hash:
            config.web_password_hash = generate_password_hash(config.web_password)
        
        return config
    except Exception as e:
        logger.error(f"Error cargando configuración: {str(e)}")
        return OSINTConfig()

def main():
    """Función principal del servidor MCP mejorado"""
    
    # Crear configuración de ejemplo si no existe
    config_path = "osint_config.json"
    if not os.path.exists(config_path):
        example_config = {
            "email_smtp_server": "smtp.gmail.com",
            "email_smtp_port": 587,
            "email_username": "",
            "email_password": "",
            "email_recipients": [],
            "web_interface_enabled": True,
            "web_port": 5000,
            "web_host": "localhost",
            "web_auth_enabled": True,
            "web_username": "admin",
            "enable_domain_analysis": True,
            "enable_ip_analysis": True,
            "max_results_per_source": 20,
            "rate_limit_delay": 2.0
        }
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(example_config, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Archivo de configuración creado: {config_path}")
    
    # Cargar configuración
    config = create_config_from_json(config_path)
    
    # Crear instancias principales
    osint_searcher = EnhancedOSINTSearcher(config)
    
    # Iniciar interfaz web si está habilitada
    if config.web_interface_enabled:
        web_interface = FlaskWebInterface(osint_searcher, config)
        
        logger.info(f"🚀 Iniciando servidor web en http://{config.web_host}:{config.web_port}")
        logger.info(f"👤 Usuario: {config.web_username}")
        if hasattr(config, 'web_password') and config.web_password:
            logger.info(f"🔑 Contraseña: {config.web_password}")
        else:
            logger.info(f"🔑 Contraseña por defecto: admin123")
        
        web_interface.app.run(
            host=config.web_host,
            port=config.web_port,
            debug=False
        )
    else:
        logger.info("Interfaz web deshabilitada. Ejecutando en modo API.")

if __name__ == "__main__":
    main()
