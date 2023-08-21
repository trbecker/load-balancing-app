package datamodel

func (i *Intent) SetMinimumCellOffset(offset int) *Intent {
	i.MinimumCellOffset = &offset
	return i
}

func (i *Intent) UnsetMinimumCellOffset(offset int) *Intent {
	i.MinimumCellOffset = nil
	return i
}

func (i *Intent) SetMaximumCellOffset(offset int) *Intent {
	i.MaximumCellOffset = &offset
	return i
}

func (i *Intent) SetMaximumLoadAverage(loadAverage int) *Intent {
	i.MaximumLoadAverage = &loadAverage
	return i
}

func (i *Intent) SetMinimumThroughput(throughput int) *Intent {
	i.MinimumThroughput = &throughput
	return i
}

func (i *Intent) SetMaximumUEPerCell(maximumUEPerCell int) *Intent {
	i.MaximumUEPerCell = &maximumUEPerCell
	return i
}

func (i *Intent) SetMaximumAssociationRate(associationRate int) *Intent {
	i.MaximumAssociationRate = &associationRate
	return i
}
