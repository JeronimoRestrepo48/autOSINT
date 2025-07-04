#!/usr/bin/env python3
"""
OSINT Search Engine - Versión Avanzada con Múltiples Herramientas
Integra todas las herramientas OSINT en una sola plataforma
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import argparse
import time

# Importar módulos OSINT
from osint_advanced import AdvancedOSINTToolkit
from osint_specialized import OSINTSpecializedTools

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/osint_advanced.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class OSINTMasterSearch:
    """Clase principal que integra todas las herramientas OSINT"""
    
    def __init__(self, config_path: str = "osint_config_advanced.json"):
        self.config_path = config_path
        self.config = self.load_config()
        
        # Inicializar herramientas
        self.advanced_toolkit = AdvancedOSINTToolkit()
        self.specialized_tools = OSINTSpecializedTools()
        
        # Crear directorios necesarios
        self.create_directories()
    
    def load_config(self) -> Dict[str, Any]:
        """Carga la configuración desde archivo JSON"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Archivo de configuración no encontrado: {self.config_path}")
            return self.get_default_config()
        except json.JSONDecodeError as e:
            logger.error(f"Error al leer configuración: {e}")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """Retorna configuración por defecto"""
        return {
            "api_keys": {},
            "osint_modules": {
                "subdomain_enumeration": {"enabled": True},
                "network_scanning": {"enabled": True},
                "social_media_search": {"enabled": True},
                "phone_analysis": {"enabled": True},
                "web_archive_search": {"enabled": True},
                "technology_detection": {"enabled": True},
                "company_investigation": {"enabled": True},
                "leak_checking": {"enabled": True},
                "pastebin_search": {"enabled": True},
                "github_investigation": {"enabled": True},
                "certificate_analysis": {"enabled": True},
                "dns_analysis": {"enabled": True},
                "exif_analysis": {"enabled": True}
            }
        }
    
    def create_directories(self):
        """Crea directorios necesarios"""
        directories = ['logs', 'reports', 'exports', 'cache', 'temp']
        for directory in directories:
            Path(directory).mkdir(exist_ok=True)
    
    def search_target(self, target: str, search_type: str = "comprehensive") -> Dict[str, Any]:
        """Búsqueda principal de un objetivo"""
        logger.info(f"Iniciando búsqueda de: {target} - Tipo: {search_type}")
        
        start_time = time.time()
        
        results = {
            'target': target,
            'search_type': search_type,
            'timestamp': datetime.now().isoformat(),
            'modules_executed': [],
            'results': {},
            'summary': {},
            'execution_time': 0
        }
        
        # Determinar tipo de objetivo
        target_type = self.detect_target_type(target)
        logger.info(f"Tipo de objetivo detectado: {target_type}")
        
        # Ejecutar módulos según el tipo de objetivo
        if target_type == 'domain':
            results['results'] = self.search_domain(target)
        elif target_type == 'ip':
            results['results'] = self.search_ip(target)
        elif target_type == 'email':
            results['results'] = self.search_email(target)
        elif target_type == 'username':
            results['results'] = self.search_username(target)
        elif target_type == 'phone':
            results['results'] = self.search_phone(target)
        elif target_type == 'company':
            results['results'] = self.search_company(target)
        else:
            results['results'] = self.search_general(target)
        
        # Generar resumen
        results['summary'] = self.generate_summary(results['results'])
        
        # Calcular tiempo de ejecución
        results['execution_time'] = time.time() - start_time
        
        # Guardar resultados
        self.save_results(results)
        
        logger.info(f"Búsqueda completada en {results['execution_time']:.2f} segundos")
        
        return results
    
    def detect_target_type(self, target: str) -> str:
        """Detecta el tipo de objetivo"""
        import re
        
        # Email
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', target):
            return 'email'
        
        # IP
        if re.match(r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', target):
            return 'ip'
        
        # Dominio
        if re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', target):
            return 'domain'
        
        # Teléfono
        if re.match(r'^[\+]?[1-9][\d]{0,15}$', target.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')):
            return 'phone'
        
        # Username (sin espacios, caracteres especiales limitados)
        if re.match(r'^[a-zA-Z0-9_-]{3,}$', target):
            return 'username'
        
        # Compañía (contiene espacios o es más complejo)
        if ' ' in target or len(target) > 20:
            return 'company'
        
        return 'general'
    
    def search_domain(self, domain: str) -> Dict[str, Any]:
        """Búsqueda completa de dominio"""
        results = {'domain_analysis': {}}
        
        if self.config['osint_modules']['subdomain_enumeration']['enabled']:
            try:
                results['domain_analysis'] = self.advanced_toolkit.comprehensive_domain_analysis(domain)
                logger.info(f"Análisis de dominio completado para: {domain}")
            except Exception as e:
                logger.error(f"Error en análisis de dominio: {e}")
        
        if self.config['osint_modules']['certificate_analysis']['enabled']:
            try:
                results['certificate_analysis'] = self.specialized_tools.certificate_analyzer.analyze_certificate(domain)
                logger.info(f"Análisis de certificado completado para: {domain}")
            except Exception as e:
                logger.error(f"Error en análisis de certificado: {e}")
        
        if self.config['osint_modules']['dns_analysis']['enabled']:
            try:
                results['dns_analysis'] = self.specialized_tools.dns_analyzer.comprehensive_dns_analysis(domain)
                logger.info(f"Análisis DNS completado para: {domain}")
            except Exception as e:
                logger.error(f"Error en análisis DNS: {e}")
        
        return results
    
    def search_ip(self, ip: str) -> Dict[str, Any]:
        """Búsqueda completa de IP"""
        results = {}
        
        if self.config['osint_modules']['network_scanning']['enabled']:
            try:
                results['network_scan'] = self.advanced_toolkit.network_scanner.scan_host(ip)
                logger.info(f"Escaneo de red completado para: {ip}")
            except Exception as e:
                logger.error(f"Error en escaneo de red: {e}")
        
        try:
            results['ip_geolocation'] = self.advanced_toolkit.ip_geolocation(ip)
            logger.info(f"Geolocalización de IP completada para: {ip}")
        except Exception as e:
            logger.error(f"Error en geolocalización: {e}")
        
        return results
    
    def search_email(self, email: str) -> Dict[str, Any]:
        """Búsqueda completa de email"""
        results = {}
        
        if self.config['osint_modules']['leak_checking']['enabled']:
            try:
                results['email_investigation'] = self.specialized_tools.comprehensive_email_investigation(email)
                logger.info(f"Investigación de email completada para: {email}")
            except Exception as e:
                logger.error(f"Error en investigación de email: {e}")
        
        try:
            results['email_analysis'] = self.advanced_toolkit.email_investigation(email)
            logger.info(f"Análisis de email completado para: {email}")
        except Exception as e:
            logger.error(f"Error en análisis de email: {e}")
        
        return results
    
    def search_username(self, username: str) -> Dict[str, Any]:
        """Búsqueda completa de username"""
        results = {}
        
        if self.config['osint_modules']['social_media_search']['enabled']:
            try:
                results['username_investigation'] = self.advanced_toolkit.username_investigation(username)
                logger.info(f"Investigación de username completada para: {username}")
            except Exception as e:
                logger.error(f"Error en investigación de username: {e}")
        
        if self.config['osint_modules']['github_investigation']['enabled']:
            try:
                results['github_investigation'] = self.specialized_tools.github_investigator.investigate_user(username)
                logger.info(f"Investigación de GitHub completada para: {username}")
            except Exception as e:
                logger.error(f"Error en investigación de GitHub: {e}")
        
        return results
    
    def search_phone(self, phone: str) -> Dict[str, Any]:
        """Búsqueda completa de teléfono"""
        results = {}
        
        if self.config['osint_modules']['phone_analysis']['enabled']:
            try:
                results['phone_investigation'] = self.advanced_toolkit.phone_investigation(phone)
                logger.info(f"Investigación de teléfono completada para: {phone}")
            except Exception as e:
                logger.error(f"Error en investigación de teléfono: {e}")
        
        return results
    
    def search_company(self, company: str) -> Dict[str, Any]:
        """Búsqueda completa de empresa"""
        results = {}
        
        if self.config['osint_modules']['company_investigation']['enabled']:
            try:
                results['company_investigation'] = self.advanced_toolkit.company_investigation(company)
                logger.info(f"Investigación de empresa completada para: {company}")
            except Exception as e:
                logger.error(f"Error en investigación de empresa: {e}")
        
        return results
    
    def search_general(self, target: str) -> Dict[str, Any]:
        """Búsqueda general para objetivos no específicos"""
        results = {}
        
        if self.config['osint_modules']['pastebin_search']['enabled']:
            try:
                results['pastebin_search'] = self.specialized_tools.pastebin_searcher.search_pastes(target)
                logger.info(f"Búsqueda en pastebin completada para: {target}")
            except Exception as e:
                logger.error(f"Error en búsqueda de pastebin: {e}")
        
        if self.config['osint_modules']['github_investigation']['enabled']:
            try:
                results['github_code_search'] = self.specialized_tools.github_investigator.search_code(target)
                logger.info(f"Búsqueda de código en GitHub completada para: {target}")
            except Exception as e:
                logger.error(f"Error en búsqueda de código: {e}")
        
        return results
    
    def generate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Genera resumen de resultados"""
        summary = {
            'total_modules': 0,
            'successful_modules': 0,
            'failed_modules': 0,
            'key_findings': [],
            'risk_assessment': 'low',
            'recommendations': []
        }
        
        # Contar módulos
        for module_name, module_results in results.items():
            summary['total_modules'] += 1
            
            if isinstance(module_results, dict) and 'error' not in module_results:
                summary['successful_modules'] += 1
                
                # Extraer hallazgos clave
                if module_name == 'domain_analysis':
                    subdomains = module_results.get('subdomains', [])
                    if subdomains:
                        summary['key_findings'].append(f"Encontrados {len(subdomains)} subdominios")
                
                elif module_name == 'email_investigation':
                    breaches = module_results.get('breach_check', {}).get('total_breaches', 0)
                    if breaches > 0:
                        summary['key_findings'].append(f"Email encontrado en {breaches} filtraciones")
                        summary['risk_assessment'] = 'high'
                
                elif module_name == 'username_investigation':
                    profiles = module_results.get('found_profiles', [])
                    if profiles:
                        summary['key_findings'].append(f"Encontrados {len(profiles)} perfiles sociales")
                
            else:
                summary['failed_modules'] += 1
        
        # Generar recomendaciones
        if summary['risk_assessment'] == 'high':
            summary['recommendations'].extend([
                "Revisar inmediatamente las filtraciones de datos encontradas",
                "Cambiar contraseñas de cuentas comprometidas",
                "Implementar autenticación de dos factores",
                "Monitorear actividad sospechosa en las cuentas"
            ])
        else:
            summary['recommendations'].extend([
                "Revisar periódicamente la exposición de datos",
                "Mantener actualizada la información de seguridad",
                "Configurar alertas para nuevas exposiciones"
            ])
        
        return summary
    
    def save_results(self, results: Dict[str, Any]):
        """Guarda los resultados en archivo JSON"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reports/osint_results_{results['target']}_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False, default=str)
            logger.info(f"Resultados guardados en: {filename}")
        except Exception as e:
            logger.error(f"Error guardando resultados: {e}")
    
    def generate_report(self, results: Dict[str, Any], format: str = 'html') -> str:
        """Genera reporte en formato especificado"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format == 'html':
            return self.generate_html_report(results, timestamp)
        elif format == 'pdf':
            return self.generate_pdf_report(results, timestamp)
        elif format == 'json':
            return self.generate_json_report(results, timestamp)
        else:
            raise ValueError(f"Formato no soportado: {format}")
    
    def generate_html_report(self, results: Dict[str, Any], timestamp: str) -> str:
        """Genera reporte HTML"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Reporte OSINT - {results['target']}</title>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #2c3e50; color: white; padding: 20px; text-align: center; }}
                .summary {{ background-color: #ecf0f1; padding: 15px; margin: 20px 0; }}
                .module {{ border: 1px solid #bdc3c7; margin: 10px 0; padding: 15px; }}
                .key-findings {{ background-color: #f39c12; color: white; padding: 10px; }}
                .recommendations {{ background-color: #27ae60; color: white; padding: 10px; }}
                .risk-high {{ background-color: #e74c3c; color: white; }}
                .risk-medium {{ background-color: #f39c12; color: white; }}
                .risk-low {{ background-color: #27ae60; color: white; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Reporte OSINT</h1>
                <h2>Objetivo: {results['target']}</h2>
                <p>Fecha: {results['timestamp']}</p>
                <p>Tiempo de ejecución: {results.get('execution_time', 0):.2f} segundos</p>
            </div>
            
            <div class="summary">
                <h3>Resumen Ejecutivo</h3>
                <p><strong>Módulos ejecutados:</strong> {results['summary']['total_modules']}</p>
                <p><strong>Exitosos:</strong> {results['summary']['successful_modules']}</p>
                <p><strong>Fallidos:</strong> {results['summary']['failed_modules']}</p>
                <p><strong>Nivel de riesgo:</strong> 
                    <span class="risk-{results['summary']['risk_assessment']}">
                        {results['summary']['risk_assessment'].upper()}
                    </span>
                </p>
            </div>
            
            <div class="key-findings">
                <h3>Hallazgos Clave</h3>
                <ul>
                    {''.join(f"<li>{finding}</li>" for finding in results['summary']['key_findings'])}
                </ul>
            </div>
            
            <div class="recommendations">
                <h3>Recomendaciones</h3>
                <ul>
                    {''.join(f"<li>{rec}</li>" for rec in results['summary']['recommendations'])}
                </ul>
            </div>
            
            <h3>Resultados Detallados</h3>
        """
        
        # Añadir resultados detallados
        for module_name, module_results in results['results'].items():
            html_content += f"""
            <div class="module">
                <h4>{module_name.replace('_', ' ').title()}</h4>
                <pre>{json.dumps(module_results, indent=2, ensure_ascii=False, default=str)}</pre>
            </div>
            """
        
        html_content += """
        </body>
        </html>
        """
        
        filename = f"reports/osint_report_{results['target']}_{timestamp}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filename
    
    def generate_json_report(self, results: Dict[str, Any], timestamp: str) -> str:
        """Genera reporte JSON"""
        filename = f"reports/osint_report_{results['target']}_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        
        return filename

    def generate_pdf_report(self, results: Dict[str, Any], timestamp: str) -> str:
        """Genera reporte PDF (simplemente convierte el HTML a PDF si posible)"""
        try:
            from xhtml2pdf import pisa
        except ImportError:
            logger.error("xhtml2pdf no está instalado. Instale con 'pip install xhtml2pdf'")
            raise ImportError("xhtml2pdf no está instalado. Instale con 'pip install xhtml2pdf'")

        html_file = self.generate_html_report(results, timestamp)
        pdf_file = html_file.replace('.html', '.pdf')

        with open(html_file, 'r', encoding='utf-8') as f_html, open(pdf_file, 'wb') as f_pdf:
            pisa_status = pisa.CreatePDF(f_html.read(), dest=f_pdf)
            # Handle pisa_status for different return types
            status_obj = None
            if hasattr(pisa_status, 'err'):
                status_obj = pisa_status
            elif isinstance(pisa_status, (tuple, list)) and len(pisa_status) > 0 and hasattr(pisa_status[0], 'err'):
                status_obj = pisa_status[0]
            if status_obj is not None and getattr(status_obj, 'err', 0):
                logger.error("Error al generar el PDF del reporte.")
                raise Exception("Error al generar el PDF del reporte.")

        return pdf_file

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description='OSINT Search Engine Avanzado')
    parser.add_argument('target', help='Objetivo a investigar')
    parser.add_argument('--type', choices=['domain', 'ip', 'email', 'username', 'phone', 'company', 'general'], 
                       help='Tipo de objetivo')
    parser.add_argument('--config', default='osint_config_advanced.json', 
                       help='Archivo de configuración')
    parser.add_argument('--format', choices=['html', 'json', 'pdf'], default='html',
                       help='Formato del reporte')
    parser.add_argument('--output', help='Archivo de salida')
    
    args = parser.parse_args()
    
    # Crear instancia del buscador
    osint_search = OSINTMasterSearch(args.config)
    
    # Realizar búsqueda
    results = osint_search.search_target(args.target, args.type or 'comprehensive')
    
    # Generar reporte
    report_file = osint_search.generate_report(results, args.format)
    
    print(f"\n{'='*60}")
    print(f"OSINT SEARCH COMPLETADO")
    print(f"{'='*60}")
    print(f"Objetivo: {args.target}")
    print(f"Tipo: {results['search_type']}")
    print(f"Tiempo de ejecución: {results['execution_time']:.2f} segundos")
    print(f"Módulos exitosos: {results['summary']['successful_modules']}/{results['summary']['total_modules']}")
    print(f"Nivel de riesgo: {results['summary']['risk_assessment'].upper()}")
    print(f"Reporte generado: {report_file}")
    
    if results['summary']['key_findings']:
        print(f"\nHallazgos clave:")
        for finding in results['summary']['key_findings']:
            print(f"  • {finding}")
    
    if results['summary']['recommendations']:
        print(f"\nRecomendaciones:")
        for rec in results['summary']['recommendations']:
            print(f"  • {rec}")
    
    print(f"\n{'='*60}")

if __name__ == "__main__":
    main()
