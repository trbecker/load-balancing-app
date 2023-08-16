package datamodel

type IntentRequest struct {
	Intent    Intent `json:"intent"`
	RequestID int    `json:"request_id"`
}

type IntentResponse struct {
	RequestID int `json:"request_id"`
	IntentID  int `json:"intent_id"`
}
