from spyne import Application, rpc, ServiceBase, Iterable, UnsignedInteger, \
    String
from spyne.protocol.json import JsonDocument
from spyne.protocol.http import HttpRpc
from spyne.server.wsgi import WsgiApplication
import logging
import json

class HelloWorldService(ServiceBase):
    @rpc(UnsignedInteger, _returns=String)
    def say_hello(ctx, creditscore):
    	print("Penis")
    	credit_score = creditscore
    	bank_list = []
    	if credit_score > 600:
    		bank_list.append("Danskebank")
    	if credit_score > 400:
    		bank_list.append("Amagerbanken")
    	if credit_score > 200:
    		bank_list.append("Nordea")
    	if credit_score > 200:
    		bank_list.append("Banknordic")
    	data = {"banks": bank_list}
    	return data

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)
    application = Application([HelloWorldService], 'spyne.examples.hello.http',
        in_protocol=HttpRpc(validator='soft'),
        out_protocol=JsonDocument(ignore_wrappers=True),
    )
    wsgi_application = WsgiApplication(application)

    server = make_server('127.0.0.1', 8000, wsgi_application)

    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at: http://localhost:8000/?wsdl")

server.serve_forever()
