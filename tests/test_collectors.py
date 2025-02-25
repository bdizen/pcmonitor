import time
from dataclasses import asdict
from pprint import pprint


def test_collector(collector, interval=1):
    collector.start()

    try:
        while True:
            metrics = collector.get_metrics()
            if metrics:
                pprint(asdict(metrics))
            time.sleep(interval)
    except KeyboardInterrupt:
        collector.stop()
        print("\nStopped metric collection")
