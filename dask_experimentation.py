import logging

import numpy as np
from dask.distributed import Client, LocalCluster, fire_and_forget

def array_summation():
    dim_size = int(9e3)
    x = np.random.random(size=(dim_size, dim_size, dim_size))
    y = np.random.random(size=(dim_size, dim_size, dim_size))
    z = (np.arcsin(x) + np.arccos(y)).sum(axis=(1,))
    return z


def large_summation():
    some_list = []
    for i in range(int(1e5)):
        print(sum(some_list))
        some_list.append(i)


def compute(client):
    print(client)
    # results_futures = [fire_and_forget(client.submit(array_summation)) for i in range(5)]
    results_futures = [fire_and_forget(client.submit(large_summation)) for i in range(5)]
    # results = results_future.result()
    # print(i, results_future.done())


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    hosts = [
        # "tcp://scheduler",
        # "tcp://dask-scheduler",
        "tcp://localhost",
        ]
    for host_ in hosts:
        print(f"Dask cluster: {host_}")
        try:
            # cluster = LocalCluster(n_workers=5, memory_limit="16GB", host=host_, scheduler_port=8786, dashboard_address=None)
            # client = Client(cluster)
            client = Client(address=f"{host_}:8786")
            # cluster = client.cluster
        except Exception as err:
            print(err)
        else:
            # cluster.adapt(minimum=5, maximum=10, maximum_memory="16GB")
            # print(f"{cluster=}")
            print(f"{client=}")
            compute(client=client)
            break
