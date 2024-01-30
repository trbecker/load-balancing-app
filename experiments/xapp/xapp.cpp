#include <sstream>
#include <thread>
#include <grpc++/grpc++.h>
#include <sqlite3.h>
#include <admissiongrpc/admission_srv.h>
#include "intent/intent.grpc.pb.h"

using intent::Intent;
using intent::IntentRequest;
using intent::IntentResponse;
using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::Status;

class Database {
public:
    Database(std::string &path);
    virtual ~Database();
    int insert_admission_request(const std::string &imsi, const std::string &gnb, const float sinr, const bool result);
    int retrieve_admissions_on_gnb(const std::string &gnb);
    int retrieve_last_second_admissions (const std::string &gnb);
private:
    sqlite3 *database;
};

Database::Database(std::string &path) : database(NULL)
{
    int rc;
    char *zErrMsg;
    if ((rc = sqlite3_open(path.c_str(), &this->database))) {
        std::cerr << "Failed to create database (" << rc << ")" << std::endl;
        this->database = NULL;
    }

    std::string sql("CREATE TABLE IF NOT EXISTS ADMISSIONS("
        "TIMESTAMP DATTETIME DEFAULT CURRENT_TIMESTAMP,"
        "GNB CHAR NOT NULL,"
        "IMSI CHAR NOT NULL,"
        "SINR REAL DEFAULT 0,"
        "LATENCY INT DEFAULT 0,"
        "RESULT BOOL);"
        "CREATE INDEX gnb ON ADMISSIONS(GNB);"
        "create index result on admissions(result);");
    
    if ((rc = sqlite3_exec(database, sql.c_str(), NULL, 0, &zErrMsg)) != SQLITE_OK) {
        std::cerr << "Failed to create table " << zErrMsg << std::endl;
    }
}

int Database::insert_admission_request(const std::string &imsi, const std::string &gnb, const float sinr, const bool result)
{
    int rc;
    std::stringstream sstream;
    char *errmsg = NULL;

    sstream << "INSERT INTO ADMISSIONS (GNB, IMSI, SINR, RESULT) VALUES ("
            << "\"" << gnb << "\", "
            << "\"" << imsi << "\", "
            << "0.0, "
            << (result ? "1" : "0") << ");";

    std::string sql = sstream.str();

    //std::cout << "Inserting admission into database: " << sql << std::endl;

    if ((rc = sqlite3_exec(database, sql.c_str(), NULL, NULL, &errmsg)) != SQLITE_OK) {
        std::cerr << "Failed to insert data in database (" << sql << "): " << errmsg << std::endl;
        return 1;
    }

    return 0;
}

int Database::retrieve_admissions_on_gnb(const string &gnb) {
    int retval = -1;
    char *errmsg;
    sqlite3_stmt *stmt;
    std::stringstream sstream;
    
    sstream << "SELECT count(gnb) FROM ADMISSIONS WHERE GNB = \"" << gnb << "\";";
    string sql = sstream.str();

    sqlite3_prepare(database, sql.c_str(), sql.size(), &stmt, NULL);

    if (sqlite3_step(stmt) == SQLITE_ROW) {
        retval = sqlite3_column_int(stmt, 0);
    }

    sqlite3_finalize(stmt);

    return retval;
}

int Database::retrieve_last_second_admissions(const std::string &gnb) {
    int retval = -1;
    char *errmsg;
    sqlite3_stmt *stmt;
    std::stringstream sstream;

    sstream << "SELECT count(imsi) FROM ADMISSIONS WHERE GNB = \"" << gnb << "\""
            "AND RESULT = 1 AND timestamp >= Datetime('now', '-1 seconds')";
    string sql = sstream.str();

    sqlite3_prepare(database, sql.c_str(), sql.size(), &stmt, NULL);

    if (sqlite3_step(stmt) == SQLITE_ROW)
    {
        retval = sqlite3_column_int(stmt, 0);
    }

    sqlite3_finalize(stmt);

    return retval;
}

Database::~Database()
{
    sqlite3_close(database);
}

std::shared_ptr<Database> database;

class JustOk : public AdmissionObserver
{
public:
    JustOk() : limit_admitted(false), limit_admission_per_second(false),
            admitted_limit(0), admission_per_second_limit(0) { /* pass*/ }

    bool admission(const string &imsi, const string &gnb, const float sinr) {
        //std::cout << "admission of " << imsi << " on " << gnb << std::endl;

        // if (limit_admitted) result = database->retrieve_admissions_on_gnb(gnb) < admitted_limit; (but possibly with no branch)
        bool result = (!limit_admitted || database->retrieve_admissions_on_gnb(gnb) < admitted_limit);

        // if (limit_admission_per_second) result = result && database->retrieve_last_second_admission_per_gnb(gnb) < admission_per_second_limit
        result = result && (!limit_admission_per_second ||
                database->retrieve_last_second_admissions(gnb) < admission_per_second_limit);

        database->insert_admission_request(imsi, gnb, sinr, result);
        return result;
    }

    void set_admission_limit(int limit) {
        limit_admitted = true;
        admitted_limit = limit;
    }

    void clear_admission_limit() {
        limit_admitted = false;
    }

    void set_admission_per_second_limit(int limit) {
        limit_admission_per_second = true;
        admission_per_second_limit = limit;
    }

    void clear_admission_per_second_limit() {
        limit_admission_per_second = false;
    }

protected:
    bool limit_admitted;
    bool limit_admission_per_second;
    int admitted_limit;
    int admission_per_second_limit;
};

class IntentImpl : public Intent::Service {
public:
    IntentImpl(std::shared_ptr<JustOk> observer);
    Status setIntent(ServerContext *context,
            const IntentRequest *request, IntentResponse *response);

private:
    std::shared_ptr<JustOk> observer;
};

IntentImpl::IntentImpl(std::shared_ptr<JustOk> observer) :
    observer(observer) { /*pass*/ }

Status IntentImpl::setIntent(ServerContext *context,
        const IntentRequest *request, IntentResponse *response)
{
    std::cout << "Received intent ["
              << "limitUE = " << request->limitueadmitted() << ", "
              << "limitAdmission = " << request->limitueadmissionpersecond()
              << "]" << std::endl;

    if (request->limitueadmitted() > 0)
        observer->set_admission_limit(request->limitueadmitted());
    else
        observer->clear_admission_limit();

    if (request->limitueadmissionpersecond() > 0)
        observer->set_admission_per_second_limit(request->limitueadmissionpersecond());
    else
        observer->clear_admission_per_second_limit();

    
    response->set_status(true);
    return Status::OK;
}

struct intent_server_data {
    std::string serverAddress;
    std::shared_ptr<JustOk> observer;
};

void runIntentServer(struct intent_server_data * data) {
    IntentImpl impl(data->observer);
    ServerBuilder builder;

    builder.AddListeningPort(data->serverAddress, grpc::InsecureServerCredentials());
    builder.RegisterService(&impl);

    std::unique_ptr<Server> server(builder.BuildAndStart());
    server->Wait();
}

int main(int argc, char **argv)
{
    string serverAddress("0.0.0.0:50101");
    string intentServerAddress("0.0.0.0:50102");
    string databasePath("/data/experiment.db");

    database = std::make_shared<Database>(databasePath);

    std::shared_ptr<JustOk> observer = std::make_shared<JustOk>();
    std::shared_ptr<AdmissionObserver> admissionObserver =
            std::static_pointer_cast<AdmissionObserver>(observer);
    struct intent_server_data intent_server_data;
    intent_server_data.observer = observer;
    intent_server_data.serverAddress = intentServerAddress;

    std::thread intentThread(runIntentServer, &intent_server_data);

    runServer(serverAddress, admissionObserver);
    return 0;
}