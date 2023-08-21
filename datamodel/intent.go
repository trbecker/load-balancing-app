package datamodel

import "encoding/json"

type Intent struct {
	Name                   string `json:"name,omitempty"`
	Idx                    int    `json:"idx,omitempty"`
	MinimumCellOffset      *int   `json:"minimum_cell_offset,omitempty"`
	MaximumCellOffset      *int   `json:"maximum_cell_offset,omitempty"`
	MaximumLoadAverage     *int   `json:"maximum_load_average,omitempty"`
	MinimumThroughput      *int   `json:"minimum_throughput,omitempty"`
	MaximumUEPerCell       *int   `json:"maximum_ue_per_cell,omitempty"`
	MaximumAssociationRate *int   `json:"maximum_association_rate,omitempty"`
}

func (i Intent) String() string {
	b, _ := json.MarshalIndent(i, "", "\t")
	return string(b)
}
