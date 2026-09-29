"""Chapter 50 companion: a small append-only message log with Kafka's core ideas.

Not Kafka: no network, no replication, no broker. It exists so the ideas can be run and inspected:
topics, partitions, keys, offsets, consumer groups, committed offsets, and at-least-once delivery.
Everything lives in one folder:
    partition-0.log, partition-1.log   one line per message, in the order they arrived
    offsets/<group>.json               each group's committed offsets
A committed offset is the position of the NEXT message the group will read, per partition.
Riverstone Supplies is fictional; every name and number is invented."""
import json, os, shutil


class MessageLog:
    def __init__(self, folder="stream_log", partitions=2, reset=False):
        """Open (or create) a log in `folder`. reset=True deletes whatever was there first."""
        self.folder, self.partitions = folder, partitions
        if reset:
            shutil.rmtree(folder, ignore_errors=True)
        os.makedirs(os.path.join(folder, "offsets"), exist_ok=True)

    def _path(self, partition):
        return os.path.join(self.folder, f"partition-{partition}.log")

    def partition_for(self, key):
        """A hash of the key decides the partition, so one key always lands in the same one.
        Here the hash is the sum of the key's bytes; Kafka uses a stronger hash (murmur2),
        so the same key can land in a different partition there, but the rule is the same."""
        return sum(key.encode()) % self.partitions

    def produce(self, key, value):
        """Append one message to the end of its key's partition; return the partition number."""
        partition = self.partition_for(key)
        with open(self._path(partition), "a") as f:
            f.write(json.dumps({"key": key, "value": value}) + "\n")
        return partition

    def end_offsets(self):
        """{partition: number of messages in it}, which is also the offset the next message gets."""
        ends = {}
        for p in range(self.partitions):
            if os.path.exists(self._path(p)):
                with open(self._path(p)) as f:
                    ends[p] = sum(1 for _ in f)
            else:
                ends[p] = 0
        return ends

    def committed(self, group):
        """{partition: committed offset} for a group, or {} if it has never committed."""
        path = os.path.join(self.folder, "offsets", f"{group}.json")
        if not os.path.exists(path):
            return {}
        with open(path) as f:
            return {int(p): offset for p, offset in json.load(f).items()}   # JSON keys are text

    def commit(self, group, offsets):
        """Store the group's offsets: 'everything before these has been handled'."""
        path = os.path.join(self.folder, "offsets", f"{group}.json")
        with open(path, "w") as f:
            json.dump(offsets, f)

    def consume(self, group):
        """Read every message after the group's committed offsets. Returns (messages, new_offsets).
        Each message is {"partition", "offset", "key", "value"}. Offsets are NOT committed here:
        the caller commits after its work has succeeded (at-least-once)."""
        committed, messages, new_offsets = self.committed(group), [], {}
        for p in range(self.partitions):
            start = committed.get(p, 0)
            lines = []
            if os.path.exists(self._path(p)):
                with open(self._path(p)) as f:
                    lines = f.read().splitlines()
            for i, line in enumerate(lines[start:]):
                messages.append({"partition": p, "offset": start + i, **json.loads(line)})
            new_offsets[p] = len(lines)
        return messages, new_offsets
