#!/usr/env/python
# -*- coding: utf-8 -*-
'''
Script to listen on a given port for UDP packets sent by a Forza Motorsport 7
"data out" stream and write the data to a TSV file.

Copyright (c) 2018 Morten Wang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import RPi.GPIO as GPIO
import logging
import socket

import yaml
import datetime as dt

from fdp import ForzaDataPacket
from panel import carPanel

def to_str(value):
    '''
    Returns a string representation of the given value, if it's a floating
    number, format it.

    :param value: the value to format
    '''
    if isinstance(value, float):
        return('{:f}'.format(value))

    return('{}'.format(value))

def dump_stream(port, packet_format='dash'):
    '''

    :param port: listening port number
    :type port: int

    :param packet_format: the packet format sent by the game, one of either
                          'sled' or 'dash'
    :type packet_format str
    '''
                
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', port))

    logging.info('listening on port {}'.format(port))

    n_packets = 0
    
    carPanel.start(32,33)    
    
    while True:
        message, address = server_socket.recvfrom(1024)
        fdp = ForzaDataPacket(message, packet_format = packet_format)
        
        carPanel.set_speed(fdp.speed)
        carPanel.set_rpm(fdp.current_engine_rpm)
        
        if fdp.is_race_on:
            if n_packets == 0:
                logging.info('{}: in race, logging data'.format(dt.datetime.now()))
            
            n_packets += 1
            if n_packets % 60 == 0:
                logging.info('{}: logged {} packets'.format(dt.datetime.now(), n_packets))
                print("Speed: ", fdp.speed * 3.6)
                print("RPM: ", fdp.current_engine_rpm)
        else:
            if n_packets > 0:
                logging.info('{}: out of race, stopped logging data'.format(dt.datetime.now()))
            n_packets = 0
                

def main():
    import argparse

    cli_parser = argparse.ArgumentParser(
        description="script that grabs data from a Forza Motorsport and replicates the panel"
    )

    # Verbosity option
    cli_parser.add_argument('-v', '--verbose', action='store_true',
                            help='write informational output')

    cli_parser.add_argument('-p', '--packet_format', type=str, default='dash',
                            choices=['sled', 'dash', 'fh4'],
                            help='what format the packets coming from the game is, either "sled" or "dash"')

    cli_parser.add_argument('port', type=int,
                            help='port number to listen on')

    args = cli_parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    dump_stream(args.port,
                args.packet_format)

    return()

if __name__ == "__main__":
    main()
    
