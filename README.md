## System Integration: Loan Broker project

Group 7: Michael Daugbjerg, Nicolai Mikkelsen, Tim Hemmingsen, Ørvur Guttesen og Laura Hartig

#
### Documentation

#### Get credit score
This module contacts the credit bureau with the given ssn number and then takes the returned credit score number and sends it to the queue.
We take the ssn number and convert it to XML and send it to the module as soap XML. We then get the returned credit score number which can be used.

#### Rule base
The module gets the credit score number as soap XML and then find the banks that would like to make an offer to the user by the calculation of the credit score number. The module then returns this list of banks back to the other module which requested this data.
This soap service accepts an unsignedInt as argument and then returns a string. This string is JSON structured so the modules on the other end are able to convert it to JSON if they like.

#### Get banks
The “get banks” module waits on the queue “rule base” for new data. When data hits the queue the module consumes the data. We then takes the credit score out from the data and make it into a request to the soap XML service rule base with the credit score. After this the module takes the data returned by the rule base and converts it into JSON and adds it to the data from the queue. Finally it is published on a new queue called “distribution”.

#### Translator
Our translator gets the data and checks for which banks it have to be send to.
Our modules use JSON so we only have to convert our data for the XML bank. If we get the normal HTTP bank we just send it as a normal endpoint. If we get the XML bank then we convert our JSON to XML and send it with rabbitMQ. For the two other banks we use our JSON and send it with rabbitMQ.

#### First bank (HTTP)
Our HTTP bank got an endpoint where it takes all the data from the body. This bank uses JSON for data. It takes all the data from the body out and calculates the rate for the loan request and then returns the data back so we can use it. The data it returns is also JSON.

#### Second bank (RabbitMQ)
This bank uses RabbitMQ for data transferring and JSON as structure for data. This bank consumes its data from a queue called “loan_request”. It takes the data out from the JSON and calculates the interest rate for the given data. It then takes the data and converts it into JSON and puts it on a queue called “normalizer”.

#### Normalizer
This module consumes data from the queue called “normalizer”. With the given data it checks if the data is XML or JSON. It then takes the data and converts all the values to JSON and publishes the data on the queue called “aggregator”.

#### Aggregator
This module consumes from the queue called “aggregator”. It checks for which answer gave the lowest interest rate. It then takes only the lowest interest banks data and inserts it into our database. We then have a row in the database with the ssn number, loan amount, loan duration, loan interest and bank name.

#
### Bottlenecks
Bottlenecks can happen in all big systems with data transferring and handling. Our system is build with a lot of small modules which makes it easier to spot the bottlenecks and makes it easier to handle the bottlenecks. A Lot of our modules make calculations with the data or converts data which can take some time to do if enough requests are being made.
A place where a bottleneck could happen is in our normalizer module. This module gets data from all our banks which can make a lot of small jobs. Since we have queues from RabbitMQ does the requests not get deleted but the queue will keep getting bigger if the normalizer does not work faster than requests get in.
With RabbitMQ and the way the whole project is built, the solution to fix this problem is easy. Since our modules just takes the data from the queue with the given name and our modules are small and only does a small part of the job, we are able to just make another instance of our module. Instead of just using 1 instance of our normalizer will we make 2 (or more if needed). Both of the instances will keep consuming from the queue so the job will be done twice as fast. Since our modules got a really low coupling, we are able to make this fix without changing anything. The only coupling between the modules are the queues we made between them. The modules does not know how the data they get are made, they just consume what the queue gives them. That way we are able to make more instances without making any problems for the other modules and so we can keep an eye on our RabbitMQ queues and see which ones are behind and just make an instance more.

Bottlenecks we don’t have any way to fix will be all services outside what we made. If for example we get more requests than what the credit bureau is able to handle, the rest of our system will also be slow. We do not control the banks either (half of them if we see them as the school project). So even though our system easily can be scaled and easily can fix bottlenecks we  are not able to fix things outside our own systems.

#
### Design
Our project is made with RabbitMQ and we use it to make queues between all our modules so even though one modules lacks behind the others, the whole system will not wait. RabbitMQ handles all our messaging between our systems. This makes it easier to change one of our modules without thinking how the coupling is between the other modules. As long as our modules takes and gives the same form of data the rest of modules will not even notice the different. This means that our design gives us both low coupling and high cohesion since every part only does what it is supposed to and only a small part of the whole system. Inside every module RabbitMQ consumes the data from the queue and Python will then take the data and process it. When the Python code is done with processing or requesting data from outside our system we use RabbitMQ to publish the data to the next queue. This way our messaging and business logic are spread out from each other as much as possible.
