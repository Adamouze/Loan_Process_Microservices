from spyne import Application, rpc, ServiceBase, Unicode, Integer
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server

class LoanProviderService(ServiceBase):
    @rpc(Integer, _returns=Unicode)
    def transfer_funds(ctx, amount):
        return f"Transfer of {amount} approved."

application = Application(
    [LoanProviderService],
    tns='loan.soap.service',
    in_protocol=Soap11(),
    out_protocol=Soap11()
)

if __name__ == "__main__":
    server = make_server('0.0.0.0', 8002, WsgiApplication(application))
    server.serve_forever()


