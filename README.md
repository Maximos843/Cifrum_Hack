# Solution of Cifrum Hack


### Problem statement
We tackled the task of multiclass categorization - determining the tone of texts. The texts were reviews of various services, and the target categories were: negative; neutral; positive. 


### Problem solving
After conducting experiments, we decided to take the BERT model pre-trained on Russian texts from DeepPavlov and finetune it for our reviews. 
Also, all reviews were preprocessed using regular expressions.
The service itself has both a web interface and a regular api with predictions by batch and by one object.
FastAPI was used to write the web service.

The model is stored on a remote service, which is connected to using boto3.
The service also uses a database, which is stored in remote storage, and the connection to it works using supabase. It is needed to store the history of queries to draw conclusions based on historical data and to see interpretations of model responses to correct negative aspects of the product. Moreover, the database is also used to cache queries so that time is not wasted on identical queries.
Tests were written for the model operation and tests for the api and web service functions.


### [Link to our service](http://a0st-ahl7-308g.gw-1a.dockhost.net/)

### Makefile commands
Maintain the service development mode with automatic updates when changes are made
```
make dev
```

Building an application
```
make build
```

Run an application
```
make run
```

Running tests
```
make test
```
