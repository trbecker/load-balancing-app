import json
import os
import queue
import time

from ricxappframe.rmr import rmr
from ricxappframe.util.constants import Constants
from ricxappframe.xapp_frame import Xapp

class AdmissionControlXapp(Xapp):
    def __init__(self, rmr_port=4560, rmr_timeout=5):
        super().__init__(None, rmr_port=rmr_port)
        self._keepgoing = True
        self.rmr_timeout = rmr_timeout
        self.rmr_port = rmr_port
        self.rmr_registered = False

    def healthcehck_handler(self, summary, buf):
        healthy = self.healthcheck()
        payload = b"OK\n" if healthy else b"ERROR [RMR or SDL is not healthy]\n"
        self.rmr_rts(buf, new_payload=payload, new_mtype=Constants.RIC_HEALTH_CHECK_RESP)
        self.rmr_free(buf)

    def default_handler(self, summary, buf):
        print(f"Message sent to default handler: {summary} {buf}")
        if summary[rmr.RMR_MS_MSG_TYPE] == Constants.RIC_HEALTH_CHECK_REQ:
            self.healthcehck_handler(summary, buf)

    def rmr_handler(self, summary, buf):
        return False

    def run(self):
        print("AdmissionControlXapp starting")
        while self._keepgoing:
            try:
                summary, buf = self._rmr_loop.rcv_queue.get(block=True, timeout=self.rmr_timeout)
                if not self.rmr_handler(summary, buf):
                    self.default_handler(summary, buf)
            except queue.Empty:
                pass
    
    def register(self):
        print("Registering")
        hostname = os.environ.get("HOSTNAME")
        xappversion = "0.0.2"
        config_path = os.environ.get("CONFIG_FILE")
        xappname = "admission-control-xapp"
        service_name = f"service-ricxapp-{hostname}"
        http_endpoint = f"{service_name}-http.ricxapp:8080"
        rmr_endpoint = f"{service_name}-rmr.ricxapp:{self.rmr_port}"
        pltnamespace = Constants.DEFAULT_PLT_NS

        request_string = {
            "appName": hostname,
            "appVersion": xappversion,
            "configPath": config_path,
            "appInstanceName": xappname,
            "httpEndpoint": http_endpoint,
            "rmrEndpoint": rmr_endpoint,
            "config": json.dumps(self._config_data)
        }
        print(f"REQUEST STRING: {request_string}, ENDPOINT: {Constants.REGISTER_PATH}")
        self.rmr_registered = self.do_post(pltnamespace, Constants.REGISTER_PATH, request_string)
        print(f"RMR regsitered {self.rmr_registered}")
        return self.rmr_registered

    def wait_rmr_registration(self, retries=5):
        while not self.rmr_registered and retries:
            retries -= 1
            time.sleep(1)
        
        if not self.rmr_registered:
            raise RuntimeError("Failed to register to RMR")

        print("Finished RMR registration")

    def start(self):
        self.wait_rmr_registration()
        print("Querying A1 policies")
        self.rmr_send('{"policy_type_id": 20008}', 20013) # A1_POLICY_QUERY = 20013
        self.run()

    def stop(self):
        super().stop()
        self.logger.info("Stopping application")
        self._keepgoing = False


if __name__ == '__main__':
    import signal

    lbxapp = AdmissionControlXapp()

    def signal_handler(sig, frame):
        lbxapp.stop()

    signal.signal(signal.SIGINT, signal_handler)

    # Configuration
    lbxapp.run()
