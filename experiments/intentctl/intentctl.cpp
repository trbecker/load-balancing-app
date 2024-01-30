#include <unistd.h>

#include <iostream>

#include <grpc++/grpc++.h>
#include "intent/intent.grpc.pb.h"

using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;
using intent::Intent;
using intent::IntentRequest;
using intent::IntentResponse;

void usage(const char *name)
{
    std::cerr << "usage: " << name << " -s <serveraddress> "
            << " [-t <per_sec_limit>] "
            << " [-u <ue_limit>]" << std::endl;
}

int main(int argc, char **argv) {
    IntentRequest request;
    IntentResponse response;
    ClientContext ctx;

    std::string serverAddress;
    int64_t limitUE = 0;
    int64_t limitAdmissionPerSec = 0;
    char c;

    while ((c = getopt(argc, argv, "t:u:s:")) != -1) {
        switch (c)
        {
        case 't':
            limitAdmissionPerSec = atol(optarg);
            break;
        case 'u':
            limitUE = atol(optarg);
            break;
        case 's':
            serverAddress = optarg;
            break;
        
        default:
            usage(argv[0]);
            return 1;
            break;
        }
    }

    if (serverAddress.empty() || (!limitUE && !limitAdmissionPerSec)) {
        usage(argv[0]);
        return 1;
    }

    if (limitUE)
        request.set_limitueadmitted(limitUE);

    if (limitAdmissionPerSec)
        request.set_limitueadmissionpersecond(limitAdmissionPerSec);

    std::unique_ptr<Intent::Stub> client = Intent::NewStub(
        grpc::CreateChannel(serverAddress, grpc::InsecureChannelCredentials()));
    Status status = client->setIntent(&ctx, request, &response);
    
    if (!status.ok()) {
        std::cerr << "failed to set intent: (" << status.error_code() << ")" << status.error_message() << std::endl;
        return 1;
    }

    if (response.status()) {
        std::cout << "accepted" << std::endl;
        return 0;
    }
    else
    {
        std::cout << "rejected" << std::endl;
        return 1;
    }
}