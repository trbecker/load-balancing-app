# `intentctl`: controls the load balancing app
`lbctl` allow the operator to create, list, view and delete the intents in the RAN.

## Usage
 ```
 intentctl <global options> <command> <options>
 ```

### Global options
  - `--uri <server uri>` Defines the server uri (default `localhost:8080`)

### Commands
   - `create`: creates a new intent. See below for the creation parameters.
   - `list`: list currently created intents.
   - `show`: shows an intent. Takes one argument `--intent <id>` where id is the intent id returned from`create` or `list`.
   - `delete`: deletes an intent. Takes one argument `--intent <id>` where id is the intent id returned from`create` or `list`.

## Creating intents
```
intentctl create [--name <name>]        \
    [--minimum-cell-offset <offset>]    \
    [--maximum-cell-offset <offset>]    \
    [--maximum-load <load>]             \
    [--minimum-throughput <throughput>] \
    [--maximum-ue-per-cell <ue number>] \
    [--maximum-association-rate <rate>]
```

- `name` set a mnemonic for the intent. 
- `minimum-cell-offset` and `maximum-cell-offset` sets the minimum and maximum offsets for Mobility Load Balancing.
- `maximum-load` sets the maximum load in a cell.
- `minimum-throughput` sets the minimum acceptable throughput for each UE.
- `maximum-ue-per-cell` sets the maximum number of UEs that can be associated to a cell.
- `maximum-association-rate` sets the maximum number of associations per second that can be accepted by a cell.