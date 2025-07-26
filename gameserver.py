import sys
import signal
import time
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

# Check for good enough Python version. Use builtin path.
# XXX: Should be killed before release.
if '__pypy__' in sys.builtin_module_names:
    sys.path.insert(2, "/usr/local/lib/python3.4/dist-packages")

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
    except ImportError:
        print("Cython failed")
        pass # No cython / old cython

# Fix log machinery by replacing tornado.concurrent.
# XXX: This might be tornado 4 specific. Be aware of bugs.
import game.hack_concurrent
#del sys.modules['tornado.concurrent']
sys.modules['tornado.concurrent'] = game.hack_concurrent

#### Import the tornado ####
from tornado.tcpserver import *
import tornado.gen
from service.gameserver import GameFactory
import time
import game.loading
import tornado.log
tornado.log.enable_pretty_logging()

def safe_bind(server, port, interface, name):
    """Bind a TCPServer and exit with a clear message if the port is in use."""
    try:
        server.bind(port, interface)
    except OSError as e:
        if e.errno in (errno.EADDRINUSE, 10048):  # 10048 is Windows-specific
            logging.error("%s port %s already in use on interface '%s'.", name, port, interface or '0.0.0.0')
            sys.exit(1)
        raise

startTime = time.time()
# Game Server
gameServer = GameFactory()
safe_bind(gameServer, config.gamePort, config.gameInterface, "Game server")
gameServer.start()

# (optionally) buildt in login server.
if config.letGameServerRunTheLoginServer:
    from service.loginserver import LoginFactory
    loginServer= LoginFactory()
    safe_bind(loginServer, config.loginPort, config.loginInterface, "Login server")
    loginServer.start()
    
# (optional) built in extension server.
# XXX Port later or kill?
#if config.enableExtensionProtocol:
#    from service.extserver import ExtFactory
#    extFactory = ExtFactory()
#    tcpService = internet.TCPServer(config.loginPort + 10000, extFactory, interface=config.loginInterface)
#    tcpService.setServiceParent(topService)

# (optional) built in extension server.
# XXX: Port later...
if config.enableWebProtocol:
    from service.webserver import Web
    from tornado import httpserver
    webServer = tornado.httpserver.HTTPServer(Web)
    safe_bind(webServer, config.webPort, config.webInterface, "Web server")
    webServer.start()


# Load the core stuff!
IOLoop.instance().add_callback(game.loading.loader, startTime)

# Start reactor. This will call the above.
signal.signal(signal.SIGINT, game.scriptsystem.shutdown)
signal.signal(signal.SIGTERM, game.scriptsystem.shutdown)
IOLoop.instance().start()

