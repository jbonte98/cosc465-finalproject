import xml.etree.ElementTree as ET
from datetime import datetime

class Client:
    def __init__(self,device_type,username):
        self._device_type = device_type
        self._username = username
        self._connections = []
        self._home = ""

    def add_connection(self,connection):
        self._connections.append(connection)
        if (connection.home):
            self._home = connection.location

    @property
    def connections(self):
        return self._connections

class Connection:

    def __init__(self,location,bytes_used,start_time,end_time):
        self._location = location
        self._shortstop = (bytes_used == 0) or (end_time-start_time).seconds < 300
        #self._home = start_time > 2
        self._home = False

    @property
    def location(self):
        return self._location

    @property
    def home(self):
        return self._home

    #We will consider this the clients home if the time is after 2pm
    def is_home(self,start_time):
        return start_time > 2

    #want to log this as a short stop for better data analysis if they didn't use any bytes or were connected for less than x minutes
    def is_shortstop(self,start_time,end_time,bytes_used):
        return (bytes_used == 0) or (end_time-start_time).seconds < 300

    def __str__(self):
        return self._location + " is shortstop: "

def main():
    establish_client("client1_associations.xml")


def establish_client(filename):
    client_tree = ET.parse(filename)
    root = client_tree.getroot()[0]
    device_type = root.find("device_type").text
    username = root.find("username").text
    client = Client(device_type,username)
    for child in root:
        #Check to make sure it is a connection instance
        if (child.tag == "association"):
            #parse child
            parse_connection(client,child)
            break
    print(str(client.connections))

def parse_connection(client,instance):
    location = instance.find("ap").text
    bytes_used = instance.find("bytes_used").text
    start_time_str = instance.find("connect_time").text[:-6].strip()
    end_time_str = instance.find("disconnect_time").text[:-6].strip()
    start_time = datetime.strptime(start_time_str,'%Y-%m-%dT%H:%M:%S')
    end_time = datetime.strptime(end_time_str,'%Y-%m-%dT%H:%M:%S')
    connection = Connection(location,bytes_used,start_time,end_time)
    client.add_connection(connection)

if __name__ == '__main__':
    main()
