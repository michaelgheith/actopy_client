#!/usr/bin/env python

import sys
import argparse
import json
import random
import time
import bluetooth


class myClient():
    def __init__(self):
        self.blah = None

    def connect(self, uuid):
        for n in range(0, 5):
             service_matches = bluetooth.find_service(uuid = uuid)
             if len(service_matches) == 0:
                 print "couldn't find the service so in retry %d" % (n+1)
                 sleep_time = (2**n) + random.random()
                 print "going to retry in %f seconds" % sleep_time
                 time.sleep(sleep_time)
             elif len(service_matches) > 0:
                 self.make_connection(service_matches)
                 return
             else:
                 break
        print "couldn't find the FooBar service"
        sys.exit(0)

    def make_connection(self, service_matches):
        first_match = service_matches[0]
        port = first_match["port"]
        name = first_match["name"]
        host = first_match["host"]

        print "connecting to \"%s\" on %s" % (name, host)
        sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        sock.connect((host, port))
        
        request = {"msg": "hello from cient!!"}
        sock.send(json.dumps(request))

        response = sock.recv(1024)
        print json.loads(response)

        sock.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="a bluetooth client")
    #parser.add_argument("-v", "--verbose", help="turn on verbose mode", action="store_true")
    parser.add_argument("-u", "--uuid", help="specify a uuid", default="1e0ca4ea-299d-4335-93eb-27fcfe7fa848")
    args = parser.parse_args()

    client = myClient()
    client.connect(uuid = args.uuid)
