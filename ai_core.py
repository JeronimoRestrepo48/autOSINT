import json
import os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.chains import LLMChain

# Importar EnhancedOSINTSearcher de MCP (ajustar la ruta si es necesario)
# Esto podría causar un problema de importación circular si ai_core es importado por MCP.py directamente.
# Se manejará con cuidado en la integración. Por ahora, para la estructura del módulo:
# from MCP import EnhancedOSINTSearcher, OSINTConfig # Comentado para evitar error si MCP no existe aún en el entorno de prueba aislado

# Variable global para cachear la configuración y el LLM
_ia_config = None
_llm = None
# _osint_searcher_instance = None # Para el buscador OSINT

def load_ia_config():
    """Carga la configuración de IA desde ia_config.json."""
    global _ia_config
    if _ia_config is None:
        # Asumimos que ai_core.py está en el directorio raíz junto a MCP.py y config/
        config_path = os.path.join(os.path.dirname(__file__), 'config', 'ia_config.json')
        if not os.path.exists(config_path): # Ruta alternativa si ai_core.py está en un subdir
             config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'ia_config.json')

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                _ia_config = json.load(f)
        except FileNotFoundError:
            print(f"Error: El archivo de configuración de IA no se encontró en {config_path}")
            _ia_config = {}
            return None
        except json.JSONDecodeError:
            print(f"Error: El archivo de configuración de IA ({config_path}) no es un JSON válido.")
            _ia_config = {}
            return None
    return _ia_config

def get_llm():
    """Inicializa y devuelve el modelo LLM."""
    global _llm
    if _llm is None:
        config = load_ia_config()
        if not config or config.get("openai_api_key") == "TU_API_KEY_DE_OPENAI_AQUI" or not config.get("openai_api_key"):
            print("Advertencia: La API key de OpenAI no está configurada en config/ia_config.json. Las funciones de IA no operarán.")
            return None

        _llm = ChatOpenAI(
            api_key=config.get("openai_api_key"),
            model=config.get("default_model_name", "gpt-3.5-turbo"),
            temperature=config.get("temperature", 0.7)
        )
    return _llm

# def get_osint_searcher():
#     """Inicializa y devuelve una instancia de EnhancedOSINTSearcher."""
#     global _osint_searcher_instance
#     if _osint_searcher_instance is None:
#         # Cargar configuración OSINT de MCP.py (o una por defecto)
#         # Esto es una simplificación; MCP.py tiene su propia carga de config.
#         osint_main_config_path = os.path.join(os.path.dirname(__file__), 'osint_config.json')
#         if not os.path.exists(osint_main_config_path):
#             osint_main_config_path = os.path.join(os.path.dirname(__file__), '..', 'osint_config.json')

#         try:
#             with open(osint_main_config_path, 'r', encoding='utf-8') as f:
#                 mcp_config_data = json.load(f)
#
#             # Crear instancia de OSINTConfig (asumiendo que está disponible)
#             # Esta es una dependencia que necesita ser resuelta cuidadosamente
#             # from MCP import OSINTConfig # Mover import aquí para evitar error si no existe
#             # temp_osint_config = OSINTConfig()
#             # for key, value in mcp_config_data.items():
#             #    if hasattr(temp_osint_config, key):
#             #        setattr(temp_osint_config, key, value)
#             # _osint_searcher_instance = EnhancedOSINTSearcher(temp_osint_config)
#             print("Placeholder para inicialización de EnhancedOSINTSearcher. Se requiere MCP.OSINTConfig.")
#             # Por ahora, no podemos inicializarlo completamente sin refactorizar MCP.py o duplicar OSINTConfig.
#             # Esto se abordará en el paso de integración.
#         except Exception as e:
#             print(f"Error inicializando EnhancedOSINTSearcher: {e}. Funciones de orquestación pueden fallar.")
#             return None
#     return _osint_searcher_instance


def interpret_prompt_for_osint(user_prompt: str) -> dict:
    """
    Interpreta el prompt del usuario para extraer la intención, entidades y parámetros
    para una búsqueda OSINT.
    """
    llm = get_llm()
    if not llm:
        return {"error": "LLM no inicializado. Verifica la configuración de la API key."}

    template = ChatPromptTemplate.from_messages([
        ("system", """Eres un asistente experto en OSINT. Tu tarea es analizar el prompt del usuario y extraer la siguiente información en formato JSON:
        1.  `main_target`: La entidad principal de la investigación (ej. persona, empresa, dominio, IP, tema).
        2.  `target_type`: El tipo de la entidad principal (ej. 'person', 'company', 'domain', 'ip', 'topic', 'email', 'phone', 'username', 'vehicle', 'general_text').
        3.  `specific_details`: Un diccionario con detalles adicionales sobre el objetivo (ej. para 'person': {{"full_name": "...", "email": "...", "phone": "..."}}; para 'company': {{"nit": "..."}}).
        4.  `information_needed`: Una lista de los tipos de información que el usuario desea obtener (ej. ['antecedentes judiciales', 'perfiles en redes sociales', 'vulnerabilidades técnicas', 'noticias recientes', 'datos de contacto']).
        5.  `sources_hint`: Una lista de posibles tipos de fuentes a consultar si el prompt lo sugiere (ej. ['gobierno', 'medios', 'foros', 'dark_web', 'registros_publicos', 'apis_especializadas', 'social_media']).
        6.  `enable_dorking`: Booleano, true si el usuario sugiere o podría beneficiarse de Google Dorking, de lo contrario false.
        7.  `search_parameters`: Un diccionario con parámetros adicionales para la búsqueda, como 'max_results', 'date_range', 'language', 'risk_filter'.
        8.  `output_format_preference`: String, preferencia de formato de reporte si se menciona (ej. 'resumen', 'lista_detallada', 'reporte_formal', 'json_results').
        9.  `original_prompt`: El prompt original del usuario.

        Ejemplo de prompt: "Investiga a Juan Pérez, correo juan.perez@email.com, y encuentra sus perfiles en redes sociales y cualquier antecedente judicial. Usa dorks si es necesario y dame un resumen."
        Salida JSON esperada:
        {{
            "main_target": "Juan Pérez",
            "target_type": "person",
            "specific_details": {{"full_name": "Juan Pérez", "email": "juan.perez@email.com"}},
            "information_needed": ["perfiles en redes sociales", "antecedentes judiciales"],
            "sources_hint": ["social_media", "gobierno"],
            "enable_dorking": true,
            "search_parameters": {{}},
            "output_format_preference": "resumen",
            "original_prompt": "Investiga a Juan Pérez, correo juan.perez@email.com, y encuentra sus perfiles en redes sociales y cualquier antecedente judicial. Usa dorks si es necesario y dame un resumen."
        }}

        Si un campo no es identificable, usa un valor por defecto apropiado como "no_especificado" para strings, lista vacía para listas, o false para booleanos.
        El campo `main_target` debe ser la entidad más específica posible.
        Para `target_type`, usa uno de: 'person', 'company', 'domain', 'ip', 'topic', 'email', 'phone', 'username', 'vehicle', 'general_text'.
        Para `specific_details`:
          - 'person': {'full_name', 'personId', 'email', 'phone', 'city', 'profession', 'university', 'company'}
          - 'company': {'businessName', 'businessNIT', 'businessCity'}
          - 'vehicle': {'vehiclePlate', 'vehicleType', 'vehicleCity', 'vehicleBrand', 'vehicleModel'}
          - 'contact': {'contactEmail', 'contactPhone', 'contactUsername', 'contactDomain', 'contactIP'}
          - 'news': {'newsQuery', 'newsRegion', 'newsTimeRange'}
          - 'government': {'govQuery', 'govRecordType'}
        Si el target_type es 'domain', 'ip', 'email', 'phone', 'username', 'topic', 'general_text', `specific_details` puede estar vacío o contener el propio target como valor.
        Asegúrate de que la salida sea un JSON válido.
        """),
        ("human", "{user_prompt}")
    ])

    chain = LLMChain(llm=llm, prompt=template, output_parser=StrOutputParser())

    response_str = ""
    try:
        response_str = chain.invoke({"user_prompt": user_prompt})
        if response_str.startswith("```json"):
            response_str = response_str[7:]
        if response_str.endswith("```"):
            response_str = response_str[:-3]

        parsed_json = json.loads(response_str.strip())

        parsed_json.setdefault("main_target", "no_especificado")
        parsed_json.setdefault("target_type", "general_text")
        parsed_json.setdefault("specific_details", {})
        parsed_json.setdefault("information_needed", [])
        parsed_json.setdefault("sources_hint", [])
        parsed_json.setdefault("enable_dorking", False)
        parsed_json.setdefault("search_parameters", {})
        parsed_json.setdefault("output_format_preference", "no_especificado")
        parsed_json["original_prompt"] = user_prompt
        return parsed_json
    except json.JSONDecodeError as e:
        print(f"Error al decodificar JSON de la respuesta del LLM: {e}")
        print(f"Respuesta recibida: {response_str}")
        return {"error": "Error al decodificar la respuesta del LLM.", "raw_response": response_str}
    except Exception as e:
        print(f"Error inesperado al interpretar el prompt: {e}")
        return {"error": f"Error inesperado: {str(e)}"}

def orchestrate_osint_search(interpretation: dict, osint_searcher) -> list:
    """
    Orquesta las búsquedas OSINT basadas en la interpretación del prompt.
    Llama a los métodos de la instancia `osint_searcher` (de EnhancedOSINTSearcher).
    """
    if not osint_searcher:
        return [{"error": "Instancia de OSINTSearcher no proporcionada o no inicializada."}]

    target = interpretation.get("main_target", "")
    target_type = interpretation.get("target_type", "general")
    details = interpretation.get("specific_details", {})
    enable_dorking = interpretation.get("enable_dorking", False)
    # user_id se tomará del contexto de la sesión en Flask, aquí un default.
    user_id_for_search = details.get("user_id", 1)

    results = []
    search_executed = False

    # Mapeo preliminar de target_type a search_type de EnhancedOSINTSearcher
    # Esto necesitará ser más robusto y considerar 'information_needed' y 'sources_hint'

    # Construir el query para EnhancedOSINTSearcher.search()
    # EnhancedOSINTSearcher.search espera un `query` string y un `search_type`
    # El `search_type` en EnhancedOSINTSearcher es más como una categoría general.
    # La lógica de MCP.py /api/search ya hace algo de esto.

    query_for_searcher = target
    search_type_for_searcher = target_type # Mapeo inicial

    if target_type == "person":
        query_parts = [details.get("full_name", target)]
        if details.get("personId"): query_parts.append(f"ID:{details.get('personId')}")
        if details.get("email"): query_parts.append(details.get('email'))
        if details.get("phone"): query_parts.append(details.get('phone'))
        if details.get("city"): query_parts.append(details.get('city'))
        query_for_searcher = " ".join(filter(None, query_parts))
        search_type_for_searcher = "person" # Coincide con el tipo en MCP.py
    elif target_type == "company":
        query_parts = [details.get("businessName", target)]
        if details.get("businessNIT"): query_parts.append(f"NIT:{details.get('businessNIT')}")
        if details.get("businessCity"): query_parts.append(details.get('businessCity'))
        query_for_searcher = " ".join(filter(None, query_parts))
        search_type_for_searcher = "business"
    elif target_type == "domain":
        query_for_searcher = target
        search_type_for_searcher = "domain"
    elif target_type == "ip":
        query_for_searcher = target
        search_type_for_searcher = "ip"
    elif target_type == "email":
        query_for_searcher = target
        search_type_for_searcher = "email" # o 'contact' si MCP.py lo maneja así
    elif target_type == "phone":
        query_for_searcher = target
        search_type_for_searcher = "contact" # MCP.py usa 'contact' para teléfonos
    elif target_type == "username":
        query_for_searcher = target
        search_type_for_searcher = "social" # O un tipo 'username' si existe
    elif target_type == "vehicle":
        query_parts = [details.get("vehiclePlate", target)]
        # ... agregar más detalles de vehículo si EnhancedOSINTSearcher los soporta así
        query_for_searcher = " ".join(filter(None, query_parts))
        search_type_for_searcher = "vehicle"
    elif target_type == "topic" or target_type == "general_text":
        query_for_searcher = target
        search_type_for_searcher = "general" # Búsqueda general para temas

    if not query_for_searcher or query_for_searcher == "no_especificado":
        return [{"error": "No se pudo determinar un objetivo de búsqueda claro a partir del prompt."}]

    print(f"AI Orchestrator: Query='{query_for_searcher}', SearchType='{search_type_for_searcher}', Dorking='{enable_dorking}'")

    try:
        # Llamada al método search de EnhancedOSINTSearcher
        # Asumimos que osint_searcher es una instancia de EnhancedOSINTSearcher
        search_result_data = osint_searcher.search(
            query=query_for_searcher,
            search_type=search_type_for_searcher,
            enable_dorking=enable_dorking,
            user_id=user_id_for_search # MCP.py lo espera
        )
        search_executed = True
        # search_result_data es un diccionario con 'results' como una lista
        if isinstance(search_result_data, dict) and "results" in search_result_data:
            raw_results = search_result_data["results"]
            # Asegurarnos que los resultados sean una lista de diccionarios como espera generate_osint_report_summary
            if isinstance(raw_results, list):
                results.extend(raw_results)
            else: # Si no es una lista, podría ser un error o un formato inesperado
                results.append({"title": "Resultado de búsqueda (formato no estándar)", "content": str(raw_results), "source": search_type_for_searcher})

        else: # Si search_result_data no es un dict o no tiene 'results'
             results.append({"title": "Resultado de búsqueda (estructura inesperada)", "content": str(search_result_data), "source": search_type_for_searcher})


    except Exception as e:
        print(f"Error durante la orquestación de búsqueda ({search_type_for_searcher} para '{query_for_searcher}'): {e}")
        results.append({"error": f"Error ejecutando búsqueda para {target_type}: {str(e)}"})

    if not search_executed and not results: # Si no se ejecutó ninguna búsqueda específica
        results.append({"info": "No se identificó una acción de búsqueda específica para este prompt o hubo un error."})

    return results


def generate_osint_report_summary(search_results: list, user_prompt: str, interpretation: dict) -> str:
    """
    Genera un resumen narrativo de los resultados OSINT utilizando un LLM.
    """
    llm = get_llm()
    if not llm:
        return "Error: LLM no inicializado. Verifica la configuración de la API key."

    simplified_results_list = []
    for result in search_results[:20]: # Limitar a 20 para el contexto del LLM
        if isinstance(result, dict):
            title = result.get('title', 'N/A')
            source = result.get('source', 'N/A')
            description = result.get('description', '')
            risk = result.get('risk_level', 'N/A')
            url = result.get('url', '')

            entry = f"- Título: {title} (Fuente: {source}, Riesgo: {risk})"
            if description:
                 entry += f", Descripción: {description[:100]}{'...' if len(description)>100 else ''}"
            if url:
                entry += f", URL: {url}"
            simplified_results_list.append(entry)
        elif isinstance(result, str): # Manejar si algún resultado es solo un string
            simplified_results_list.append(f"- {result}")


    results_str = "\n".join(simplified_results_list) if simplified_results_list else "No se encontraron resultados procesables para el resumen."
    if not search_results:
         results_str = "No se encontraron resultados en la búsqueda."


    template_str = f"""Eres un analista OSINT experto. Has realizado una investigación basada en el siguiente prompt del usuario:
'{user_prompt}'

La interpretación del prompt fue:
- Objetivo Principal: {interpretation.get('main_target')}
- Tipo de Objetivo: {interpretation.get('target_type')}
- Detalles Específicos: {json.dumps(interpretation.get('specific_details'))}
- Información Requerida: {', '.join(interpretation.get('information_needed', []))}

Y has obtenido los siguientes hallazgos (limitado a los primeros relevantes):
{results_str}

Por favor, redacta un resumen ejecutivo conciso y coherente de los hallazgos.
El resumen debe:
1.  Comenzar mencionando brevemente el objetivo de la investigación.
2.  Destacar los puntos más relevantes encontrados en relación a lo que el usuario solicitó.
3.  Si hay información sensible o de alto riesgo, mencionarla con cautela.
4.  Si no se encontró información relevante para alguna de las solicitudes, indicarlo.
5.  Concluir con una breve valoración general de los hallazgos.
6.  Mantén un tono profesional y objetivo. No inventes información que no esté en los resultados.
7.  El resumen no debe exceder los 350-450 tokens.
"""

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", template_str),
        ("human", "Genera el resumen ejecutivo de la investigación.")
    ])

    chain = LLMChain(llm=llm, prompt=prompt_template, output_parser=StrOutputParser())

    try:
        summary = chain.invoke({}) # El input está en el system prompt
        return summary
    except Exception as e:
        print(f"Error al generar el resumen del reporte: {e}")
        return f"Error al generar el resumen: {str(e)}"

if __name__ == '__main__':
    print("Probando ai_core.py...")
    config = load_ia_config()

    if not config or config.get("openai_api_key") == "TU_API_KEY_DE_OPENAI_AQUI" or not config.get("openai_api_key"):
        print("Configuración de API Key de OpenAI no encontrada o es el valor por defecto.")
        print("Por favor, configura tu API Key en config/ia_config.json para pruebas completas.")
    else:
        print("API Key de OpenAI encontrada. Procediendo con pruebas de LLM.")

        # Prueba de interpretación
        test_prompt_person = "Investiga a Carlos Rodriguez con cédula 123456789 en Cali. Necesito sus perfiles de redes sociales y si tiene procesos judiciales. Usa dorks."
        print(f"\n--- Probando interpretación para: \"{test_prompt_person}\" ---")
        interpretation_person = interpret_prompt_for_osint(test_prompt_person)
        print(json.dumps(interpretation_person, indent=2, ensure_ascii=False))

        test_prompt_domain = "Analiza la seguridad del dominio example.com, busca subdominios y tecnologías usadas."
        print(f"\n--- Probando interpretación para: \"{test_prompt_domain}\" ---")
        interpretation_domain = interpret_prompt_for_osint(test_prompt_domain)
        print(json.dumps(interpretation_domain, indent=2, ensure_ascii=False))

        test_prompt_topic = "Quiero un reporte sobre las últimas vulnerabilidades de phishing en el sector bancario colombiano."
        print(f"\n--- Probando interpretación para: \"{test_prompt_topic}\" ---")
        interpretation_topic = interpret_prompt_for_osint(test_prompt_topic)
        print(json.dumps(interpretation_topic, indent=2, ensure_ascii=False))

        # Prueba de generación de resumen (con resultados simulados)
        if interpretation_person and "error" not in interpretation_person:
            print("\n--- Probando generación de resumen para prompt de persona ---")
            simulated_results_person = [
                {"title": "Perfil de Carlos Rodriguez en Facebook", "source": "facebook", "description": "Usuario activo, fotos recientes de viajes.", "risk_level": "low", "url": "http://facebook.com/carlos.r"},
                {"title": "Mención de Carlos Rodriguez en proceso judicial No. 2023-001", "source": "rama_judicial_sim", "description": "Demandante en caso civil por incumplimiento.", "risk_level": "medium", "url": "http://simulacion.gov.co/proceso1"},
                {"title": "No se encontraron más perfiles públicos relevantes.", "source": "busqueda_general", "description": "", "risk_level": "low", "url": ""}
            ]
            summary_person = generate_osint_report_summary(simulated_results_person, test_prompt_person, interpretation_person)
            print("Resumen Generado:\n", summary_person)

        # Prueba de orquestación (simulada, ya que EnhancedOSINTSearcher no está instanciado aquí)
        print("\n--- Probando orquestación (simulación de llamada) ---")
        if interpretation_domain and "error" not in interpretation_domain:
            # Simular una instancia de osint_searcher para la prueba
            class MockOSINTSearcher:
                def search(self, query, search_type, enable_dorking, user_id):
                    print(f"[MockSearcher] Recibida búsqueda: query='{query}', type='{search_type}', dorking='{enable_dorking}'")
                    return {"results": [
                        {"title": f"Resultado simulado para {query} ({search_type})", "source": search_type, "description": "Contenido simulado.", "risk_level": "low"}
                    ]}

            mock_searcher = MockOSINTSearcher()
            orchestration_results_domain = orchestrate_osint_search(interpretation_domain, mock_searcher)
            print("Resultados de orquestación (simulada) para dominio:")
            print(json.dumps(orchestration_results_domain, indent=2, ensure_ascii=False))

            # Generar resumen de estos resultados orquestados
            if orchestration_results_domain and not any("error" in r for r in orchestration_results_domain):
                 summary_orchestrated = generate_osint_report_summary(orchestration_results_domain, test_prompt_domain, interpretation_domain)
                 print("\nResumen de resultados orquestados (dominio):\n", summary_orchestrated)

    print("\nPruebas de ai_core.py finalizadas.")
