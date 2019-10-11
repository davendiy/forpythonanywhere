#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 10.10.2019
# by David Zashkolny
# 3 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

import threading
from queue import Queue, Empty
from collections import deque
import time
import random
import logging

logging.basicConfig(level=logging.DEBUG)

QUEUE_LENGTH = 0
WAITING_TIME = 0
QUEUE_CLIENTS_AMOUNT = 0

lock = threading.RLock()


def live(required_time, hotel: deque):
    tmp = random.random() * (required_time - 1) + 1
    time.sleep(tmp)
    logging.debug('[<-] End of living. Popping from hotel...')
    with lock:
        hotel.pop()


def client_generator(queue: Queue, generating_time, living_time, hotel, max_amount):
    global QUEUE_LENGTH
    while True:
        tmp_time = random.random() * (generating_time - 1) + 1
        time.sleep(tmp_time)
        logging.debug("[*] New client arrived.")
        if len(hotel) < max_amount:
            logging.debug("[->] Push to the hotel without queue, start of living...")
            with lock:
                hotel.append(1)
            threading.Thread(target=live, args=(living_time, hotel),
                             daemon=True).start()
        else:
            logging.debug("[*] There is no place in hotel, pushing to the queue...")
            queue.put(time.time())
            with lock:
                QUEUE_LENGTH += 1


def client_handler(queue: Queue, hotel: deque, living_time, max_amount):
    global QUEUE_LENGTH, WAITING_TIME, QUEUE_CLIENTS_AMOUNT

    while True:
        try:
            tmp_time = queue.get(timeout=1)
            t = False
            with lock:
                QUEUE_LENGTH -= 1
                if len(hotel) < max_amount:
                    hotel.append(1)
                    logging.debug("[->] Push to the hotel from the queue, start of living...")
                    t = True
                    WAITING_TIME += time.time() - tmp_time
                    QUEUE_CLIENTS_AMOUNT += 1
                else:
                    queue.put(tmp_time)
                    QUEUE_LENGTH += 1
            if t:
                threading.Thread(target=live, args=(living_time, hotel),
                                 daemon=True).start()
        except Empty:
            continue


def simulation(t1, t2, n, simulation_time):
    clients = Queue()
    hotel = deque()

    queue_length = 0
    amount = 0

    while True:
        threading.Thread(target=client_generator, args=(clients, t1, t2, hotel, n), daemon=True).start()
        threading.Thread(target=client_handler, args=(clients, hotel, t2, n), daemon=True).start()
        time.sleep(1)
        queue_length += QUEUE_LENGTH
        amount += 1
        logging.debug(f"[!Info] number of measurement: {amount}, lenght of queue: {QUEUE_LENGTH}")
        if amount > simulation_time:
            break

    return queue_length/amount


if __name__ == '__main__':
    test_t1 = float(input("t1: "))
    test_t2 = float(input("t2: "))
    n = int(input("n: "))
    sim_time = float(input("simulation time: "))
    res = simulation(test_t1, test_t2, n, sim_time)
    logging.debug(f"[*] Done... Average length of queue: {res}.")
    logging.debug(f"[*] Average waiting time: {WAITING_TIME / QUEUE_CLIENTS_AMOUNT}")
