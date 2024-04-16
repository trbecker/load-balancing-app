import numpy as np
import socket

import openapi_client as e2sim_client
import controllers

speed_of_light = 299792485 # m/s
MHz = 1000000 # Hz
kHz = 1000 # Hz
minute = 60 # second
k_b = 1.380649e-23 # Boltzmann contant [J/K]

endpoint = socket.gethostbyname(socket.gethostname())

class UE:
    def __init__(self, simulator, position, id):
        self.__simulator = simulator
        self.__position = position
        self.__id = id

    def __getattr__(self, attr):
        if attr == 'position':
            return self.__simulator.ue_positions[self.__position, 0, :]
        if attr == 'gain':
            return self.__simulator.ue_gains[self.__position, 0, 0]
        if attr == 'id':
            return self.__id
        if attr == 'endpoint':
            return f'http://{endpoint}:8081/v1/UE/{self.__id}'
        if attr == 'flow':
            return np.random.randint(0, 1000000)
        if attr == 'latency':
            return np.random.uniform(0, 20)
        if attr == 'sinr':
            return self.__simulator.sinr[self.__position].reshape(self.__simulator.n_cells)
        if attr == 'rsrp':
            return self.__simulator.rsrp[self.__position].reshape(self.__simulator.n_cells)
        if attr == 'rsrq':
            return self.__simulator.rsrq[self.__position].reshape(self.__simulator.n_cells)
        if attr == 'bler':
            return self.__simulator.bler[self.__position]
        if attr == 'cqi':
            return self.__simulator.cqi[self.__position].reshape(self.__simulator.n_cells)
        if attr == 'connection_metrics':
            cells = [cell for _, cell in self.__simulator.cells.items()]
            sinr = list(self.sinr)
            rsrp = list(self.rsrp)
            rsrq = list(self.rsrq)
            bler = list(self.bler[0]) * len(cells)
            cqi  = list(self.cqi)
            return list(zip(cells, sinr, rsrp, rsrq, bler, cqi))
        if attr == 'idx':
            return self.__position
        raise AttributeError(f'{attr} is not defined for UE')

    def get_connection_parameters(self, target_cell):
        for metrics in self.connection_metrics:
            if target_cell.id == metrics[0].id:
                return metrics
        raise NameError(f'{target_cell.id} is not defined')

    def connect(self, target_cell):
        print(f'{self.id} is connectiong to {target_cell.gnb_id}')
        if not self.__simulator.connection_manager:
            raise RuntimeError("Missing connection manager")
        self.__simulator.connection_manager.connect(self, [target_cell])

    def handover(self, target_cell):
        print(f'{self.id} is being handed over to {target_cell.gnb_id}')
        if not self.__simulator.connection_manager:
            raise RuntimeError("missing connection manager")
        self.disconnect()
        self.connect(target_cell)

    def disconnect(self):
        print(f'{self.id} is disconnecting')
        if not self.__simulator.connection_manager:
            raise RuntimeError("missing connection manager")
        self.__simulator.connection_manager.disconnect(self)

class Cell:
    def __init__(self, simulator, position, ant):
        self.__simulator = simulator
        self.__position = position
        self.__ant = ant

    def __getattr__(self, attr):
        if attr == 'position':
            return self.__simulator.cell_positions[0, self.__position, :]
        if attr == 'id':
            return self.__ant['gnb_id']
        
        try:
            return self.__ant[attr]
        except Exception as e:
            print(f'Error {e} when trying to access {attr}')
            raise AttributeError(f'{attr} is not defined for Cell')

    def set_power(self, target_power):
        self.__simulator.cell_power[0, self.__position, :] = target_power

class Simulator:
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
        self.connection_manager = None

        self.gamma = 1

        self.ues = dict()
        self.cells = dict()

    def add_ue(self, ue_location, ue_gain):
        pos = self.current_ue
        self.current_ue += 1

        self.ue_positions[pos, 0] = ue_location
        self.ue_gains[pos] = ue_gain

        ue = UE(self, pos, f'724011{pos:09}')

        self.ues[ue.id] = ue
        return ue

    def move_ues(self):
        move = np.random.uniform(0, 1, self.ue_positions.shape)
        move[:, 0, 2] = 0
        self.ue_positions += move

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
        self.cell_power[0, pos] = ant['power'] * 1000 # [mW]

        a = Cell(self, pos, ant)
        self.cells[ant['gnb_id']] = a

        return a

    def get_ue(self, ue):
        return self.ues[ue]
    
    def get_cell(self, antenna):
        return self.cells[antenna]
    
    def __getattr__(self, attr):
        if attr == 'ue_names':
            return [name for name, _ in self.ues.items()]
        if attr == 'cell_names':
            return [name for name, _ in self.cells.items()]
    

    def _simulate(self):
        distances = np.reshape(np.linalg.norm(self.ue_positions - self.cell_positions, axis = 2), (self.n_ues, self.n_cells, 1))

        power_rx = (self.cell_power * self.cell_gains * self.ue_gains) * (self.cell_wave_lengths / (4 * np.pi * distances)) ** 2 # [mW]
        noise = k_b * np.random.normal(300, 1, self.ue_gains.shape) * self.subcarrier_spacing * 1000 # [J/K] [K] [1/s] [1/1000] = [J/1000/s] = [mW]
        power_rx_sum = np.sum(power_rx, axis=2) # [mw]
        power_rx_sum = np.reshape(power_rx_sum, (power_rx_sum.shape[0], power_rx_sum.shape[1], 1)) # [mW]
        power_rx_avg = power_rx_sum / power_rx.shape[2] # [mW]
        # SINR-Range in TS 38331 is INTEGER(0..127)
        snr = 10 * np.log10(power_rx_avg / noise) # dbm
        # bw = 12 * 240000 * np.log2(1 + power_rx_avg / noise) / 1024 / 1024
        path_losses_lin = self.cell_power / power_rx_avg # [mW] / [mW] = []
        path_losses_db = 10 * self.gamma * np.log10(path_losses_lin) # [dB]
        shadowing = np.random.normal(0, 7.9, path_losses_db.shape) # [dB]
        path_losses_db += shadowing # [dB]
        # From http://4g5gworld.com/blog/5gnr-reference-signals-measurement
        # https://www.techplayon.com/rsrp/
        # rsrp-range in TS 38331 is INTEGER(0..127)
        rsrp = 10 * np.log10(self.cell_power) - path_losses_db # [dbm]
        # RSSI is calculated from the formula RSRP = RSSI - 10 * log_{10} (12 * N) [RSSI = RSRP + log_{10} (12 * N)], with N the number of resource blocks.
        # N is dependent on UE_BW (N = BW / (12 * subcarrier_spacing)). We will assume N = 1 for this test case.
        # https://www.techplayon.com/rssi/
        # RSSI-Range in TS 38331 is INTEGER(0..76)
        rssi = rsrp + 10 * np.log10(12) # RSSI under full load [dbm]
        #RSRQ is calculate as RSRQ = (N * RSRP) / RSSI
        # RSRQ-Range in TS 38331 is INTEGER(0..127)
        rsrq = rsrp / rssi # [dbm]

        bler = np.random.exponential(2, (self.n_ues, 1, 1)) # [bit/s]
        bler = bler * (1 - bler > 1)
        cqi_threshold = [-9.478, -6.658, -4.098, -1.798, 
                          0.399,  2.424,  4.489,  6.367, 
                          8.456, 10.266, 12.218, 14.122, 
                         15.849, 17.786, 19.809]
        cqi = np.sum([snr < cqi_thresh for cqi_thresh in cqi_threshold], axis = 0)

        self.sinr, self.rsrp, self.rsrq, self.bler, self.cqi = snr, rsrp, rsrq, bler, cqi

        return snr, rsrp, rsrq, bler, cqi

def __ue_random_position():
    return np.random.uniform(0, 100, (1, 1, 3))

def build_simulation_from_yaml(configfile, position_function):
    import yaml
    with open(configfile, 'r') as fp:
        config = yaml.safe_load(fp)

    n_ues = config['ues']['quantity']
    n_cells = len(config['antennae'])
    simulator = Simulator(n_ues, n_cells)

    antennae = [simulator.add_cell(antenna) for antenna in config['antennae']]
    ues = [simulator.add_ue(position_function(), 2) for i in range(n_ues)]

    return simulator, antennae, ues

def prepare_simulation(configfile, position_function=__ue_random_position):
    simulation, antennae, ues = build_simulation_from_yaml(configfile, position_function)
    n_ues = simulation.n_ues
    n_cells = simulation.n_cells
    controllers.simulator = simulation
    return simulation, antennae, ues