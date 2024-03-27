import numpy as np
import random
import time
import openapi_client as e2sim_client
from environment_manager import prepare_simulation


def grandstand_height(m):
    height = m * 10 / 42
    if m > 21:
        height += 2

    return height

def random_position():
    # UEs may fall into 4 areas: sides host left and host right, and goals, host team and visiting team at the first half.
    # (0) host left  x = -20...-10, y = 0...150
    # (1) host right x = 100...110, y = 0...150
    # (2) host goal  x = -20...110, y = 140...150
    # (3) visiting goal x = -20...110, y = 0...10
    # select the place
    position = random.randint(0, 93) # To uniformelly distribute the positions
    if position < 20: # Host left
        x = random.uniform(0, 42)
        y = random.uniform(42, 162)
        z = grandstand_height(x)
    elif position < 40:
        x = random.uniform(0, 42)
        y = random.uniform(42, 162)
        z = grandstand_height(x)
        x = 169 - x
    elif position < 67:
        x = random.uniform(0, 169)
        y = random.uniform(0, 42)
        z = grandstand_height(y)
    else:
        x = random.uniform(0, 169)
        y = random.uniform(0, 42)
        z = grandstand_height(y)
        y = 204 - y
    return (x, y, z)

def _get_endpoint_ip():
    import socket
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

def to_int(value):
    return int(np.floor(value))

def _anr(bbu, rsrp, snr, rsrq, cqi=0, bler=0):
    return e2sim_client.AnrPayload(nodeb=bbu, 
            rsrp=to_int(rsrp), 
            rsrq=to_int(rsrq), 
            sinr=to_int(snr), 
            cqi=to_int(cqi),
            bler=to_int(bler)
    )

def create_ue(ue_number, bbu_values):
    anr_values = [_anr(bbu, rsrp, snr, rsrq, cqi, bler) for bbu, rsrp, snr, rsrq, cqi, bler in bbu_values]
    flow =  random_flow()
    ip = _get_endpoint_ip()
    return e2sim_client.UeDescriptor(data_plane_flow = flow, anr_payload = anr_values, endpoint = f"http://{ip}:8081/{ue_number}")

if __name__ == '__main__':
    from multiprocessing.pool import ThreadPool
    import sys, yaml, getopt

    configfile = '/etc/config/configmap/application.yaml'

    opts, args = getopt.getopt(sys.argv[1:], 'c:')

    for opt, arg in opts:
        if opt == 'c':
            configfile = arg

    simulation, antennae, ues = prepare_simulation(configfile)
    n_ues = simulation.n_ues
    n_cells = simulation.n_cells

    # rsrp, snr, rsrq, bler, cqi
    rsrp, snr, rsrq, bler, cqi = simulation._simulate()
    rsrp = np.reshape(rsrp, (n_ues, n_cells))
    snr = np.reshape(snr, (n_ues, n_cells))
    rsrq = np.reshape(rsrq, (n_ues, n_cells))
    cqi = np.reshape(cqi, (n_ues, n_cells))
    bbu_descriptors = [e2sim_client.NodebDescriptor(nodeb_id=antenna['gnb_id']) for antenna in antennae]

    ue_descriptors = list()

    print("Starting connection test")

    ant_endpoints = [ antenna['endpoint'] for antenna in antennae ]

    def connect_task(ue):
        connected = False

        latencies = list()

        snr_ue = snr[ue]
        bbu_order = list(snr_ue.argsort())

        while not connected:
            time.sleep(random.random())
            bbu_values = [(bbu_descriptors[i], rsrp[ue, i], snr_ue[i], rsrq[ue, i], cqi[ue, i], bler[ue]) for i in range(len(bbu_descriptors))]
            ue_descr = create_ue(ue, bbu_values)
            ue_descriptors.append(ue_descr)

            if not bbu_order:
                bbu_order = list(snr_ue.argsort())

            connection_bbu = bbu_order.pop()
            connection_bbu_id = bbu_descriptors[connection_bbu].nodeb_id
            print(f"connecting ue 724011{ue:09} to antenna {connection_bbu_id}")
            configuration = e2sim_client.Configuration(host=ant_endpoints[connection_bbu])
            api_client = e2sim_client.ApiClient(configuration)
            management_api = e2sim_client.ManagementApi(api_client)

            start = time.monotonic_ns()
            try:
                admission_req = e2sim_client.UEIMSIAdmissionPutRequest(ue=ue_descr, nodeb=connection_bbu_id)
                management_api.u_eimsi_admission_put(f'724011{ue:09}', admission_req)
                latency = time.monotonic_ns() - start
                connected = True
            except Exception as e:
                latency = time.monotonic_ns() - start
                print(e)
            
            cbbu = bbu_values[connection_bbu]
            values = f'724011{ue:09},{cbbu[0].nodeb_id},{latency},{cbbu[2]},{connected}'
            print(values)
            latencies.append(values)
            print(f'{ue} connected')
                

        return latencies

    def flatten(l):
        flat = list()
        for row in l:
            flat += row

        return flat

    pool = ThreadPool(processes=100)
    latencies = flatten(pool.map(connect_task, ues))
    with open('/data/latencies.txt', 'w+') as fp:
        fp.writelines([f'{l}\n' for l in latencies])
