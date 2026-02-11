
import sys
import logging
import traceback
from PyQt5.QtWidgets import QApplication

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

try:
    from src.login import LoginCls
    from src.database import setup_database_schema
except ImportError as e:
    logger.critical(f"Import Error: {e}")
    sys.exit(1)

def main():
    logger.info("Application starting...")
    try:
        app = QApplication(sys.argv)
        logger.info("QApplication created.")
        
        # Ensure DB tables exist
        logger.info("Setting up database schema...")
        if not setup_database_schema():
            logger.error("Database setup failed.")
            sys.exit(1)
        logger.info("Database setup complete.")
            
        logger.info("Initializing Login Window...")
        win = LoginCls()
        win.show()
        logger.info("Login Window shown.")
        
        sys.exit(app.exec_())
    except Exception as e:
        logger.critical(f"Unhandled exception: {e}")
        logger.critical(traceback.format_exc())
        sys.exit(1)

if __name__ == '__main__':
    main()
