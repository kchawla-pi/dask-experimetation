import asyncio
import json
import logging
import time
from pathlib import Path

import numpy as np
from dask.distributed import Client, LocalCluster, fire_and_forget
from distributed import Future

logger = logging.getLogger(__name__)

def array_summation(count: int):
    time.sleep(10)
    dim_size = int(1e2)
    x = np.random.random(size=(dim_size, dim_size, dim_size))
    y = np.random.random(size=(dim_size, dim_size, dim_size))
    z = (np.arcsin(x) + np.arccos(y)).sum(axis=(1,))
    Path(f"array_summation-{count}.txt").write_text(json.dumps(z.tolist()))
    return z

def large_summation(count: int):
    time.sleep(10)
    some_list = []
    for i in range(int(1e5)):
        # print(sum(some_list))
        some_list.append(i)
    Path(f"large_summation-{count}.txt").write_text(json.dumps(some_list))


def compute(client, fn):
    print(client)
    # results_futures = [fire_and_forget(client.submit(array_summation)) for i in range(5)]
    results_futures: list[Future] = [fire_and_forget(client.submit(fn, i)) for i in range(5)]
    # results = results_future.result()
    # print(i, results_future.done())
    return results_futures


def main():
    [file_.unlink() for file_ in Path(".").rglob("large_summation*")]
    [file_.unlink() for file_ in Path(".").rglob("array_summation*")]

    # results_futures = []
    hosts = [
        "tcp://scheduler",
        # "tcp://dask-scheduler",
        # "tcp://localhost",
        ]
    # schedular_running = True
    # while schedular_running:
    for host_ in hosts:
        print(f"Dask cluster: {host_}")
        try:
            client = Client(address=f"{host_}:6878")
            cluster = client.cluster
            logger.debug(f"{cluster=}")
        except RuntimeError as err:
            print(err)
        else:
            results_futures_large_summation = compute(client=client, fn=large_summation)
            results_futures_array_summation = compute(client=client, fn=array_summation)
            break
    # time.sleep(30)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
