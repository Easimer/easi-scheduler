import time

# Timer
# Stores the interval, the function and its arguments.
class Timer:
    _start = None # secs since epoch since the has been timer started
    _timeout = None # secs, after start should be reseted
    _function = None # function to call at timeout
    _args = None # tuple of args to be passed to the timeout function

    # Constructor
    # timeout: the number of seconds that elapses before the function is run
    # function: the function to be called
    #     Note: the function will only have one argument, a tuple of arguments
    # args: optional arguments that will be passed to the function
    def __init__(self, timeout, function, *args):
        self._function = function
        self._timeout = timeout
        self._start = time.time()
        self._args = args
    
    # Resets the time of last reset
    def reset(self):
        self._start = time.time()

    # Calls the function if enough time has elapsed
    def check(self):
        if time.time() - self._start >= self._timeout:
            self._function(self._args)
            self.reset()

    # Sets the timeout
    def set_timeout(self, timeout):
        self._timeout = timeout

# Scheduler
# Stores the timers and checks if they should be run
class Scheduler:
    _timers = []
    _interval = None # secs
    # Constructor
    # timers: a list of Timer objects
    # interval: the Scheduler checks the Timer objects every `interval` seconds
    def __init__(self, timers, interval = 1):
        self._interval = interval
        if not timers or len(timers) == 0:
            return
        for timer in timers:
            if not isinstance(timer, Timer):
                print("Scheduler: object is not Timer: %s" % timer)
                continue
            timer.reset()
            self._timers.append(timer)
    
    # Adds another timer
    def add_timer(self, timer):
        self._timers.append(timer)

    # Runs the Timer checking loop
    # Note: this function blocks
    def run(self):
        try:
            while True:
                for timer in self._timers:
                    timer.check()
                time.sleep(self._interval)
        except KeyboardInterrupt:
            return
