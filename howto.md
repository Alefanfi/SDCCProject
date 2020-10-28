# SDCCProject
![parking now logo](https://github.com/Alefanfi/SDCCProject/blob/master/ClientWindows/gui/logo.png?raw=true)

## Requirements
This project uses docker and docker-compose to simulate the fog nodes locally.

Please refer to this links:
* [docker download](https://www.docker.com/products/docker-desktop)
* [docker compose download](https://docs.docker.com/compose/install/)

## Fog nodes
To create the fog nodes you need to run the following command from the terminal:
    
    docker-compose up --scale fognode=3

This will create both the proxy server, which redirects the client requests to one of the nodes, and the fog cluster.

You can to specify the number of instances of fognode you wish to create using the "--scale" option (in the above example we
used 3). 

All information on the options can be found in the [docker-compose up](https://docs.docker.com/compose/reference/up/) manual.

#### Sensors
To simulate the sensors you can use the code provided in sensor.py.
 
Just run the following commands:

    cd Sensors
    
    python sensor.py
    
## Client
There are two client applications respectively for:
* Windows
* Mac

To use it just cd into the directory of your choice and run:
    
    python client.py

The gui shows if the parking spots are currently empty ![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+) or not ![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) . 

To see the statistics just push the "show statistics" button.

## Server 
If you wish to run your own server side application you will need to change the config.json file in the FogNode directory specifying the new ip and port.

The application makes use of the [AWS s3](https://aws.amazon.com/it/s3/) service to implement a persistent storage.
In the CentralNode directory you can find a configuration file, config.json, in which you can specify
the name of your bucket and all the credentials to access the service.

To run the server from terminal use:

    cd CentralNode
    
    python server.py