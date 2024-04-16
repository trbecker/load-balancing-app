#include <iostream>
#include <memory>
#include <signal.h>
#include <unistd.h>
#include <vector>

#include <envman/environment_manager.h>
#include <admissiongrpc/admission_clnt.h>

EnvironmentManager *manager;
int32_t gnbid;

class SimpleObserver : public EnvironmentManagerObserver {
public:
    SimpleObserver(const std::string &serverAddress);
    void anrUpdate(const std::string iMSI,
                   const std::map<int32_t, std::shared_ptr<anr_entry>> &entries);
    void flowUpdate(const std::string iMSI, const flow_entry &entry);
    void disassociationRequest(const std::shared_ptr<ue_data> ue);
    bool associationRequest(const std::shared_ptr<ue_data> ue, const int32_t &cell);

protected:
    std::unique_ptr<AdmissionClient> admissionClient;
};

SimpleObserver::SimpleObserver(const std::string &serverAddress) :
    admissionClient(createClient(serverAddress))
{ 
    std::cout << "Initializing observer" << std::endl;    
}

void SimpleObserver::anrUpdate(const std::string iMSI,
                               const std::map<int32_t, std::shared_ptr<anr_entry>> &entries)
{ 
    std::cout << "Got anr update, nothing to do here" << std::endl;
}

void SimpleObserver::flowUpdate(const std::string iMSI, const flow_entry &entry)
{
    std::cout << "Got flow update, nothing to do here" << std::endl;
}

void SimpleObserver::disassociationRequest(const std::shared_ptr<ue_data> ue)
{
    std::cout << "Got disassociation request, nothing to do here" << std::endl;
}

bool SimpleObserver::associationRequest(const std::shared_ptr<ue_data> ue, const int32_t &cell)
{
    float sinr = 0;
    std::cout << "Got association request, asking it" << std::endl;
    auto anr_gnb = ue->anr.find(gnbid);

    if (anr_gnb != ue->anr.end()) {
        sinr = anr_gnb->second->sinr;
        std::cout << "sinr between " << ue->imsi << " and " << gnbid
                << " is " << sinr << std::endl;
    } else {
        std::cerr << "gnb " << gnbid << " not found in anr data."
                << " available gnbs ";
        for (auto it = ue->anr.begin(); it != ue->anr.end(); it++)
            std::cerr << it->first << ", ";
        std::cerr << std::endl;
    }

    return admissionClient->requestAdmission(ue->imsi, gnbid, sinr);
}

static void sigHandler [[noreturn]] (int sig)
{
    switch (sig)
    {
    case SIGINT:
    case SIGQUIT:
    case SIGTERM:
    case SIGHUP:
    default:
        manager->stop();
        break;
    }
    exit(0);
}

static void setUpUnixSignals()
{
    std::vector quitSignals({SIGINT, SIGQUIT, SIGTERM, SIGHUP});
    sigset_t blocking_mask;
    sigemptyset(&blocking_mask);
    for (auto sig : quitSignals)
        sigaddset(&blocking_mask, sig);

    struct sigaction sa;
    sa.sa_handler = sigHandler;
    sa.sa_mask = blocking_mask;
    sa.sa_flags = 0;

    for (auto sig : quitSignals)
        sigaction(sig, &sa, nullptr);
}

int main(int argc, char **argv)
{
    std::cout << "Hello, let us start this container" << std::endl;
    char c;
    std::string serverAddress("xapp:50101");

    std::cout << "Setting up signals" << std::endl;

    setUpUnixSignals();

    std::cout << "Parsing command line" << std::endl;

    while((c = getopt(argc, argv, "i:s:")) != -1) {
        switch (c)
        {
        case 'i':
            gnbid = atoi(optarg);
            std::cout << "-i " << gnbid << std::endl;
            break;
        case 's':
            serverAddress = optarg;
            std::cout << "-s " << serverAddress << std::endl;
            break;
        
        default:
            std::cout << "unknown argument -" << c << " " << optarg << std::endl;
            break;
        }
    }

    std::cout << "Starting environment manager" << std::endl;

    manager = new EnvironmentManager(8081, 2);

    std::cout << "Creating observer" << std::endl;

    std::shared_ptr<SimpleObserver> observer = std::make_shared<SimpleObserver>(serverAddress);

    std::cout << "observer created, adding it to the manager" << std::endl;

    manager->add_observer(observer, ENVMAN_OBSERVE_ADMISSION);

    std::cout << "Starting manager" << std::endl;

    manager->start();
    return 0;
}
