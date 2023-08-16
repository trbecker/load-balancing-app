package datamodel

const (
	MinimumCellOffset int = iota
	MaximumCellOffset
	MaximumLoadAverage
	MinimumThroughput
	MaximumUEPerCell
	MaximumAssociationRate
)

type IntentParameter struct {
	Type int `json:"parameter_type"`
}

type MinimumCellOffsetParam struct {
	Offset int `json:"offset"`
	IntentParameter
}

func NewMinimumCellOffset(offset int) MinimumCellOffsetParam {
	return MinimumCellOffsetParam{
		Offset: offset,
		IntentParameter: IntentParameter{
			Type: MinimumCellOffset,
		},
	}
}

type MaximumCellOffsetParam struct {
	Offset int `json:"offset"`
	IntentParameter
}

func NewMaximumCellOffset(offset int) MaximumCellOffsetParam {
	return MaximumCellOffsetParam{
		Offset: offset,
		IntentParameter: IntentParameter{
			Type: MaximumCellOffset,
		},
	}
}

type MaximumLoadAverageParam struct {
	LoadAverage int `json:"load_avg"`
	IntentParameter
}

func NewMaximumLoadAverage(loadAverage int) MaximumLoadAverageParam {
	return MaximumLoadAverageParam{
		LoadAverage: loadAverage,
		IntentParameter: IntentParameter{
			Type: MaximumLoadAverage,
		},
	}
}

type MinimumThroughputParam struct {
	MinimumThroughput int `json:"min_throughput"`
	IntentParameter
}

func NewMinimumThroughput(minimumTroughput int) MinimumThroughputParam {
	return MinimumThroughputParam{
		MinimumThroughput: minimumTroughput,
		IntentParameter: IntentParameter{
			Type: MinimumThroughput,
		},
	}
}

type MaximumUEPerCellParam struct {
	MaximumUEPerCell int `json:"max_ue_per_cell"`
	IntentParameter
}

func NewMaximumUEPerCell(maximumUEPerCell int) MaximumUEPerCellParam {
	return MaximumUEPerCellParam{
		MaximumUEPerCell: maximumUEPerCell,
		IntentParameter: IntentParameter{
			Type: MaximumUEPerCell,
		},
	}
}

type MaximumAssociationRateParam struct {
	MaximumAssociationRate int `json:"max_ue_accept_per_second"`
	IntentParameter
}

func NewMaximumAssociationRate(acceptanceRate int) MaximumAssociationRateParam {
	return MaximumAssociationRateParam{
		MaximumAssociationRate: acceptanceRate,
		IntentParameter: IntentParameter{
			Type: MaximumAssociationRate,
		},
	}
}
