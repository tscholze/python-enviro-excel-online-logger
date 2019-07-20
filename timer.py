from threading import Timer


class RepeatingTimer(object):
    """
    Timer with recurring / repeating event raising.

    Source is based on:
        https://gist.github.com/alexbw/1187132
    """

    def __init__(self, function, interval, *args, **kwargs):
        super(RepeatingTimer, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.function = function
        self.interval = interval

    def start(self):
        """
        Starts the timer.
        """
        self.callback()

    def stop(self):
        """
        Stops the timer.
        """
        self.interval = False

    def callback(self):
        """
        Callback for every tick of the timer.
        """
        if self.interval:
            self.function(*self.args, **self.kwargs)
            Timer(self.interval, self.callback, ).start()
