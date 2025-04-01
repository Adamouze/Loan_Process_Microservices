from zeep import Client

wsdl_ulr="http://localhost:8002/?wsdl"

Soap_client = Client(wsdl=wsdl_ulr)

response = Soap_client.service.transfer_funds(20000)

print(response)







