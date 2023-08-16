package main

import (
	"encoding/json"
	"log"
	"net/http"
	"strconv"

	"github.com/gorilla/mux"
	"github.com/trbecker/lbapp/datamodel"
	"github.com/trbecker/lbapp/intentstore"
)

var intentStore intentstore.MemoryTable

func main() {
	intentStore = intentstore.NewMemoryTable()
	r := mux.NewRouter()
	r.HandleFunc("/intent", IntentCreate).Methods("POST")
	r.HandleFunc("/intents", IntentList).Methods("GET")
	r.HandleFunc("/intent/{idx}", IntentShow).Methods("GET")
	r.HandleFunc("/intent/{idx}", IntentDelete).Methods("DELETE")

	srv := &http.Server{
		Addr:    ":8080",
		Handler: r,
	}
	srv.ListenAndServe()
}

func IntentList(w http.ResponseWriter, r *http.Request) {
	intents, err := intentStore.List()
	if err != nil {
		log.Fatalf("failed to get the intent list")
	}
	json.NewEncoder(w).Encode(intents)
}

func IntentCreate(w http.ResponseWriter, r *http.Request) {
	defer r.Body.Close()
	var req datamodel.IntentRequest
	err := json.NewDecoder(r.Body).Decode(&req)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
	}

	idx, err := intentStore.Insert(req.Intent)
	if err != nil {
		log.Fatalf("failed to store the intent")
	}

	resp := datamodel.IntentResponse{
		RequestID: req.RequestID,
		IntentID:  idx,
	}
	json.NewEncoder(w).Encode(resp)
}

func IntentShow(w http.ResponseWriter, r *http.Request) {
	idxs := mux.Vars(r)["idx"]
	idx, err := strconv.Atoi(idxs)
	if err != nil {
		log.Fatalf("can't find intent by idx %s", idxs)
	}
	log.Printf("request to view intent %d", idx)
	intent, err := intentStore.Retrieve(idx)
	if err != nil {
		log.Fatalf("failed to retrieve intent %d", idx)
	}
	json.NewEncoder(w).Encode(intent)
}

func IntentDelete(w http.ResponseWriter, r *http.Request) {
	idxs := mux.Vars(r)["idx"]
	idx, err := strconv.Atoi(idxs)
	if err != nil {
		log.Fatalf("unable to delete intent %s", idxs)
	}
	log.Printf("deleting intent %d", idx)
	err = intentStore.Delete(idx)
	if err != nil {
		log.Fatalf("unable to delete intent %d", idx)
	}
	w.WriteHeader(200)
}
