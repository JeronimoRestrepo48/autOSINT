#!/usr/bin/env python3
"""
Módulo OSINT especializado para Colombia
Incluye fuentes de información gubernamentales, medios de comunicación y bases de datos públicas
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
import re
from bs4 import BeautifulSoup
import logging

class ColombiaOSINT:
    """
    Clase para realizar búsquedas OSINT específicas para Colombia
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Fuentes gubernamentales colombianas
        self.government_sources = {
            'registraduria': 'https://www.registraduria.gov.co',
            'runt': 'https://www.runt.com.co',
            'supersociedades': 'https://www.supersociedades.gov.co',
            'dane': 'https://www.dane.gov.co',
            'procuraduria': 'https://www.procuraduria.gov.co',
            'contraloria': 'https://www.contraloria.gov.co',
            'fiscalia': 'https://www.fiscalia.gov.co',
            'policia': 'https://www.policia.gov.co'
        }
        
        # Medios de comunicación colombianos
        self.media_sources = {
            'el_tiempo': 'https://www.eltiempo.com',
            'el_espectador': 'https://www.elespectador.com',
            'semana': 'https://www.semana.com',
            'caracol_radio': 'https://www.caracol.com.co',
            'rcn_radio': 'https://www.rcnradio.com',
            'blu_radio': 'https://www.bluradio.com',
            'w_radio': 'https://www.wradio.com.co',
            'la_fm': 'https://www.lafm.com.co',
            'publimetro': 'https://www.publimetro.co',
            'city_tv': 'https://www.citytv.com.co'
        }
        
        # Cámaras de comercio principales
        self.commerce_chambers = {
            'bogota': 'https://www.ccb.org.co',
            'medellin': 'https://www.camaramedellin.com.co',
            'cali': 'https://www.ccc.org.co',
            'barranquilla': 'https://www.camarabaq.org.co',
            'cartagena': 'https://www.cccartagena.org.co',
            'bucaramanga': 'https://www.camaradirecta.com',
            'manizales': 'https://www.ccm.org.co',
            'pereira': 'https://www.camarapereira.org.co'
        }
        
        # Universidades colombianas
        self.universities = {
            'nacional': 'https://www.unal.edu.co',
            'andes': 'https://www.uniandes.edu.co',
            'javeriana': 'https://www.javeriana.edu.co',
            'externado': 'https://www.uexternado.edu.co',
            'rosario': 'https://www.urosario.edu.co',
            'pontificia_bolivariana': 'https://www.upb.edu.co',
            'eafit': 'https://www.eafit.edu.co',
            'del_valle': 'https://www.univalle.edu.co',
            'antioquia': 'https://www.udea.edu.co',
            'icesi': 'https://www.icesi.edu.co'
        }
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def search_person(self, nombre: str, apellido: str, cedula: Optional[str] = None, 
                      ciudad: Optional[str] = None, telefono: Optional[str] = None) -> Dict[str, Any]:
        """
        Búsqueda completa de una persona en Colombia
        """
        results = {
            'query': f"{nombre} {apellido}",
            'timestamp': datetime.now().isoformat(),
            'person_data': {
                'nombre': nombre,
                'apellido': apellido,
                'cedula': cedula,
                'ciudad': ciudad,
                'telefono': telefono
            },
            'sources': {},
            'findings': [],
            'risk_level': 'low'
        }
        
        try:
            # Búsqueda en medios de comunicación
            media_results = self._search_in_media(f"{nombre} {apellido}", ciudad)
            results['sources']['media'] = media_results
            
            # Búsqueda en redes sociales
            social_results = self._search_social_media(nombre, apellido, ciudad)
            results['sources']['social'] = social_results
            
            # Búsqueda en bases de datos académicas
            academic_results = self._search_academic_databases(nombre, apellido)
            results['sources']['academic'] = academic_results
            
            # Búsqueda en registros comerciales
            if ciudad:
                commercial_results = self._search_commercial_records(nombre, apellido, ciudad)
                results['sources']['commercial'] = commercial_results
            
            # Análisis de riesgo
            results['risk_level'] = self._analyze_risk_level(results)
            
            # Consolidar hallazgos
            results['findings'] = self._consolidate_findings(results)
            
        except Exception as e:
            self.logger.error(f"Error en búsqueda de persona: {str(e)}")
            results['error'] = str(e)
            
        return results

    def search_business(self, nombre_empresa: str, nit: Optional[str] = None, 
                       ciudad: Optional[str] = None) -> Dict[str, Any]:
        """
        Búsqueda de información empresarial en Colombia
        """
        results = {
            'query': nombre_empresa,
            'timestamp': datetime.now().isoformat(),
            'business_data': {
                'nombre': nombre_empresa,
                'nit': nit,
                'ciudad': ciudad
            },
            'sources': {},
            'findings': [],
            'risk_level': 'low'
        }
        
        try:
            # Búsqueda en Superintendencia de Sociedades
            supersociedades_results = self._search_supersociedades(nombre_empresa, nit)
            results['sources']['supersociedades'] = supersociedades_results
            
            # Búsqueda en Cámaras de Comercio
            if ciudad:
                chamber_results = self._search_commerce_chamber(nombre_empresa, ciudad)
                results['sources']['chamber'] = chamber_results
            
            # Búsqueda en medios de comunicación
            media_results = self._search_in_media(nombre_empresa, ciudad)
            results['sources']['media'] = media_results
            
            # Búsqueda de sanciones y multas
            sanctions_results = self._search_sanctions(nombre_empresa, nit)
            results['sources']['sanctions'] = sanctions_results
            
            # Análisis de riesgo
            results['risk_level'] = self._analyze_business_risk(results)
            
            # Consolidar hallazgos
            results['findings'] = self._consolidate_findings(results)
            
        except Exception as e:
            self.logger.error(f"Error en búsqueda empresarial: {str(e)}")
            results['error'] = str(e)
            
        return results

    def search_news(self, query: str, days_back: int = 30, 
                   region: Optional[str] = None) -> Dict[str, Any]:
        """
        Búsqueda en medios de comunicación colombianos
        """
        results = {
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'search_params': {
                'days_back': days_back,
                'region': region
            },
            'sources': {},
            'articles': [],
            'risk_level': 'low'
        }
        
        try:
            # Búsqueda en cada medio
            for media_name, media_url in self.media_sources.items():
                try:
                    articles = self._search_media_outlet(media_url, query, days_back)
                    if articles:
                        results['sources'][media_name] = articles
                        results['articles'].extend(articles)
                except Exception as e:
                    self.logger.error(f"Error buscando en {media_name}: {str(e)}")
                    
            # Filtrar por región si se especifica
            if region:
                results['articles'] = [
                    article for article in results['articles']
                    if region.lower() in article.get('content', '').lower()
                ]
            
            # Análisis de riesgo basado en contenido
            results['risk_level'] = self._analyze_news_risk(results['articles'])
            
        except Exception as e:
            self.logger.error(f"Error en búsqueda de noticias: {str(e)}")
            results['error'] = str(e)
            
        return results

    def search_government_records(self, query: str, record_type: str = 'all') -> Dict[str, Any]:
        """
        Búsqueda en registros gubernamentales
        """
        results = {
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'record_type': record_type,
            'sources': {},
            'findings': [],
            'risk_level': 'low'
        }
        
        try:
            if record_type in ['all', 'procuraduria']:
                # Búsqueda en Procuraduría (sanciones disciplinarias)
                proc_results = self._search_procuraduria(query)
                results['sources']['procuraduria'] = proc_results
                
            if record_type in ['all', 'contraloria']:
                # Búsqueda en Contraloría (responsabilidad fiscal)
                cont_results = self._search_contraloria(query)
                results['sources']['contraloria'] = cont_results
                
            if record_type in ['all', 'fiscalia']:
                # Búsqueda en Fiscalía (procesos penales)
                fisc_results = self._search_fiscalia(query)
                results['sources']['fiscalia'] = fisc_results
                
            if record_type in ['all', 'policia']:
                # Búsqueda en Policía Nacional
                pol_results = self._search_policia(query)
                results['sources']['policia'] = pol_results
                
            # Análisis de riesgo
            results['risk_level'] = self._analyze_government_risk(results)
            
            # Consolidar hallazgos
            results['findings'] = self._consolidate_findings(results)
            
        except Exception as e:
            self.logger.error(f"Error en búsqueda gubernamental: {str(e)}")
            results['error'] = str(e)
            
        return results

    def _search_in_media(self, query: str, location: Optional[str] = None) -> List[Dict]:
        """Búsqueda en medios de comunicación"""
        articles = []
        
        for media_name, media_url in self.media_sources.items():
            try:
                media_articles = self._search_media_outlet(media_url, query, 30)
                if media_articles:
                    articles.extend(media_articles)
            except Exception as e:
                self.logger.error(f"Error buscando en {media_name}: {str(e)}")
                
        return articles

    def _search_media_outlet(self, base_url: str, query: str, days_back: int) -> List[Dict]:
        """Búsqueda en un medio específico"""
        articles = []
        
        try:
            # Implementar búsqueda específica por medio
            # Esto sería personalizado para cada sitio web
            search_url = f"{base_url}/buscar?q={query}"
            
            response = self.session.get(search_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extraer artículos (esto varía por sitio)
                article_elements = soup.find_all(['article', 'div'], class_=re.compile(r'(article|noticia|news)'))
                
                for element in article_elements[:5]:  # Limitar a 5 resultados por medio
                    try:
                        from bs4 import Tag
                        if isinstance(element, Tag):
                            title = element.find(['h1', 'h2', 'h3', 'h4'])
                            title_text = title.get_text(strip=True) if title and hasattr(title, 'get_text') and not isinstance(title, int) else "Sin título"
                            
                            link = element.find('a')
                            from bs4 import Tag
                            if link and isinstance(link, Tag) and link.get('href'):
                                article_url = str(link.get('href'))
                                if article_url and not article_url.startswith('http'):
                                    article_url = base_url + article_url
                            else:
                                article_url = ""
                                
                            content = element.get_text(strip=True)[:500]
                            
                            articles.append({
                                'title': title_text,
                                'url': article_url,
                                'content': content,
                                'source': base_url,
                                'timestamp': datetime.now().isoformat()
                            })
                        
                    except Exception as e:
                        self.logger.error(f"Error extrayendo artículo: {str(e)}")
                        
            time.sleep(1)  # Respetar límites de velocidad
            
        except Exception as e:
            self.logger.error(f"Error buscando en {base_url}: {str(e)}")
            
        return articles

    def _search_social_media(self, nombre: str, apellido: str, ciudad: Optional[str] = None) -> List[Dict]:
        """Búsqueda en redes sociales (simulada)"""
        # En una implementación real, esto usaría APIs de redes sociales
        return [
            {
                'platform': 'Facebook',
                'profile_url': f"https://facebook.com/search?q={nombre}+{apellido}",
                'found': True,
                'risk_indicators': []
            },
            {
                'platform': 'Twitter',
                'profile_url': f"https://twitter.com/search?q={nombre}+{apellido}",
                'found': True,
                'risk_indicators': []
            },
            {
                'platform': 'LinkedIn',
                'profile_url': f"https://linkedin.com/search/results/people/?keywords={nombre}+{apellido}",
                'found': True,
                'risk_indicators': []
            }
        ]

    def _search_academic_databases(self, nombre: str, apellido: str) -> List[Dict]:
        """Búsqueda en bases de datos académicas"""
        results = []
        
        for univ_name, univ_url in self.universities.items():
            try:
                # Simular búsqueda en directorio académico
                results.append({
                    'university': univ_name,
                    'url': univ_url,
                    'found': False,  # En implementación real, hacer búsqueda real
                    'publications': [],
                    'affiliations': []
                })
            except Exception as e:
                self.logger.error(f"Error buscando en {univ_name}: {str(e)}")
                
        return results

    def _search_commercial_records(self, nombre: str, apellido: str, ciudad: str) -> List[Dict]:
        """Búsqueda en registros comerciales"""
        results = []
        
        # Buscar en cámara de comercio de la ciudad
        if ciudad.lower() in self.commerce_chambers:
            chamber_url = self.commerce_chambers[ciudad.lower()]
            try:
                results.append({
                    'chamber': ciudad,
                    'url': chamber_url,
                    'found': False,  # En implementación real, hacer búsqueda real
                    'businesses': []
                })
            except Exception as e:
                self.logger.error(f"Error buscando en cámara de {ciudad}: {str(e)}")
                
        return results

    def _search_supersociedades(self, nombre_empresa: str, nit: Optional[str] = None) -> Dict:
        """Búsqueda en Superintendencia de Sociedades"""
        return {
            'source': 'Superintendencia de Sociedades',
            'url': self.government_sources['supersociedades'],
            'found': False,  # En implementación real, hacer búsqueda real
            'company_data': {},
            'financial_data': {},
            'legal_status': {}
        }

    def _search_commerce_chamber(self, nombre_empresa: str, ciudad: str) -> Dict:
        """Búsqueda en Cámara de Comercio"""
        chamber_url = self.commerce_chambers.get(ciudad.lower(), '')
        return {
            'chamber': ciudad,
            'url': chamber_url,
            'found': False,  # En implementación real, hacer búsqueda real
            'registration_data': {},
            'renewals': [],
            'representatives': []
        }

    def _search_sanctions(self, nombre_empresa: str, nit: Optional[str] = None) -> List[Dict]:
        """Búsqueda de sanciones y multas"""
        return [
            {
                'entity': 'Superintendencia de Industria y Comercio',
                'sanctions': [],
                'fines': []
            },
            {
                'entity': 'Superintendencia Financiera',
                'sanctions': [],
                'fines': []
            }
        ]

    def _search_procuraduria(self, query: str) -> Dict:
        """Búsqueda en Procuraduría General"""
        return {
            'source': 'Procuraduría General',
            'url': self.government_sources['procuraduria'],
            'disciplinary_sanctions': [],
            'investigations': []
        }

    def _search_contraloria(self, query: str) -> Dict:
        """Búsqueda en Contraloría General"""
        return {
            'source': 'Contraloría General',
            'url': self.government_sources['contraloria'],
            'fiscal_responsibility': [],
            'audits': []
        }

    def _search_fiscalia(self, query: str) -> Dict:
        """Búsqueda en Fiscalía General"""
        return {
            'source': 'Fiscalía General',
            'url': self.government_sources['fiscalia'],
            'criminal_cases': [],
            'investigations': []
        }

    def _search_policia(self, query: str) -> Dict:
        """Búsqueda en Policía Nacional"""
        return {
            'source': 'Policía Nacional',
            'url': self.government_sources['policia'],
            'police_records': [],
            'wanted_lists': []
        }

    def _analyze_risk_level(self, results: Dict) -> str:
        """Análisis de nivel de riesgo para personas"""
        risk_score = 0
        
        # Evaluar presencia en medios
        if results['sources'].get('media'):
            media_count = len(results['sources']['media'])
            if media_count > 5:
                risk_score += 2
            elif media_count > 0:
                risk_score += 1
                
        # Evaluar presencia en redes sociales
        if results['sources'].get('social'):
            social_platforms = len(results['sources']['social'])
            if social_platforms > 3:
                risk_score += 1
                
        # Determinar nivel de riesgo
        if risk_score >= 3:
            return 'high'
        elif risk_score >= 1:
            return 'medium'
        else:
            return 'low'

    def _analyze_business_risk(self, results: Dict) -> str:
        """Análisis de nivel de riesgo para empresas"""
        risk_score = 0
        
        # Evaluar sanciones
        if results['sources'].get('sanctions'):
            for sanction_entity in results['sources']['sanctions']:
                if sanction_entity.get('sanctions') or sanction_entity.get('fines'):
                    risk_score += 3
                    
        # Evaluar presencia en medios (negativa)
        if results['sources'].get('media'):
            media_count = len(results['sources']['media'])
            if media_count > 3:
                risk_score += 2
                
        # Determinar nivel de riesgo
        if risk_score >= 3:
            return 'high'
        elif risk_score >= 1:
            return 'medium'
        else:
            return 'low'

    def _analyze_news_risk(self, articles: List[Dict]) -> str:
        """Análisis de riesgo basado en contenido de noticias"""
        risk_keywords = [
            'corrupción', 'fraude', 'delito', 'investigación', 'captura',
            'condena', 'sanción', 'multa', 'proceso judicial', 'demanda',
            'escándalo', 'irregularidad', 'malversación', 'soborno'
        ]
        
        risk_score = 0
        
        for article in articles:
            content = article.get('content', '').lower()
            title = article.get('title', '').lower()
            
            for keyword in risk_keywords:
                if keyword in content or keyword in title:
                    risk_score += 1
                    
        # Normalizar por número de artículos
        if articles:
            risk_ratio = risk_score / len(articles)
            if risk_ratio > 0.5:
                return 'high'
            elif risk_ratio > 0.2:
                return 'medium'
                
        return 'low'

    def _analyze_government_risk(self, results: Dict) -> str:
        """Análisis de riesgo en registros gubernamentales"""
        risk_score = 0
        
        # Evaluar cada fuente gubernamental
        for source_name, source_data in results['sources'].items():
            if isinstance(source_data, dict):
                # Buscar indicadores de riesgo
                if source_data.get('disciplinary_sanctions'):
                    risk_score += 3
                if source_data.get('criminal_cases'):
                    risk_score += 3
                if source_data.get('fiscal_responsibility'):
                    risk_score += 2
                if source_data.get('investigations'):
                    risk_score += 1
                    
        # Determinar nivel de riesgo
        if risk_score >= 5:
            return 'high'
        elif risk_score >= 2:
            return 'medium'
        else:
            return 'low'

    def _consolidate_findings(self, results: Dict) -> List[Dict]:
        """Consolidar hallazgos de todas las fuentes"""
        findings = []
        
        # Procesar cada fuente
        for source_name, source_data in results['sources'].items():
            if isinstance(source_data, list):
                for item in source_data:
                    if isinstance(item, dict) and item.get('found'):
                        findings.append({
                            'source': source_name,
                            'type': 'match',
                            'description': f"Encontrado en {source_name}",
                            'url': item.get('url', ''),
                            'timestamp': datetime.now().isoformat()
                        })
            elif isinstance(source_data, dict) and source_data.get('found'):
                findings.append({
                    'source': source_name,
                    'type': 'match',
                    'description': f"Encontrado en {source_name}",
                    'url': source_data.get('url', ''),
                    'timestamp': datetime.now().isoformat()
                })
                
        return findings

    def get_available_sources(self) -> Dict[str, List[str]]:
        """Obtener lista de fuentes disponibles"""
        return {
            'government': list(self.government_sources.keys()),
            'media': list(self.media_sources.keys()),
            'commerce': list(self.commerce_chambers.keys()),
            'universities': list(self.universities.keys())
        }

    def get_search_statistics(self) -> Dict[str, Any]:
        """Obtener estadísticas de búsqueda"""
        return {
            'total_sources': len(self.government_sources) + len(self.media_sources) + len(self.commerce_chambers) + len(self.universities),
            'government_sources': len(self.government_sources),
            'media_sources': len(self.media_sources),
            'commerce_sources': len(self.commerce_chambers),
            'academic_sources': len(self.universities),
            'last_updated': datetime.now().isoformat()
        }


# Instancia global del módulo OSINT Colombia
colombia_osint = ColombiaOSINT()
