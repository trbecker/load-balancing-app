package client

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"time"

	"github.com/trbecker/lbapp/datamodel"
)

type Client struct {
	Uri string
}

func SendCommand(req *http.Request) (*http.Response, error) {
	req.Header.Set("Content-Type", "application/json")
	client := http.Client{Timeout: 10 * time.Second}
	return client.Do(req)
}

func (client *Client) IntentCreate(intent datamodel.Intent) (int, error) {
	intent_create := datamodel.IntentRequest{
		RequestID: 0, // XXX randomize this
		Intent:    intent,
	}

	marshal, err := json.Marshal(intent_create)
	if err != nil {
		fmt.Fprintf(os.Stderr, "failed to marshal intent (%s)", err)
		return -1, err
	}

	req, err := http.NewRequest("POST",
		fmt.Sprintf("http://%s/intent", client.Uri),
		bytes.NewReader(marshal))
	if err != nil {
		fmt.Fprintf(os.Stderr, "failed to create request (%s)", err)
		return -1, err
	}

	res, err := SendCommand(req)
	if err != nil {
		fmt.Fprintf(os.Stderr, "failed to send intent (%s)", err)
		return -1, err
	}

	switch res.StatusCode {
	case 200:
		var response datamodel.IntentResponse
		err = json.NewDecoder(res.Body).Decode(&response)
		if err != nil {
			fmt.Fprintf(os.Stderr, "failed to parse response (%s)", err)
			return -1, err
		}
		return response.IntentID, nil

	default:
		return -1, fmt.Errorf("HTTP %d", res.StatusCode)
	}
}

func (client *Client) IntentDelete(idx int) error {
	if idx < 0 {
		fmt.Fprintf(os.Stderr, "invalid intent %d", idx)
		return fmt.Errorf("inavlid intent %d", idx)
	}

	req, err := http.NewRequest("DELETE",
		fmt.Sprintf("http://%s/intent/%d", client.Uri, idx), nil)
	if err != nil {
		fmt.Fprintf(os.Stderr, "failed to create delete request %s", err)
		return err
	}

	res, err := SendCommand(req)
	if err != nil {
		fmt.Fprintf(os.Stderr, "failed to send delete command %s", err)
		return err
	}

	if res.StatusCode != 200 {
		return fmt.Errorf("HTTP %d", res.StatusCode)
	}

	return nil
}

func (client *Client) IntentShow(idx int) (*datamodel.Intent, error) {
	if idx < 0 {
		return nil, fmt.Errorf("invalid intent %d", idx)
	}

	res, err := http.Get(fmt.Sprintf("http://%s/intent/%d", client.Uri, idx))
	if err != nil {
		fmt.Fprintf(os.Stderr, "failed to get intent %s", err)
		return nil, err
	}

	var intent datamodel.Intent
	json.NewDecoder(res.Body).Decode(&intent)

	return &intent, nil
}

func (client *Client) IntentList() ([]datamodel.Intent, error) {
	res, err := http.Get(fmt.Sprintf("http://%s/intents", client.Uri))
	if err != nil {
		fmt.Fprintf(os.Stderr, "unable to obtain intent list (%s)", err)
		return nil, err
	}

	var intents []datamodel.Intent = make([]datamodel.Intent, 256)

	err = json.NewDecoder(res.Body).Decode(&intents)
	if err != nil {
		fmt.Fprintf(os.Stderr, "failed to parse the received response  (%s)", err)
		return nil, err
	}

	return intents, nil
}
