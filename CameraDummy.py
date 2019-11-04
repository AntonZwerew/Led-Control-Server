class Camera:

    def __init__(self):
        self.LED = self.LED()

    class LED:
        def __init__(self):
            self.state = None
            self.color = None
            self.rate = None

