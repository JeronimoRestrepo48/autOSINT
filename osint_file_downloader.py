#!/usr/bin/env python3
"""
Módulo de descarga de archivos para OSINT
Descarga archivos importantes encontrados durante las búsquedas
"""

import os
import requests
import hashlib
import mimetypes
import asyncio
import aiofiles
from pathlib import Path
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse, urljoin, unquote
import magic
import zipfile
import tarfile
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class OSINTFileDownloader:
    """Descargador de archivos para investigaciones OSINT"""
    
    def __init__(self, downloads_dir: str = "downloads", max_file_size: int = 50 * 1024 * 1024):
        self.downloads_dir = Path(downloads_dir)
        self.max_file_size = max_file_size  # 50MB por defecto
        self.downloads_dir.mkdir(exist_ok=True)
        
        # Extensiones de archivos importantes para OSINT
        self.important_extensions = {
            'documents': ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.rtf', '.odt'],
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg'],
            'archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
            'code': ['.py', '.js', '.html', '.css', '.php', '.asp', '.aspx', '.jsp', '.rb', '.go', '.java'],
            'data': ['.csv', '.json', '.xml', '.sql', '.db', '.sqlite', '.xlsx', '.xls'],
            'configs': ['.conf', '.config', '.ini', '.cfg', '.yaml', '.yml', '.toml'],
            'certificates': ['.crt', '.cer', '.pem', '.key', '.p12', '.pfx'],
            'logs': ['.log', '.logs', '.access', '.error']
        }
        
        # MIME types importantes
        self.important_mime_types = [
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/zip',
            'application/x-rar-compressed',
            'application/json',
            'text/plain',
            'text/csv',
            'text/xml',
            'image/jpeg',
            'image/png',
            'image/gif'
        ]
        
        # Headers para peticiones HTTP
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    def is_important_file(self, url: str, content_type: Optional[str] = None) -> bool:
        """Determina si un archivo es importante para OSINT"""
        try:
            parsed = urlparse(url)
            path = unquote(parsed.path.lower())
            
            # Verificar extensión
            for category, extensions in self.important_extensions.items():
                if any(path.endswith(ext) for ext in extensions):
                    return True
            
            # Verificar MIME type
            if content_type and content_type.lower() in self.important_mime_types:
                return True
                
            # Verificar patrones específicos en la URL
            important_patterns = [
                'backup', 'dump', 'export', 'config', 'database', 'db',
                'admin', 'private', 'secret', 'confidential', 'internal',
                'password', 'passwd', 'credentials', 'key', 'token',
                'report', 'document', 'file', 'download', 'attachment'
            ]
            
            if any(pattern in path for pattern in important_patterns):
                return True
                
            return False
            
        except Exception as e:
            logger.error(f"Error evaluando importancia del archivo {url}: {e}")
            return False
    
    async def download_file(self, url: str, target_dir: Optional[str] = None, filename: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Descarga un archivo de forma asíncrona"""
        try:
            if target_dir:
                download_path = Path(target_dir)
            else:
                download_path = self.downloads_dir / datetime.now().strftime("%Y%m%d_%H%M%S")
            
            download_path.mkdir(parents=True, exist_ok=True)
            
            # Realizar petición HEAD para obtener información del archivo
            response = requests.head(url, headers=self.headers, timeout=10, allow_redirects=True)
            
            # Verificar tamaño del archivo
            content_length = response.headers.get('content-length')
            if content_length and int(content_length) > self.max_file_size:
                logger.warning(f"Archivo {url} demasiado grande ({content_length} bytes)")
                return None
            
            # Obtener nombre del archivo
            if not filename:
                filename = self._get_filename_from_url(url, dict(response.headers))
            
            file_path = download_path / filename
            
            # Descargar archivo
            response = requests.get(url, headers=self.headers, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = 0
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        total_size += len(chunk)
                        
                        # Verificar límite de tamaño durante descarga
                        if total_size > self.max_file_size:
                            logger.warning(f"Archivo {url} excede límite de tamaño")
                            f.close()
                            file_path.unlink()
                            return None
            
            # Generar hash del archivo
            file_hash = self._calculate_file_hash(file_path)
            
            # Detectar tipo de archivo
            file_type = self._detect_file_type(file_path)
            
            # Extraer metadatos si es posible
            metadata = self._extract_metadata(file_path)
            
            result = {
                'url': url,
                'filename': filename,
                'filepath': str(file_path),
                'size': total_size,
                'hash': file_hash,
                'type': file_type,
                'metadata': metadata,
                'downloaded_at': datetime.now().isoformat(),
                'content_type': response.headers.get('content-type', ''),
                'important': self.is_important_file(url, response.headers.get('content-type'))
            }
            
            logger.info(f"Archivo descargado: {filename} ({total_size} bytes)")
            return result
            
        except Exception as e:
            logger.error(f"Error descargando archivo {url}: {e}")
            return None
    
    def _get_filename_from_url(self, url: str, headers: Dict[str, str]) -> str:
        """Extrae el nombre del archivo de la URL o headers"""
        try:
            # Intentar obtener de Content-Disposition
            content_disposition = headers.get('content-disposition', '')
            if 'filename=' in content_disposition:
                filename = content_disposition.split('filename=')[1].strip('"\'')
                return filename
            
            # Obtener de la URL
            parsed = urlparse(url)
            filename = unquote(parsed.path.split('/')[-1])
            
            if filename and '.' in filename:
                return filename
            
            # Generar nombre por defecto
            return f"downloaded_file_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
        except Exception:
            return f"downloaded_file_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calcula el hash SHA-256 del archivo"""
        try:
            hash_sha256 = hashlib.sha256()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception as e:
            logger.error(f"Error calculando hash: {e}")
            return ""
    
    def _detect_file_type(self, file_path: Path) -> str:
        """Detecta el tipo de archivo usando python-magic"""
        try:
            if magic:
                return magic.from_file(str(file_path), mime=True)
            else:
                # Fallback usando mimetypes
                mime_type, _ = mimetypes.guess_type(str(file_path))
                return mime_type or "application/octet-stream"
        except Exception as e:
            logger.error(f"Error detectando tipo de archivo: {e}")
            return "application/octet-stream"
    
    def _extract_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Extrae metadatos del archivo"""
        metadata = {}
        
        try:
            # Metadatos básicos
            stat = file_path.stat()
            metadata['size'] = stat.st_size
            metadata['modified'] = datetime.fromtimestamp(stat.st_mtime).isoformat()
            metadata['created'] = datetime.fromtimestamp(stat.st_ctime).isoformat()
            
            # Metadatos específicos según tipo de archivo
            file_type = self._detect_file_type(file_path)
            
            if file_type == 'application/pdf':
                metadata.update(self._extract_pdf_metadata(file_path))
            elif 'image' in file_type:
                metadata.update(self._extract_image_metadata(file_path))
            elif file_type in ['application/zip', 'application/x-rar-compressed']:
                metadata.update(self._extract_archive_metadata(file_path))
                
        except Exception as e:
            logger.error(f"Error extrayendo metadatos: {e}")
            
        return metadata
    
    def _extract_pdf_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Extrae metadatos de archivos PDF"""
        metadata = {}
        try:
            import PyPDF2
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                info = pdf_reader.metadata
                
                if info:
                    metadata['title'] = info.get('/Title', '')
                    metadata['author'] = info.get('/Author', '')
                    metadata['subject'] = info.get('/Subject', '')
                    metadata['creator'] = info.get('/Creator', '')
                    metadata['producer'] = info.get('/Producer', '')
                    metadata['creation_date'] = str(info.get('/CreationDate', ''))
                    metadata['modification_date'] = str(info.get('/ModDate', ''))
                
                metadata['page_count'] = len(pdf_reader.pages)
                
        except Exception as e:
            logger.error(f"Error extrayendo metadatos PDF: {e}")
            
        return metadata
    
    def _extract_image_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Extrae metadatos de imágenes"""
        metadata = {}
        try:
            from PIL import Image
            from PIL.ExifTags import TAGS
            
            with Image.open(file_path) as img:
                metadata['width'] = img.width
                metadata['height'] = img.height
                metadata['format'] = img.format
                metadata['mode'] = img.mode
                
                # Extraer EXIF
                exif_data = img.getexif()
                if exif_data:
                    exif = {}
                    for tag_id, value in exif_data.items():
                        tag = TAGS.get(tag_id, tag_id)
                        exif[tag] = str(value)
                    metadata['exif'] = exif
                    
        except Exception as e:
            logger.error(f"Error extrayendo metadatos de imagen: {e}")
            
        return metadata
    
    def _extract_archive_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Extrae metadatos de archivos comprimidos"""
        metadata = {}
        try:
            if file_path.suffix.lower() == '.zip':
                with zipfile.ZipFile(file_path, 'r') as zip_file:
                    file_list = zip_file.namelist()
                    metadata['file_count'] = len(file_list)
                    metadata['files'] = file_list[:50]  # Limitar lista
                    
            elif file_path.suffix.lower() in ['.tar', '.gz', '.bz2']:
                with tarfile.open(file_path, 'r') as tar_file:
                    members = tar_file.getmembers()
                    metadata['file_count'] = len(members)
                    metadata['files'] = [m.name for m in members[:50]]
                    
        except Exception as e:
            logger.error(f"Error extrayendo metadatos de archivo: {e}")
            
        return metadata
    
    async def download_from_search_results(self, search_results: List[Dict[str, Any]], 
                                         target_name: str) -> List[Dict[str, Any]]:
        """Descarga archivos importantes encontrados en resultados de búsqueda"""
        downloaded_files = []
        
        # Crear directorio específico para este objetivo
        target_dir = self.downloads_dir / target_name / datetime.now().strftime("%Y%m%d_%H%M%S")
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Buscar URLs de archivos en los resultados
        file_urls = self._extract_file_urls(search_results)
        
        # Limitar número de descargas
        max_downloads = 50
        file_urls = file_urls[:max_downloads]
        
        logger.info(f"Descargando {len(file_urls)} archivos para {target_name}")
        
        # Descargar archivos de forma concurrente
        tasks = []
        for url in file_urls:
            if self.is_important_file(url):
                task = self.download_file(url, str(target_dir))
                tasks.append(task)
        
        # Ejecutar descargas
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, dict) and result is not None:
                downloaded_files.append(result)
        
        # Generar reporte de descargas
        self._generate_download_report(downloaded_files, target_dir)
        
        return downloaded_files
    
    def _extract_file_urls(self, search_results: List[Dict[str, Any]]) -> List[str]:
        """Extrae URLs de archivos de los resultados de búsqueda"""
        file_urls = []
        
        for result in search_results:
            # Extraer URLs de diferentes campos
            urls_to_check = []
            
            if isinstance(result, dict):
                # URLs directas
                if 'url' in result:
                    urls_to_check.append(result['url'])
                if 'link' in result:
                    urls_to_check.append(result['link'])
                if 'href' in result:
                    urls_to_check.append(result['href'])
                    
                # URLs en contenido
                if 'content' in result:
                    urls_to_check.extend(self._extract_urls_from_text(result['content']))
                if 'description' in result:
                    urls_to_check.extend(self._extract_urls_from_text(result['description']))
                
                # URLs en subdocumentos
                if 'files' in result and isinstance(result['files'], list):
                    urls_to_check.extend(result['files'])
                if 'attachments' in result and isinstance(result['attachments'], list):
                    urls_to_check.extend(result['attachments'])
            
            # Filtrar URLs válidas
            for url in urls_to_check:
                if self._is_valid_file_url(url):
                    file_urls.append(url)
        
        return list(set(file_urls))  # Eliminar duplicados
    
    def _extract_urls_from_text(self, text: str) -> List[str]:
        """Extrae URLs de texto usando regex"""
        import re
        
        url_pattern = r'https?://[^\s<>"]{1,}\.[a-zA-Z]{2,}(?:[^\s<>"]*)?'
        urls = re.findall(url_pattern, text)
        
        return [url for url in urls if self._is_valid_file_url(url)]
    
    def _is_valid_file_url(self, url: str) -> bool:
        """Verifica si una URL es válida para descarga"""
        try:
            if not url or not url.startswith(('http://', 'https://')):
                return False
            
            parsed = urlparse(url)
            path = parsed.path.lower()
            
            # Verificar que tenga extensión de archivo
            if not any(path.endswith(ext) for category in self.important_extensions.values() for ext in category):
                return False
            
            # Excluir URLs problemáticas
            excluded_domains = ['javascript:', 'mailto:', 'tel:', 'ftp://']
            if any(url.lower().startswith(excluded) for excluded in excluded_domains):
                return False
            
            return True
            
        except Exception:
            return False
    
    def _generate_download_report(self, downloaded_files: List[Dict[str, Any]], target_dir: Path):
        """Genera un reporte de los archivos descargados"""
        try:
            report_path = target_dir / "download_report.json"
            
            report = {
                'timestamp': datetime.now().isoformat(),
                'total_files': len(downloaded_files),
                'total_size': sum(f.get('size', 0) for f in downloaded_files),
                'files': downloaded_files,
                'summary': {
                    'by_type': {},
                    'by_category': {}
                }
            }
            
            # Generar estadísticas
            for file_info in downloaded_files:
                file_type = file_info.get('type', 'unknown')
                report['summary']['by_type'][file_type] = report['summary']['by_type'].get(file_type, 0) + 1
            
            # Guardar reporte
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Reporte de descargas generado: {report_path}")
            
        except Exception as e:
            logger.error(f"Error generando reporte de descargas: {e}")

# Instancia global del descargador
file_downloader = OSINTFileDownloader()
