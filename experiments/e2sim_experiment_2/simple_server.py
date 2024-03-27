from experiment import prepare_simulation
import controllers

s, a ,u = prepare_simulation('/etc/config/configmap/application.yaml')
controllers.start_server(8080)