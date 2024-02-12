package main

import (
	"fmt"
	"github.com/aws/aws-lambda-go/lambda"
)

func main() {
	
	lambda.Start(Handler)
}

// Handler is executed after warm up to decrypt the file in the S3 event, and write it to the configured S3 destination file.
func Handler(event string) (Event, error) { 
	
	fmt.Println("hola gophers!")
	
	return Event{
		Body: "success",
		StatusCode: 200,
	}, nil
}

type Event struct {
	StatusCode int `json:"statusCode,omitempty"`
	Body string `json:"body,omitempty"`
}