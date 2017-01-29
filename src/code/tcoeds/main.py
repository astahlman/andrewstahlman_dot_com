#!/usr/bin/python2.7
from random import randint
import logging

class LogicalClock(object):

    def __init__(self):
        self.time = 0

    def increment(self):
        self.time += 1

    def ensure_at_least(self, t):
        self.time = max(self.time, t)

class Mutex(object):

    def __init__(self):
        self._owner = None
        self.num_claims = 0
        self.num_releases = 0

    def owner(self):
        return self._owner

    def claim(self, new_owner):
        assert self._owner is None, "Aaaaaaaaaaaagh. {} tried to claim the lock, but {} owns it.".format(new_owner, self._owner)
        logging.debug("{} claims the lock.".format(new_owner))
        self._owner = new_owner
        self.num_claims += 1
        assert self.num_claims == self.num_releases + 1

    def release(self, owner):
        assert self._owner is owner, "{} tried to release a lock that {} owns.".format(owner, self._owner)
        logging.debug("{} releases the lock.".format(owner))
        self._owner = None
        self.num_releases += 1
        assert self.num_claims == self.num_releases

class Message(object):

    def __init__(self, sender, recipient, sent_at):
        self.sender = sender
        self.recipient = recipient
        self.sent_at = sent_at

    def __repr__(self):
        return "{}@{} -> {}: {}".format(self.sender.name, self.sent_at, self.recipient.name, self.content)

    @classmethod
    def a_mutex_request(cls, sender, recipient, sent_at):
        m = Message(sender, recipient, sent_at)
        m.content = "REQUEST"
        return m

    @classmethod
    def a_mutex_release(cls, sender, recipient, sent_at):
        m = Message(sender, recipient, sent_at)
        m.content = "RELEASE"
        return m

    @classmethod
    def an_ack(cls, sender, recipient, sent_at):
        m = Message(sender, recipient, sent_at)
        m.content = "ACK"
        return m

class MsgBroker(object):

    def __init__(self):
        self.queue = {}

    def send_message(self, sender, recipient, msg):
        queue_key = (sender, recipient)
        outbox = self.queue.get(queue_key, [])
        self.queue[queue_key] = outbox
        outbox.append(msg)

    def deliver(self):
        for (sender, recipient), outbox in self.queue.items():
            while outbox and randint(1, 20) == 1:
                msg = outbox.pop(0)
                logging.debug("[MSG]: {}".format(msg))
                recipient.receive_message(sender, msg)

    def __str__(self):
        pending_msgs = 0
        for (sender, recipient), outbox in self.queue.items():
            pending_msgs += (len(outbox) if outbox else 0)
        return 'Messages pending delivery: {}'.format(pending_msgs)

class Process(object):

    def __init__(self, name, the_lock, msg_broker, num_peers):
        self.name = name
        self.the_lock = the_lock
        self.msg_broker = msg_broker
        self.num_peers = num_peers

        self.clock = LogicalClock()
        self.request_queue = []
        self.latest_ack_from = {}

    def __str__(self):
        return "{name}@{time}".format(name=self.name, time=self.time())

    def request_lock(self, peers):
        for p in peers:
            msg = Message.a_mutex_request(self, p, self.time())
            self.send_message(p, msg)

        self.request_queue.append(Message.a_mutex_request(self, self, self.time()))
        self.clock.increment()

    def wants_lock(self):
        return not self.has_request_pending() and randint(1, 10) == 1

    def has_request_pending(self):
        return any(x for x in self.request_queue if x.sender is self)

    def release_lock(self, peers):
        assert self.the_lock.owner() is self, "Tried to release a lock we don't own!"
        req = self.request_queue.pop(0)
        assert req.sender is self, "We somehow claimed the lock without being at the front of the queue!"
        self.the_lock.release(self)
        for p in peers:
            self.send_message(p, Message.a_mutex_release(self, p, self.time()))
        self.clock.increment()

    def ready_to_release(self):
        return randint(1, 2)

    def receive_message(self, sender, msg):
        self.clock.ensure_at_least(msg.sent_at + 1)

        if msg.content == "REQUEST":
            self.request_queue.append(msg)
            self.send_message(sender, Message.an_ack(self, sender, self.time()))

        elif msg.content == "RELEASE":
            logging.debug("{} processing release by {}. Before removing:".format(self, sender))
            logging.debug(str(self.request_queue))
            self.request_queue.pop(0)
            logging.debug("After: {}:".format(self.request_queue))

        elif msg.content == "ACK":
            self.latest_ack_from[sender.name] = msg.sent_at

        if msg.content in ["ACK", "RELEASE"] and self.can_claim_lock():
                self.the_lock.claim(self)

    def can_claim_lock(self):
        first_req = self.get_request_queue()[0]
        if first_req.sender is self:
            acks = [sender for (sender, t) in self.latest_ack_from.iteritems()
                        if t > first_req.sent_at]
            return len(acks) == self.num_peers

    @classmethod
    def total_ordering(cls, msg):
        return (msg.sent_at, msg.sender.name)

    def get_request_queue(self):
        self.request_queue.sort(key=Process.total_ordering)
        return self.request_queue

    def send_message(self, recipient, msg):
        self.msg_broker.send_message(self, recipient, msg)

    def time(self):
        return self.clock.time

import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser('Simulate Processes coordinating mutual exclusion.')
    parser.add_argument(
        '-v', '--verbose',
        help='print every message exchanged between processes',
        action='store_true')
    args = parser.parse_args()
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level)

    the_lock = Mutex()
    msg_broker = MsgBroker()

    num_processes = 10

    a = Process("Andromeda", the_lock, msg_broker, num_processes - 1)
    b = Process("Bonesaw", the_lock, msg_broker, num_processes - 1)
    c = Process("Charybda", the_lock, msg_broker, num_processes - 1)
    d = Process("Doofus", the_lock, msg_broker, num_processes - 1)
    e = Process("Egbertina", the_lock, msg_broker, num_processes - 1)
    f = Process("Fido", the_lock, msg_broker, num_processes - 1)
    g = Process("Gary", the_lock, msg_broker, num_processes - 1)
    h = Process("Hufflepuff", the_lock, msg_broker, num_processes - 1)
    i = Process("Iola", the_lock, msg_broker, num_processes - 1)
    j = Process("Jethro", the_lock, msg_broker, num_processes - 1)

    processes = [a, b, c, d, e, f, g, h, i, j]
    assert len(processes) == num_processes

    SIMULATION_NUM_CYCLES = 10000

    logging.info("Starting simulation with {} processes.".format(len(processes)))
    for t in range(1, SIMULATION_NUM_CYCLES):
        for p in processes:
            peers = [x for x in processes if not x is p]
            if p.wants_lock():
                p.request_lock(peers)
            if p == the_lock.owner() and p.ready_to_release():
                p.release_lock(peers)

        msg_broker.deliver()

    logging.info("The lock was claimed {} times and released {} times"
                 .format(the_lock.num_claims, the_lock.num_releases))
    logging.info("MsgBroker: {}".format(msg_broker))
