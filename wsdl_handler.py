import zeep

wsdl = 'http://datdb.cphbusiness.dk:8080/CreditScoreService/CreditScoreService?wsdl'
client = zeep.Client(wsdl=wsdl)
print(client.service.creditScore('123456-1234'))