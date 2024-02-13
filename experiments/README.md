# Running the experiments

1. Clone the repository
2. Change the experiment configuration on `experiments/experiment.yaml`. For each gnb in the configmap, create a new gnb pod configuration.
3. Apply the configuration: `kubectl apply -n experiment -f experiments/experiment.yaml`.
4. Enter the `envman-sbrc-24` pod: `kubectl exec -it -n experiment envman-sbrc-24 -- bash`
5. Inside the pod, execute `python experiment.py [-c configfile]`. The default configuration file is provided as a config map at `/etc/config/configmap/application.yml`

# Applying intents

There are two intents that you can apply in the experiment: limiting connections per second and limiting the number of simultaneously connected UEs in a gnb.

1. Enter the `intentctl` pod: `kubectl exec -it -n experiment intentctl -- bash`
2. To limit the number of connections per second: `intentctl -s admission-control:50102 -t <number>` 
3. To limit the number of simultaneously connected UEs per gnb: `intentctl -s admission-control:50102 -u <number>`

# Configuring the experiment

The configuration is provided via a configmap in `experiments/experiment.yml`. It is composed of two objects: `ues` and `antennae`. These objects are contained in a 3D volume that defines the experiment.

## UEs
Currntly, we can only control the number of UEs in the experiment. The UEs are randomly located in the grandstand of a stadium.

```
ue:
  quantity: 10000 # number of ues in the experiment
```

## Antennae
Currently, each antenna has a single frequency associated with it, and a single 5G numerology. `antennae` is a list of antenna, each associated with a gnb.

```
antennae:
  - name: "gnb1"
    endpoint: "http://gnb1:8081/v1" # The endpoint for the envman of this gnb
    location: [47.0, 47.0 47.0] # The location of the antenna in the 3D volume, in [m]
    numerology: 4 # The 5G numerology associated with the antenna
    frequency: 7175 # The central frequency associated with the antenna, in [MHz]
    power: 10 # The power emitted by the antenna, in [W]
    gain: 8 # The antenna gain
    bandwidth: 100 # The total antenna bandwith, with sidebands, in [MHz]. It will be subdivided in channels by the numerology.
```

# Data
The data collected in this experiment is collected in the `admission-control` and `envman-sbrc-24` pods. To collect the data, execute `kubectl cp -n experiment envman-sbrc-24:/data/latencies.txt <location>` and `kubectl cp -n experiment admission-control-xapp:/data/experiment.db <location>`

This data needs to be combined with `python3 experiments/mergedata.py latencies.txt experiment.db`. To generate the data for plots, execute `python experiments/results/generate_data.py <path/to/experiment.db>`. And to generate the graphs, execute the `.plot` files in `experiments/results`.