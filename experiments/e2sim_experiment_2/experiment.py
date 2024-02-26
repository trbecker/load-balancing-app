import numpy as np
import random
import time
import openapi_client as e2sim_client
import yaml

speed_of_light = 299792485
MHz = 1000000
kHz = 1000
minute = 60
k_b = 1.380649e-23 # Boltzmann contant

class experiment:
    def __init__(self, n_ues, n_cells):
        self.n_ues = n_ues
        self.n_cells = n_cells
        self.ue_positions = np.zeros((n_ues, 1, 3))
        self.ue_gains = np.zeros((n_ues, 1, 1))
        self.cell_positions = np.zeros((1, n_cells, 3))
        self.cell_gains = np.zeros((1, n_cells, 1))
        self.cell_wave_lengths = np.zeros((1, n_cells, 4))
        self.cell_power = np.zeros((1, n_cells, 1))
        self.subcarrier_spacing = np.zeros((1, n_cells, 1))
        self.current_ue = 0
        self.current_cell = 0

        self.gamma = 1

    def add_ue(self, ue_location, ue_gain):
        pos = self.current_ue
        self.current_ue += 1

        self.ue_positions[pos, 0] = ue_location
        self.ue_gains[pos] = ue_gain

        return pos

    def move_ues(self):
        self.ue_positions += np.random.uniform(0, 1, self.ue_positions.shape)


    def add_cell(self, ant):
        pos = self.current_cell
        self.current_cell += 1

        ant['frequency'] = ant['frequency'] * MHz
        ant['bandwidth'] = ant['bandwidth'] * MHz
        ant['subcarrier_spacing'] = 15 * 2 ** ant['numerology'] * kHz

        self.subcarrier_spacing[0, pos] = ant['subcarrier_spacing']
        self.cell_positions[0, pos] = ant['location']
        self.cell_gains[0, pos] = ant['gain']
        n_subcarriers = int(np.floor(ant['bandwidth'] / ant['subcarrier_spacing']))
        first_subcarrier = ant['frequency'] - ant['bandwidth'] / 2 + ant['subcarrier_spacing'] / 2
        subcarriers = [first_subcarrier + sc * ant['subcarrier_spacing'] for sc in range(n_subcarriers)]
        self.cell_wave_lengths[0, pos] = speed_of_light / np.random.choice(subcarriers, replace=False, size=(4,))
        self.cell_power[0, pos] = ant['power']

        return ant

    def _simulate(self):
        distances = np.reshape(np.linalg.norm(self.ue_positions - self.cell_positions, axis = 2), (self.n_ues, self.n_cells, 1))

        power_rx = (self.cell_power * self.cell_gains * self.ue_gains) * (self.cell_wave_lengths / (4 * np.pi * distances)) ** 2
        noise = k_b * np.random.normal(300, 1, self.ue_gains.shape) * self.subcarrier_spacing
        power_rx_sum = np.sum(power_rx, axis=2)
        power_rx_sum = np.reshape(power_rx_sum, (power_rx_sum.shape[0], power_rx_sum.shape[1], 1))
        power_rx_avg = power_rx_sum / power_rx.shape[2]
        # SINR-Range in TS 38331 is INTEGER(0..127)
        snr = 10 * np.log10(power_rx_avg / noise)
        bw = 12 * 240000 * np.log2(1 + power_rx_avg / noise) / 1024 / 1024
        path_losses_lin = self.cell_power / power_rx_avg
        path_losses_db = 10 * self.gamma * np.log10(path_losses_lin)
        shadowing = np.random.normal(0, 7.9, path_losses_db.shape)
        path_losses_db += shadowing
        # From http://4g5gworld.com/blog/5gnr-reference-signals-measurement
        # rsrp-range in TS 38331 is INTEGER(0..127)
        rsrp = 10 * np.log10(self.cell_power) - path_losses_db
        print(np.mean(rsrp), np.mean(snr), np.mean(bw))
        # RSSI is calculated from the formula RSRP = RSSI - 10 * log_{10} (12 * N) [RSSI = RSRP + log_{10} (12 * N)], with N the number of resource blocks.
        # N is dependent on UE_BW (N = BW / (12 * subcarrier_spacing)). We will assume N = 1 for this test case.
        # RSSI-Range in TS 38331 is INTEGER(0..76)
        rssi = rsrp + 10 * np.log10(12)
        #RSRQ is calculate as RSRQ = (N * RSRP) / RSSI
        # RSRQ-Range in TS 38331 is INTEGER(0..127)
        rsrq = rsrp / rssi

        bler = np.random.exponential(2, (self.n_ues, 1, 1))
        bler = bler * (1 - bler > 1)
        cqi_threshold = [-9.478, -6.658, -4.098, -1.798, 
                          0.399,  2.424,  4.489,  6.367, 
                          8.456, 10.266, 12.218, 14.122, 
                         15.849, 17.786, 19.809]
        cqi = np.sum([snr < cqi_thresh for cqi_thresh in cqi_threshold], axis = 0)

        return rsrp, snr, rsrq, bler, cqi

if __name__ == '__main__':
    from multiprocessing.pool import ThreadPool, Pool
    import sys, yaml, getopt

    configfile = '/etc/config/configmap/application.yaml'

    opts, args = getopt.getopt(sys.argv[1:], 'c:')

    for opt, arg in opts:
        if opt == 'c':
            configfile = arg

    with open(configfile, 'r') as fp:
        config = yaml.safe_load(fp)

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

    def random_flow():
        return e2sim_client.DataPlaneFlow(average_throughput=np.random.randint(0, 1000000), latency=np.random.uniform(0, 20))


    def create_ue(ue_number, bbu_values):
        anr_values = [_anr(bbu, rsrp, snr, rsrq, cqi, bler) for bbu, rsrp, snr, rsrq, cqi, bler in bbu_values]
        flow =  random_flow()
        ip = _get_endpoint_ip()
        return e2sim_client.UeDescriptor(data_plane_flow = flow, anr_payload = anr_values, endpoint = f"http://{ip}:8081/{ue_number}")

    n_ues = config['ues']['quantity']
    n_cells = len(config['antennae'])
    exp = experiment(n_ues, n_cells)

    antennae = [exp.add_cell(antenna) for antenna in config['antennae']]
    print(antennae)

    ues = [exp.add_ue(random_position(), 2) for i in range(n_ues)]
    # rsrp, snr, rsrq, bler, cqi
    rsrp, snr, rsrq, bler, cqi = exp._simulate()
    rsrp = np.reshape(rsrp, (n_ues, n_cells))
    snr = np.reshape(snr, (n_ues, n_cells))
    rsrq = np.reshape(rsrq, (n_ues, n_cells))
    cqi = np.reshape(cqi, (n_ues, n_cells))
    bbu_descriptors = [e2sim_client.NodebDescriptor(nodeb_id=antenna['gnb_id']) for antenna in antennae]
 
    print(f'rsrp {rsrp.min()} {rsrp.max()}')
    print(f'snr {snr.min()} {snr.max()}')
    print(f'rsrq {rsrq.min()} {rsrq.max()}')

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
            print(f"connecting ue 724011{ue:09} to antenna {connection_bbu}")
            configuration = e2sim_client.Configuration(host=ant_endpoints[connection_bbu])
            api_client = e2sim_client.ApiClient(configuration)
            management_api = e2sim_client.ManagementApi(api_client)

            start = time.monotonic_ns()
            try:
                admission_req = UEIMSIAdmissionPutRequest(ue=ue_descr, noded=connection_bbu)
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
