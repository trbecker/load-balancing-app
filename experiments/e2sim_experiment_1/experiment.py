import numpy as np
import random
import time
import openapi_client as e2sim_client

speed_of_light = 299792485
MHz = 1000000
kHz = 1000
minute = 60
k_b = 1.380649e-23 # Boltzmann contant

class experiment:
    def __init__(self, n_ues, n_cells, subcarrier_spacing):
        self.n_ues = n_ues
        self.n_cells = n_cells
        self.ue_positions = np.zeros((n_ues, 1, 3))
        self.ue_gains = np.zeros((n_ues, 1, 1))
        self.cell_positions = np.zeros((1, n_cells, 3))
        self.cell_gains = np.zeros((1, n_cells, 1))
        self.cell_wave_lengths = np.zeros((1, n_cells, 4))
        self.cell_power = np.zeros((1, n_cells, 1))
        self.current_ue = 0
        self.current_cell = 0
        self.subcarrier_spacing = subcarrier_spacing

        self.gamma = 1

    def add_ue(self, ue_location, ue_gain):
        pos = self.current_ue
        self.current_ue += 1

        self.ue_positions[pos, 0] = ue_location
        self.ue_gains[pos] = ue_gain

        return pos

    def move_ues(self):
        self.ue_positions += np.random.uniform(0, 1, self.ue_positions.shape)


    def add_cell(self, cell_location, cell_power, cell_frequency, cell_bw, cell_gain):
        pos = self.current_cell
        self.current_cell += 1

        self.cell_positions[0, pos] = cell_location
        self.cell_gains[0, pos] = cell_gain
        n_subcarriers = int(np.floor(cell_bw / self.subcarrier_spacing))
        first_subcarrier = cell_frequency - cell_bw / 2 + self.subcarrier_spacing / 2
        subcarriers = [first_subcarrier + sc * self.subcarrier_spacing for sc in range(n_subcarriers)]
        self.cell_wave_lengths[0, pos] = speed_of_light / np.random.choice(subcarriers, replace=False, size=(4,))
        self.cell_power[0, pos] = cell_power

        return pos

    def _simulate(self):
        distances = np.reshape(np.linalg.norm(self.ue_positions - self.cell_positions, axis = 2), (self.n_ues, self.n_cells, 1))

        power_rx = (self.cell_power * self.cell_gains * self.ue_gains) * (self.cell_wave_lengths / (4 * np.pi * distances)) ** 2
        noise = k_b * np.random.normal(300, 1, self.ue_gains.shape) * self.subcarrier_spacing
        power_rx_sum = np.sum(power_rx, axis=2)
        power_rx_sum = np.reshape(power_rx_sum, (power_rx_sum.shape[0], power_rx_sum.shape[1], 1))
        power_rx_avg = power_rx_sum / power_rx.shape[2]
        snr = 10 * np.log10(power_rx_avg / noise)
        bw = 12 * 240000 * np.log2(1 + power_rx_avg / noise) / 1024 / 1024
        path_losses_lin = self.cell_power / power_rx_avg
        path_losses_db = 10 * self.gamma * np.log10(path_losses_lin)
        shadowing = np.random.normal(0, 7.9, path_losses_db.shape)
        path_losses_db += shadowing
        # From http://4g5gworld.com/blog/5gnr-reference-signals-measurement
        rsrp = 10 * np.log10(self.cell_power) - path_losses_db
        print(np.mean(rsrp), np.mean(snr), np.mean(bw))
        # RSSI is calculated from the formula RSRP = RSSI - 10 * log_{10} (12 * N) [RSSI = RSRP + log_{10} (12 * N)], with N the number of resource blocks.
        # N is dependent on UE_BW (N = BW / (12 * subcarrier_spacing)). We will assume N = 1 for this test case.
        rssi = rsrp + 10 * np.log10(12)
        #RSRQ is calculate as RSRQ = (N * RSRP) / RSSI
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

    def _anr(bbu, rsrp, snr, rsrq):
        return e2sim_client.AnrPayload(nodeb=bbu, rsrp=rsrp, rsrq=rsrq, sinr=snr, cqi=0, bler=0)

    def random_flow():
        return e2sim_client.DataPlaneFlow(average_throughput=np.random.randint(0, 1000000), latency=np.random.uniform(0, 20))


    def create_ue(ue_number, bbu_values):
        anr_values = [_anr(bbu, rsrp, snr, rsrq) for bbu, rsrp, snr, rsrq in bbu_values]
        flow =  random_flow()
        ip = _get_endpoint_ip()
        return e2sim_client.UeDescriptor(data_plane_flow = flow, anr_payload = anr_values, endpoint = f"http://{ip}:8081/{ue_number}")

    def ue_connect(server_url, imsi, ue):
        configuration = e2sim_client.Configuration(
                host = server_url)
        with e2sim_client.ApiClient(configuration) as api_client:
            api_instance = e2sim_client.ManagementApi(api_client)
            try:
                api_instance.u_eimsi_admission_put(imsi, ue)
            except Exception as e:
                print("ManagementApi.u_eimsi_admission_put: %s\n" % e)

    subcarrier_spacing = 240 * kHz
    n_ues = 10000
    n_cells = 6
    update_time_minute = 2 
    exp = experiment(n_ues, n_cells, subcarrier_spacing)

    half_cells = int(n_cells / 2)

    antenna_ys = [47 + 120 / half_cells * i for i in range(half_cells)] * 2
    antenna_xs = [47] * half_cells +  [157] * half_cells
    dl_channels_f = ([ (7175 + 100 * n) * MHz for n in range(10) ] * (len(antenna_ys) // 6 + 6))[0:len(antenna_ys)]

    antennae = [exp.add_cell((x, y, 25), 10, f, 100 * MHz, 8) for x, y, f in zip(antenna_xs, antenna_ys, dl_channels_f)]
    
    ues = [exp.add_ue(random_position(), 2) for i in range(n_ues)]
    rsrp, snr, rsrq = exp._simulate()
    rsrp = np.reshape(rsrp, (n_ues, n_cells))
    snr = np.reshape(snr, (n_ues, n_cells))
    rsrq = np.reshape(rsrq, (n_ues, n_cells))
    bbu_descriptors = [e2sim_client.NodebDescriptor(nodeb_id=f'ant_{aid}') for aid in antennae]

    configuration = e2sim_client.Configuration(host="http://10.88.0.15:8081/v1")
    api_client = e2sim_client.ApiClient(configuration)
    management_api = e2sim_client.ManagementApi(api_client)

    ue_descriptors = list()

    print("Connecting UEs")

    start = time.time()
    for ue in ues:
        bbu_values = [(bbu_descriptors[i], rsrp[ue, i], snr[ue, i], rsrq[ue, i]) for i in range(len(bbu_descriptors))]
        ue_descr = create_ue(ue, bbu_values)
        ue_descriptors.append(ue_descr)

        try:
            management_api.u_eimsi_admission_put(f'{ue}', ue_descr)
        except Exception as e:
            print(f'ManagementApi.u_eimsi_admission_put: {e}')

    end = time.time()
    ellapsed = end - start
    print(f"Finished connecting UEs, ellapsed time: {ellapsed}")


    print(f"Starting ANR and flow updates every {update_time_minute} minute")
    while True:
        time.sleep(update_time_minute * minute - ellapsed)
        print("Updating anr")
        start = time.time()
        exp.move_ues()
        rsrp, snr, rsrq = exp._simulate()
        rsrp = np.reshape(rsrp, (n_ues, n_cells))
        snr = np.reshape(snr, (n_ues, n_cells))
        rsrq = np.reshape(rsrq, (n_ues, n_cells))
        for ue in ues:
            ue_descriptors[ue].anr_payload = [_anr(bbu_descriptors[i], rsrp[ue, i], snr[ue, i], rsrq[ue, i]) for i in range(len(bbu_descriptors))]
            ue_descriptors[ue].data_plane_flow = random_flow()
            try:
                management_api.u_eimsi_anr_put(f'{ue}', 
                            e2sim_client.UEIMSIAnrPutRequest(nodeb_list=ue_descriptors[ue].anr_payload))
                management_api.u_eimsi_flow_put(f'{ue}', 
                            e2sim_client.UEIMSIFlowPutRequest(flow=ue_descriptors[ue].data_plane_flow))
            except Exception as e:
                print(f'Failed to update ue {ue}: {e}')

        end = time.time()
        ellapsed = end - start
        print(f"Finished ANR updates, ellapsed time: {ellapsed}")
