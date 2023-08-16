package datamodel

import (
	"encoding/json"
	"errors"
)

type Intent struct {
	Name          string            `json:"name"`
	Idx           int               `json:"idx"`
	RawParameters []json.RawMessage `json:"parameters"`
	Parameters    []interface{}     `json:"-"`
}

func (i *Intent) AddParameter(p interface{}) {
	i.Parameters = append(i.Parameters, p)
}

func (i *Intent) UnmarshalJSON(b []byte) error {
	type intent Intent
	err := json.Unmarshal(b, (*intent)(i))
	if err != nil {
		return err
	}

	for _, raw := range i.RawParameters {
		var p IntentParameter
		err = json.Unmarshal(raw, &p)
		if err != nil {
			return err
		}

		var q interface{}
		switch p.Type {
		case MinimumCellOffset:
			q = &MinimumCellOffsetParam{}
		case MaximumCellOffset:
			q = &MaximumCellOffsetParam{}
		case MaximumLoadAverage:
			q = &MaximumLoadAverageParam{}
		case MinimumThroughput:
			q = &MinimumThroughputParam{}
		case MaximumUEPerCell:
			q = &MaximumUEPerCellParam{}
		case MaximumAssociationRate:
			q = &MaximumAssociationRateParam{}
		default:
			return errors.New("unknown parameter type")
		}

		err = json.Unmarshal(raw, q)
		if err != nil {
			return err
		}
		i.Parameters = append(i.Parameters, q)
	}

	i.RawParameters = nil

	return nil
}

func (i Intent) MarshalJSON() ([]byte, error) {
	type intent Intent
	if i.Parameters != nil && i.RawParameters == nil {
		for _, p := range i.Parameters {
			b, err := json.Marshal(p)
			if err != nil {
				return nil, err
			}
			i.RawParameters = append(i.RawParameters, b)
		}
	}
	return json.Marshal((intent)(i))
}

func (i Intent) String() string {
	b, _ := json.Marshal(i)
	return string(b)
}
