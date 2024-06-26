package main

import (
	"github.com/go-zookeeper/zk"

	"time"
	"fmt"
)

func main() {
	c, _, err := zk.Connect([]string{"127.0.0.1:22181"}, time.Second)
	if err != nil {
		panic(err)
	}

	children, stat, ch, err := c.ChildrenW("/")
	if err != nil {
		panic(err)
	}

	

	fmt.Printf("%+v %+v\n", children, stat)
	e := <-ch
	fmt.Printf("%+v\n", e)
}
