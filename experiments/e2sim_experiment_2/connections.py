import openapi_client as e2sim_client
from multiprocessing.pool import ThreadPool
import numpy as np

def ftoi(v):
    return int(np.floor(v))

def connect_task(data):
    ue, target_cells, c_manager = data
    connected = False
    cells = target_cells.copy()

    # create anr payload
    anr = [ e2sim_client.AnrPayload(
        nodeb=cell.id,
        rsrp=ftoi(rsrp),
        rsrq=ftoi(rsrq), 
        sinr=ftoi(sinr),
        bler=ftoi(bler),
        cqi=ftoi(cqi)
    ) for (cell, sinr, rsrp, rsrq, bler, cqi) in ue.connection_metrics]

    flow = None
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
                nodeb=e2sim_client.NodebDescriptor(nodeb_id=target_cell.id)
            )
            management_api.u_eimsi_admission_put(f'724011{ue.id:09}', admission_req)
            connected = True
            c_manager.connections[ue.id] = target_cell
            print(f'{ue.id} connected to {target_cell.id}')
        except Exception as e:
            print(e)

def disconnect_task(data):
    ue, c_manager = data
    connected_cell = c_manager.connections[ue.id]
    configuration = e2sim_client.Configuration(host=connected_cell.endpoint)
    api_client = e2sim_client.ApiClient(configuration)
    management_api = e2sim_client.ManagementApi(api_client)

    try:
        management_api.u_eimsi_admission_delete(ue.id)
        del c_manager.connections[ue.id]
    except Exception as e:
        print(f'{e}')

class ConnectionManager:
    def __init__(self, simulator, thread_pool_procs=100):
        self.connections = dict()
        self.simulator = simulator
        self.pool = ThreadPool(processes=thread_pool_procs)

    def handover(self, ue, target_cell):
        self.disconnect(ue)
        self.connect(ue, [target_cell])
    
    def disconnect(self, ue):
        self.pool.apply(disconnect_task, (ue, self))

    def connect(self, ue, target_cells):
        self.pool.apply(connect_task, (ue, target_cells, self))

    def auto_connect(self, ues, cells):
        pass
