import openapi_client as e2sim_client
from multiprocessing.pool import ThreadPool
import numpy as np
import connexion
from ue_server import encoder

def ftoi(v):
    return int(np.floor(v))

def auto_connection_task(data):
    ue, target_cells, c_manager = data
    return connect_task(ue, target_cells, c_manager)

def connect_task(ue, target_cells, c_manager):
    connected = False
    cells = target_cells.copy()
    # create anr payload
    anr = [ e2sim_client.AnrPayload(
        nodeb=e2sim_client.NodebDescriptor(nodeb_id=int(cell.id)),
        rsrp=ftoi(rsrp),
        rsrq=ftoi(rsrq), 
        sinr=ftoi(sinr),
        bler=ftoi(bler),
        cqi=ftoi(cqi)
    ) for (cell, sinr, rsrp, rsrq, bler, cqi) in ue.connection_metrics]

    flow = e2sim_client.DataPlaneFlow(average_throughput=1000000, latency=10)
    ue_descriptor = e2sim_client.UeDescriptor(data_plane_flow = flow, anr_payload = anr,
                                              endpoint = ue.endpoint)

    while not connected:
        target_cell = cells.pop()
        configuration = e2sim_client.Configuration(host=target_cell.endpoint)
        api_client = e2sim_client.ApiClient(configuration)
        management_api = e2sim_client.ManagementApi(api_client)

        try:
            admission_req = e2sim_client.UEIMSIAdmissionPutRequest(
                ue=ue_descriptor,
                nodeb=target_cell.id
            )
            management_api.u_eimsi_admission_put(ue.id, admission_req)
            connected = True
            c_manager.connections[ue.id] = target_cell
            print(f'{ue.id} connected to {target_cell.id}')
        except Exception as e:
            print(e)
            raise e

def disconnect_task(ue, c_manager):
    connected_cell = c_manager.connections[ue.id]
    configuration = e2sim_client.Configuration(host=connected_cell.endpoint)
    api_client = e2sim_client.ApiClient(configuration)
    management_api = e2sim_client.ManagementApi(api_client)

    try:
        management_api.u_eimsi_admission_delete(ue.id)
        del c_manager.connections[ue.id]
    except Exception as e:
        print(f'{e}')

def start_server():
    app = connexion.App('ue_manager', specification_dir='./openapi')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml', arguments={'title': 'EU Control API'}, pythonic_params=True)
    app.run(port=8080, debug=True)

class ConnectionManager:
    def __init__(self, simulator, thread_pool_procs=100):
        self.connections = dict()
        self.simulator = simulator
        self.pool = ThreadPool(processes=thread_pool_procs)
        self.listener_thread = None
        simulator.connection_manager = self

    def handover(self, ue, target_cell):
        self.disconnect(ue)
        self.connect(ue, [target_cell])
    
    def disconnect(self, ue):
        data = (ue, self)
        self.pool.apply(disconnect_task, data)

    def connect(self, ue, target_cells):
        self.pool.apply(connect_task, (ue, target_cells, self))

    def auto_connect(self, ues, cells):
        # Need to have called simulator.simulate before
        #ue_pos = [ue.pos for ue in ues]
        #cell_pos = [cell.pos for cell in cells]

        connection_order = self.simulator.sinr.argsort(axis=1)
        connection_order = connection_order.reshape((self.simulator.n_ues, self.simulator.n_cells))

        data = [ (ue, [cells[i] for i in connection_order[ue.idx]], self) for ue in ues ]

        self.pool.map(auto_connection_task, data)

    def start(self):
        start_server()