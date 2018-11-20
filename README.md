## System Integration: Loan Broker project

###### Group 7: Michael, Nicolai, Tim, Ørvur og Laura



#
#### Documentation

##### Get credit score
This module contacts the credit bureau with the given ssn number and then takes the returned credit score number and sends it to the queue.
We take the ssn number and convert it to XML and send it to the module as soap XML. We then get the returned credit score number which can be used.

##### Rule base
The module gets the credit score number as soap XML and then find the banks that would like to make an offer to the user by the calculation of the credit score number. The module then returns this list of banks back to the other module which requested this data.
This soap service accepts an unsignedInt as argument and then returns a string. This string is JSON structured so the modules on the other end are able to convert it to JSON if they like.

##### Get banks
The “get banks” module waits on the queue “rule base” for new data. When data hits the queue the module consumes the data. We then takes the credit score out from the data and make it into a request to the soap XML service rule base with the credit score. After this the module takes the data returned by the rule base and converts it into JSON and adds it to the data from the queue. Finally it is published on a new queue called “distribution”.

##### Translator
Our translator gets the data and checks for which banks it have to be send to.
Our modules use JSON so we only have to convert our data for the XML bank. If we get the normal HTTP bank we just send it as a normal endpoint. If we get the XML bank then we convert our JSON to XML and send it with rabbitMQ. For the two other banks we use our JSON and send it with rabbitMQ.
