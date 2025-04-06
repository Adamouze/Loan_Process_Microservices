from spyne import Application, rpc, ServiceBase, Unicode, Integer
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
from app.services.loan_provider_services import LoanProviderService
import os

LOAN_PROVIDER_PORT = int(os.getenv("LOAN_PROVIDER_PORT"))
if not LOAN_PROVIDER_PORT or LOAN_PROVIDER_PORT <= 0:
    raise ValueError("LOAN_PROVIDER_PORT environment variable is not set.")

application = Application(
    [LoanProviderService],
    tns='loan.soap.service',
    in_protocol=Soap11(),
    out_protocol=Soap11()
)

if __name__ == "__main__":
    server = make_server('0.0.0.0', LOAN_PROVIDER_PORT, WsgiApplication(application))
    server.serve_forever()


