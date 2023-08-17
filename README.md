# O-RAN Load balancing app
This repository contains the O-RAN Load balancing app. This application takes in intents at the SMO level and delivers policies to the RAN to self-organize the network.

## Organization
The repository is a `golang` workspace.

  - `lbctl` contains the application that sends the intents to the RAN.
  - `smoapp` contains the entrypoint application that receives intents and derives it for all other RAN nodes.
  - `client` containts the client code
  - `datamodel` contains the datamodel for the application: Intents, Parameters and so on.
  - `intentstore` contains the intent storage. The basic implementation uses a memory based storage, with a persistent store planned.