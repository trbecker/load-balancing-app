import connexion
from ue_server import encoder
from typing import Dict
from typing import Tuple
from typing import Union

from ue_server.models.cell_gnb_id_power_put_request import CellGnbIdPowerPutRequest  # noqa: E501
from ue_server.models.ueimsi_handover_put_request import UEIMSIHandoverPutRequest  # noqa: E501
from ue_server import util

simulator = None

def cell_gnb_id_power_put(gnb_id, cell_gnb_id_power_put_request):  # noqa: E501
    """cell_gnb_id_power_put

     # noqa: E501

    :param gnb_id: 
    :type gnb_id: int
    :param cell_gnb_id_power_put_request: 
    :type cell_gnb_id_power_put_request: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    try:
        if connexion.request.is_json:
            cell_gnb_id_power_put_request = CellGnbIdPowerPutRequest.from_dict(connexion.request.get_json())  # noqa: E501
            simulator.get_cell(gnb_id).set_power(cell_gnb_id_power_put_request.target_power)
        else:
            return ('Invalid format', 400)
    except KeyError as e:
        return (f'gnb {gnb_id} net defined', 404)
    except Exception as e:
        return (f'{e}', 500)
    


def test_get():  # noqa: E501
    """test_get

     # noqa: E501


    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if not simulator:
        return ("Simulator is None", 500)
    return "doing magic..."


def u_eimsi_disconnect_put(i_msi):  # noqa: E501
    """u_eimsi_disconnect_put

     # noqa: E501

    :param i_msi: 
    :type i_msi: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    try:
        simulator.get_ue(i_msi).disconnect()
        return ("Accepted", 202)
    except KeyError as e:
        return (f'No UE with id {i_msi}', 404)
    except Exception as e:
        return (f'Error {e} ({i_msi} {simulator} {simulator.get_ue(i_msi)})', 500)


def u_eimsi_handover_put(i_msi, ueimsi_handover_put_request):  # noqa: E501
    """u_eimsi_handover_put

     # noqa: E501

    :param i_msi: 
    :type i_msi: str
    :param ueimsi_handover_put_request: 
    :type ueimsi_handover_put_request: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    
    try:
        if connexion.request.is_json:
            ueimsi_handover_put_request = UEIMSIHandoverPutRequest.from_dict(connexion.request.get_json())  # noqa: E501
            simulator.get_ue(i_msi).handover(ueimsi_handover_put_request.target_cell)
            return ('Accepted', 202)
        else:
            return ('Accepting JSON only', 400)
    except KeyError as e:
        return (f'UE {i_msi} is not defined', 404)
    except Exception as e:
        return (f'{e}', 500)


def u_eimsi_test_put(i_msi):  # noqa: E501
    """u_eimsi_test_put

     # noqa: E501

    :param i_msi: 
    :type i_msi: str

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if simulator:
        try:
            simulator.get_ue(i_msi)
            return (f'{i_msi} exists', 200)
        except KeyError as e:
            return (f'{i_msi} doesn\'t exist', 404)
        except Exception as e:
            return (f'{e}', 500)
    return ('Simulator is not set', 500)

def start_server(port):
    app = connexion.App(__name__, specification_dir="./openapi/")
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'UE Control API'},
                pythonic_params=True)
    app.run(port=8080)

if __name__ == '__main__':
    import controllers
    controllers.simulator = 'a'
    start_server(8080)