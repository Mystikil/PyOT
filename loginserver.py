import sys
import logging
import errno

# Setup logging immediately so import-time errors are captured
error_handler = logging.FileHandler('errorlog.md')
error_handler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
error_handler.setFormatter(formatter)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    handlers=[logging.StreamHandler(), error_handler])


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.getLogger().error("Uncaught exception",
                              exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception

sys.path.insert(0, '.')
sys.path.insert(1, 'game')

try:
    import config
except ImportError:
    print("You got no config.py file. Please make a file from config.py.dist")
    sys.exit()

#### Try Cython? ####
if config.tryCython:
    try:
        import pyximport
        pyximport.install(pyimport = True)
    except:
        pass # No cython / old cython

# Fix log machinery by replacing tornado.concurrent.
# XXX: This might be tornado 4 specific. Be aware of bugs.
import game.hack_concurrent
#del sys.modules['tornado.concurrent']
sys.modules['tornado.concurrent'] = game.hack_concurrent

#### Import the tornado ####
from tornado.tcpserver import *
from tornado.ioloop import IOLoop

def safe_bind(server, port, interface, name):
    """Bind a TCPServer and exit with a clear message if the port is in use."""
    try:
        server.bind(port, interface)
    except OSError as e:
        if e.errno in (errno.EADDRINUSE, 10048):
            logging.error("%s port %s already in use on interface '%s'.", name, port, interface or '0.0.0.0')
            sys.exit(1)
        raise
    
from service.loginserver import LoginFactory
loginServer= LoginFactory()
safe_bind(loginServer, config.loginPort, config.loginInterface, "Login server")
loginServer.start()

# Start reactor. This will call the above.
IOLoop.instance().start()
            
