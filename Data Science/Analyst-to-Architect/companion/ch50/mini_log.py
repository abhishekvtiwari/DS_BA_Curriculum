"""Chapter 50 companion: a small append-only message log with Kafka's core ideas.
Not Kafka: no network, no replication, no broker. It exists so the ideas can be run and inspected:
topics, partitions, offsets, consumer groups, committed offsets, and at-least-once delivery.
Riverstone Supplies is fictional; every name and number is invented."""
import json, os, shutil

class MessageLog:
    def __init__(self, folder="stream_log", partitions=2, reset=False):
        self.folder, self.partitions = folder, partitions
        if reset:
            shutil.rmtree(folder, ignore_errors=True)
        os.makedirs(folder, exist_ok=True)
        os.makedirs(os.path.join(folder, "offsets"), exist_ok=True)

    def _path(self, partition):
        return os.path.join(self.folder, f"partition-{partition}.log")

    def partition_for(self, key):
        """Same rule as Kafka: a hash of the key decides the partition, so one key keeps its order."""
        return sum(key.encode()) % self.partitions

    def produce(self, key, value):
        partition = self.partition_for(key)
        with open(self._path(partition), "a") as f:
            f.write(json.dumps({"key": key, "value": value}) + "\n")
        return partition

    def end_offsets(self):
        return {p: sum(1 for _ in open(self._path(p))) if os.path.exists(self._path(p)) else 0
                for p in range(self.partitions)}

    def committed(self, group):
        path = os.path.join(self.folder, "offsets", f"{group}.json")
        return json.load(open(path)) if os.path.exists(path) else {}

    def commit(self, group, offsets):
        path = os.path.join(self.folder, "offsets", f"{group}.json")
        json.dump({str(k): v for k, v in offsets.items()}, open(path, "w"))

    def consume(self, group, max_messages=None):
        """Read from each partition's committed offset. Returns (messages, new_offsets).
        Offsets are NOT committed here: the caller commits after the work succeeded (at-least-once)."""
        committed, messages, new_offsets = self.committed(group), [], {}
        for p in range(self.partitions):
            start = int(committed.get(str(p), 0))
            lines = open(self._path(p)).read().splitlines() if os.path.exists(self._path(p)) else []
            taken = lines[start:] if max_messages is None else lines[start:start + max_messages]
            for i, line in enumerate(taken):
                record = json.loads(line)
                messages.append({"partition": p, "offset": start + i, **record})
            new_offsets[p] = start + len(taken)
        return messages, new_offsets
