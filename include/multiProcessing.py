from multiprocessing import Manager, Pool, Value, cpu_count
from multiprocessing.pool import ThreadPool, AsyncResult
from typing import Any, Iterator
from datetime import datetime

import logging
import time
import sys


class ParallelProcessing:
  """
  Parallel processing.

  References
  ----------
  [1] Class `ParallelProcessing`: https://stackoverflow.com/a/70464369/16109419

  Examples
  --------
  >>> class MyParallelProcessing(ParallelProcessing):
  >>>     def process(self, name: str) -> None:
  >>>         print(f"Executing process: {name}...")
  >>>         time.sleep(5)
  >>>
  >>>
  >>> params_list = [("A",), ("B",), ("C",), ("D",), ("E",), ("F",)]
  >>> mpp = MyParallelProcessing()
  >>> mpp.run(args_list=params_list)
  """

  _n_jobs: int
  _waiting_time: int
  _queue: Value
  _results_async: list[AsyncResult]
  _results: list

  def __init__(self, n_jobs: int = -1, waiting_time: int = 1):
    """
    Instantiates a parallel processing object to execute processes in parallel.

    Parameters
    ----------
    n_jobs: int
        Number of jobs.
    waiting_time: int
        Waiting time when jobs queue is full, e.g. `_queue.value` == `_n_jobs`.
    """
    self._n_jobs = n_jobs if n_jobs >= 0 else cpu_count()
    self._waiting_time = waiting_time if waiting_time >= 0 else 60*60

  def process(self, *args) -> None:
    """
    Abstract process that must be overridden.

    Parameters
    ----------
    *args
        Parameters of the process to be executed.
    """
    raise NotImplementedError("Process not defined ('NotImplementedError' exception).")

  def _execute(self, *args) -> None:
    """
    Run the process and remove it from the process queue by decreasing the queue process counter.

    Parameters
    ----------
    *args
        Parameters of the process to be executed.
    """
    result = self.process(*args)
    self._queue.value -= 1
    return result
  
  def _call_back(self, result: Any) -> None:
    """
    Callback.

    Parameters
    ----------
    result: Any
        Result from processes.
    """
    logging.info(result)
    self._results.append(result)

  def _error_callback(self, result: Any) -> None:
    """
    Error callback.

    Parameters
    ----------
    result: Any
        Result from exceptions.
    """
    logging.error(result)
    sys.exit(1)

  def run(self, args_list: Iterator[tuple], use_multithreading: bool = False) -> list:
    """
    Run processes in parallel.

    Parameters
    ----------
    args_list: Iterator[tuple]
        List of process parameters (`*args`).
    use_multithreading: bool
        Use multithreading instead multiprocessing.
    """
    manager = Manager()
    self._queue = manager.Value('i', 0)
    lock = manager.Lock()
    pool = Pool(processes=self._n_jobs) if not use_multithreading else ThreadPool(processes=self._n_jobs)
    self._results_async = []
    self._results = []

    start_time = datetime.now()

    with lock:  # Write-protecting the processes queue shared variable.
      for args in args_list:
        while True:
          if self._queue.value < self._n_jobs:
            self._queue.value += 1

            # Running processes in parallel:
            pool.apply_async(func=self._execute,
                             args=args,
                             callback=self._call_back,
                             error_callback=self._error_callback)

            break
          else:
            logging.debug(f"Pool full ({self._n_jobs}): waiting {self._waiting_time} seconds...")
            time.sleep(self._waiting_time)

    pool.close()
    pool.join()

    exec_time = datetime.now() - start_time
    logging.info(f"Execution time: {exec_time}")
    
    return self._results
