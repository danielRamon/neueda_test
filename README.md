# neueda_test
Test for Neueda of my knwoledge about docker and python

## Diragram

![alt text](https://github.com/danielRamon/neueda_test/blob/main/diagram.png?raw=true)

## How it works?
### Requirements
In order to deploy the containers you need to install [docker-compose](https://docs.docker.com/compose/install/).

In order to generate a new "secret.key" for encryptaction you need to install [pip](https://pip.pypa.io/en/stable/installation/). And obviusly you ne to have installed [python](https://www.python.org/downloads/)

### I'm ready wath now?
You can test the program with the following step in the main folder of the project:
```bash
docker-compose up
```

If you want to generate a new "secret.key" for encryptaction, run the "keyGenerator.py":
```bash
python keyGenerator.py
```
and now you are ready to deploy with the new "secret.key"

### That's working!!
You can add or modify some document in JSON format inside json_file in "SENDER" container and you'll have the same in XML format in xml_file in "RECEIVER" container.

If you want to update some JSON existent just modify it or "touch" it to change the modification data. In order to update everything in one command in order to synchronize just do the folowing command in the container "SENDER":
```bash
find /home/sender/json_file -exec touch {} \;
```

This program have a smart system to recognize errors in the JSON's files format. So if you see a file inside json_file folder ("SENDER") ended on ".BadFormat" maybe you need to take a look. Remember to change the name after the modification deleting the ".BadFormat".
