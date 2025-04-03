import os
from types import SimpleNamespace
from dotenv import load_dotenv

def load_config(args=None):
    """
    Carga la configuración desde variables de entorno y argumentos CLI.
    
    Args:
        args (argparse.Namespace, optional): Argumentos de línea de comandos para sobrescribir valores.
    
    Returns:
        SimpleNamespace: Objeto con la configuración cargada.
    
    Raises:
        ValueError: Si faltan variables de entorno obligatorias o tienen tipos inválidos.
    """
    # Cargar variables de entorno desde .env
    load_dotenv()
    
    # Variables obligatorias
    client_id = os.getenv('CTRADER_CLIENT_ID')
    client_secret = os.getenv('CTRADER_CLIENT_SECRET')
    account_id = os.getenv('CTRADER_ACCOUNT_ID')
    
    # Validar variables obligatorias
    if not all([client_id, client_secret, account_id]):
        raise ValueError("Faltan variables de entorno obligatorias: CTRADER_CLIENT_ID, CTRADER_CLIENT_SECRET, CTRADER_ACCOUNT_ID")
    
    # Convertir account_id a entero
    try:
        account_id = int(account_id)
    except ValueError:
        raise ValueError("CTRADER_ACCOUNT_ID debe ser un número entero")
    
    # Variables opcionales con valores por defecto
    host = os.getenv('CTRADER_API_HOST', 'demo')
    port = os.getenv('CTRADER_API_PORT', '5035')
    access_token = os.getenv('ACCESS_TOKEN', '')
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    output_dir = os.getenv('OUTPUT_DIR', '/app/data/output')
    
    # Validar y convertir host
    if host not in ['demo', 'live']:
        raise ValueError("CTRADER_API_HOST debe ser 'demo' o 'live'")
    api_host = f"{host}.ctraderapi.com"
    
    # Convertir port a entero
    try:
        port = int(port)
    except ValueError:
        raise ValueError("CTRADER_API_PORT debe ser un número entero")
    
    # Sobrescribir con argumentos CLI si se proporcionan
    if args:
        if hasattr(args, 'host') and args.host:
            api_host = f"{args.host}.ctraderapi.com"
        if hasattr(args, 'port') and args.port:
            port = args.port
        if hasattr(args, 'log_level') and args.log_level:
            log_level = args.log_level
        if hasattr(args, 'output_dir') and args.output_dir:
            output_dir = args.output_dir
    
    # Crear y retornar objeto de configuración
    return SimpleNamespace(
        client_id=client_id,
        client_secret=client_secret,
        account_id=account_id,
        api_host=api_host,
        port=port,
        access_token=access_token,
        log_level=log_level,
        output_dir=output_dir
    ) 