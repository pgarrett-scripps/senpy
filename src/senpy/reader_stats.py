from dataclasses import dataclass
import time


@dataclass
class ReaderStats:
    print_freq: int

    line_itr: int = 0
    _last_time: float = 0

    def add_line(self):

        if self.line_itr == 0:  # initialize
            self._last_time = time.time()

        elif self.line_itr % self.print_freq == 0:
            elapsed_time = time.time()-self._last_time
            print(f"Lines: {self.line_itr} Time: {elapsed_time} Line/Sec: {elapsed_time/self.line_itr}")
            self._last_time = time.time()

        self.line_itr += 1