package datamodel

func (i *Intent) SetMinimumCellOffset(offset int) *Intent {
	i.AddParameter(NewMinimumCellOffset(offset))
	return i
}

func (i *Intent) SetMaximumCellOffset(offset int) *Intent {
	i.AddParameter(NewMaximumCellOffset(offset))
	return i
}

func (i *Intent) SetMaximumLoadAverage(loadAverage int) *Intent {
	i.AddParameter(NewMaximumLoadAverage(loadAverage))
	return i
}

func (i *Intent) SetMinimumThroughput(throughput int) *Intent {
	i.AddParameter(NewMinimumThroughput(throughput))
	return i
}

func (i *Intent) SetMaximumUEPerCell(maximumUEPerCell int) *Intent {
	i.AddParameter(NewMaximumUEPerCell(maximumUEPerCell))
	return i
}

func (i *Intent) SetMaximumAssociationRate(associationRate int) *Intent {
	i.AddParameter(NewMaximumAssociationRate(associationRate))
	return i
}
