"""Local gallery server that also works when launched without a console."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
log = (ROOT / 'tools' / 'gallery_server.log').open('a', encoding='utf-8', buffering=1)
sys.stdout = log
sys.stderr = log
server = ThreadingHTTPServer(('127.0.0.1', 8769), partial(SimpleHTTPRequestHandler, directory=str(ROOT)))
try:
    server.serve_forever()
finally:
    server.server_close()
    log.close()
