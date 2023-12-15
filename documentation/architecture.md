# Intents
Intents are high level desires for the RAN performance. Having a throughput of a least a certain value for each UE is an intent. Intents are expressed in  terms of resource utilization, like bandwidth, latency and energy.

Intents are  received in the Load Balancing Intent Receiver, and this component records it in a persistent database, as well as publishing it in the appropriate topic in Kafka. Kafka distributes this intent to the subscribed Load Balancing Intent Brokers, which breaks down the intent into low level policies that are implemeented in the Near-RT RIC and in //Intelligent Network Functions//.

The network functions need to implement certain statistic counters to monitor the functions.

# Intelligent Network Functions
Intelligent Network Functions are network functions that can also perform policies.

In our example, we deploy an Intelligent Radio Resource Control which is capable of limit the number of UEs associated to the  cells it controls and limit the  number of incoming association requests. Other functions may be implemented, like some parts of the MLB protocol.

When an NF is intelligent, the Near-RT RIC send the policy to the NF and monitors the statistics to see when volations are present. On NFs that lack intelligence, the Near-RT RIC will subscribe to the adequate events, and interfere when a violation is about to happen.

# Sending sending commands
`lb_smoapp` receives commands over a REST interface with the following endpoints.
    - 'PUT /intent': creates a new intent. Request body is a JSON document describing the intent with a requestID, response body is the RequestID plus the IntentID.
    - 'GET /intents':  List  all current intents.
    - 'GET /intent/idx': Retrieves details for the intent identified by idx.
    - 'DELETE /intent/idx': Deletes the intent identified by idx.