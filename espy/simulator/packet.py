class Packet(object):
    def __init__(self, sender, dest, msg):
        self.sender = sender
        self.dest = dest
        self.msg = msg
