import logging


def init_logger(logfile: str, file_loglvl=logging.DEBUG, console_loglvl=logging.INFO):
    """Initialize the root logger and standard log handlers."""
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # Add a filehandler that saves every log message to the logfile
    file_handler = logging.FileHandler(logfile, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    file_handler.setLevel(file_loglvl)
    root_logger.addHandler(file_handler)

    # Add a consolehandler to send output to the console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    console_handler.setLevel(console_loglvl)
    root_logger.addHandler(console_handler)
