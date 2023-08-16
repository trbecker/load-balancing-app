package intentstore

import (
	"github.com/trbecker/lbapp/datamodel"
)

type MemoryTable struct {
	CurrentIdx int
	Intents    map[int]datamodel.Intent
}

func NewMemoryTable() MemoryTable {
	memoryTable := MemoryTable{
		CurrentIdx: 0,
		Intents:    make(map[int]datamodel.Intent),
	}
	return memoryTable
}

func (m *MemoryTable) Insert(intent datamodel.Intent) (int, error) {
	idx := m.CurrentIdx
	m.CurrentIdx++
	intent.Idx = idx
	m.Intents[idx] = intent
	return idx, nil
}

func (m *MemoryTable) Retrieve(idx int) (datamodel.Intent, error) {
	return m.Intents[idx], nil
}

func (m *MemoryTable) Delete(idx int) error {
	delete(m.Intents, idx)
	return nil
}

func (m *MemoryTable) List() ([]datamodel.Intent, error) {
	var intents []datamodel.Intent
	for _, intent := range m.Intents {
		intents = append(intents, intent)
	}
	return intents, nil
}
