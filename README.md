# neueda_test
Test for Neueda of my docker/python knwoledge.

## Diragram

![alt text](https://github.com/danielRamon/neueda_test/blob/main/diagram.png?raw=true)

## How it works?
### Requirements
In order to deploy the containers you need to install [docker-compose](https://docs.docker.com/compose/install/).

In order to generate a new "secret.key" for encryptaction you need to install [pip](https://pip.pypa.io/en/stable/installation/). And obviusly you need to have installed [python](https://www.python.org/downloads/)

### I'm ready, what now?
You can test the program with the following step in the main folder of the project:
```bash
docker-compose up
```

If you want to generate a new "secret.key" for encryptation, run the "keyGenerator.py":
```bash
python keyGenerator.py
```
and now you are ready to deploy with the new "secret.key"

### That's working!!
You can add or modify any document in JSON format inside the "json_file" folder in the "SENDER" container and you'll have the same data in XML format in the "xml_file" folder in the "RECEIVER" container.

If you want to update any existing JSON file just modify it or "touch" it to change the modification date. To update everything with just one command, for example in order to synchronize, type the following command in the container "SENDER":
```bash
find /home/sender/json_file -exec touch {} \;
```

This program has a smart system to recognize errors in the JSON files format, so if you see a file inside the "json_file" folder ("SENDER") ended on ".BadFormat" maybe you need to take a look on it. Remember to change the name after the modification, deleting the ".BadFormat".
