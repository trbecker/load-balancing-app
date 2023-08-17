package main

import (
	"flag"
	"fmt"
	"os"

	"github.com/trbecker/lbapp/client"
	"github.com/trbecker/lbapp/datamodel"
)

var (
	_flagURI = flag.String("uri", "localhost:8080", "server uri")
	_client  client.Client
)

func CreateIntent(args []string) error {
	createIntentCmd := flag.NewFlagSet("create", flag.PanicOnError)
	flagName := createIntentCmd.String("name", "undefined", "mnemonic for the intent")
	flagMinimumCellOffset := createIntentCmd.Int("minimum-cell-offset", -1,
		"minimum cell offset")
	flagMaximumCellOffset := createIntentCmd.Int("maximum-cell-offset", -1,
		"maximum cell offset")
	flagMaximumLoadAverage := createIntentCmd.Int("maximum-load", -1,
		"maximum cell load average")
	flagMinimumThroughput := createIntentCmd.Int("minimum-throughput", -1,
		"minimum throughput per ue")
	flagMaximumUEPerCell := createIntentCmd.Int("maximum-ue-per-cell", -1,
		"maximum ue per cell")
	flagMaximumAssciationRate :=
		createIntentCmd.Int("maximum-association-rate", -1,
			"maximum number of associations accepted per second")

	createIntentCmd.Parse(args)

	var intent = datamodel.Intent{
		Name: *flagName,
	}

	if *flagMinimumCellOffset >= 0 {
		intent.SetMinimumCellOffset(*flagMinimumCellOffset)
	}

	if *flagMaximumCellOffset >= 0 {
		intent.SetMaximumCellOffset(*flagMaximumCellOffset)
	}

	if *flagMaximumLoadAverage >= 0 {
		intent.SetMaximumLoadAverage(*flagMaximumLoadAverage)
	}

	if *flagMinimumThroughput >= 0 {
		intent.SetMinimumThroughput(*flagMinimumThroughput)
	}

	if *flagMaximumUEPerCell >= 0 {
		intent.SetMaximumUEPerCell(*flagMaximumUEPerCell)
	}

	if *flagMaximumAssciationRate >= 0 {
		intent.SetMaximumAssociationRate(*flagMaximumAssciationRate)
	}

	intentID, err := _client.IntentCreate(intent)
	if err != nil {
		return err
	}
	fmt.Printf("Created intent '%s' with id %d\n", intent.Name, intentID)
	return nil
}

func ListIntents() error {
	intents, err := _client.IntentList()

	if err == nil {
		for _, intent := range intents {
			fmt.Printf("%d %s\n", intent.Idx, intent.Name)
		}
	}

	return err
}

func IntentShow(args []string) error {
	intentShowCmd := flag.NewFlagSet("intent show", flag.PanicOnError)
	flagIdx := intentShowCmd.Int("intent", -1, "id of the intent")
	intentShowCmd.Parse(args)

	intent, err := _client.IntentShow(*flagIdx)
	if err == nil {
		fmt.Println(intent)
	}
	return err
}

func IntentDelete(args []string) error {
	intentDeleteCmd := flag.NewFlagSet("intent delete", flag.PanicOnError)
	flagIdx := intentDeleteCmd.Int("intent", -1, "intent to delete")
	intentDeleteCmd.Parse(args)

	err := _client.IntentDelete(*flagIdx)

	return err
}

func main() {
	flag.Parse()
	_client = client.Client{
		Uri: *_flagURI,
	}

	command, args := flag.Args()[0], flag.Args()[1:]
	var err error
	switch command {
	case "create":
		err = CreateIntent(args)
	case "list":
		err = ListIntents()
	case "show":
		err = IntentShow(args)
	case "delete":
		err = IntentDelete(args)
	}

	if err != nil {
		fmt.Fprintf(os.Stderr, "command failed %s\n", err)
	}
}
