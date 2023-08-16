package main

import (
	"flag"
	"fmt"
	"os"

	"github.com/trbecker/lbapp/client"
	"github.com/trbecker/lbapp/datamodel"
)

func CreateIntent() error {
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
		createIntentCmd.Int("maximum-association-acceptance-rate", -1,
			"maximum number of associations accepted per second")

	createIntentCmd.Parse(os.Args[3:])

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

	intentID, err := client.IntentCreate(intent)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to create intent %s", err)
		return err
	}
	fmt.Printf("Created intent '%s' with id %d\n", intent.Name, intentID)
	return nil
}

func ListIntents() error {
	intents, err := client.IntentList()

	if err == nil {
		for _, intent := range intents {
			fmt.Printf("%d %s\n", intent.Idx, intent.Name)
		}
	}

	return nil
}

func IntentShow() error {
	intentShowCmd := flag.NewFlagSet("intent show", flag.PanicOnError)
	flagIdx := intentShowCmd.Int("intent", -1, "id of the intent")
	intentShowCmd.Parse(os.Args[3:])

	intent, err := client.IntentShow(*flagIdx)
	if err == nil {
		fmt.Println(intent)
	}
	return err
}

func IntentDelete() error {
	intentDeleteCmd := flag.NewFlagSet("intent delete", flag.PanicOnError)
	flagIdx := intentDeleteCmd.Int("intent", -1, "intent to delete")
	intentDeleteCmd.Parse(os.Args[3:])

	err := client.IntentDelete(*flagIdx)

	if err != nil {
		fmt.Fprintf(os.Stderr, "failed to delete intent %s", err)
	}

	return err
}

func IntentCmd() error {
	switch os.Args[2] {
	case "create":
		return CreateIntent()
	case "list":
		return ListIntents()
	case "show":
		return IntentShow()
	case "delete":
		return IntentDelete()
	}

	return nil
}

func main() {
	var err error
	switch os.Args[1] {
	case "intent":
		err = IntentCmd()
	}

	if err != nil {
		fmt.Fprintf(os.Stderr, "command failed %s", err)
	}
}
