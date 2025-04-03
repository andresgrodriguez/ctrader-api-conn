import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(log_level='INFO', log_dir='/app/data/logs'):
    """
    Configura el sistema de logging con handlers para consola y archivo.
    
    Args:
        log_level (str): Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir (str): Directorio donde se guardarán los archivos de log
    
    Returns:
        logging.Logger: Logger raíz configurado
    """
    # Crear directorio de logs si no existe
    os.makedirs(log_dir, exist_ok=True)
    
    # Configurar el logger raíz
    logger = logging.getLogger()
    logger.setLevel(log_level.upper())
    
    # Limpiar handlers existentes para evitar duplicados
    logger.handlers.clear()
    
    # Crear formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    )
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler para archivo con rotación
    log_file = os.path.join(log_dir, 'ctrader_client.log')
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger 