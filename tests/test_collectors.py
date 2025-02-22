from pprint import pprint
from dataclasses import asdict
import time

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