package intentstore

import (
	"github.com/trbecker/lbapp/datamodel"
)

type IntentStore interface {
	/* Inserts the intent into the store. Returns the index */
	Insert(intent datamodel.Intent) (int, error)
	/* Retrieves an intent from the store. */
	Retrieve(idx int) (datamodel.Intent, error)
	/* Deletes an intent from the store */
	Delete(idx int) error
	/* List intents in the store */
	List() ([]datamodel.Intent, error)
}
