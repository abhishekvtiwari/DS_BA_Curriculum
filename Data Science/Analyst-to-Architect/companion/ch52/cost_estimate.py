"""Chapter 52 companion: a worked monthly cost estimate for running the Riverstone pipeline
in the cloud, extending Chapter 49's storage-only estimate to include compute.
Illustrative list prices, as of writing; always check your provider's current calculator.
Riverstone Supplies is fictional; every name and number is invented."""

HOURS_PER_MONTH = 730

def container_compute_cost(vcpu, memory_gb, hours_per_month, price_per_vcpu_hour=0.04, price_per_gb_hour=0.004):
    """A simple pay-per-second container/Fargate-style pricing model."""
    return round((vcpu * price_per_vcpu_hour + memory_gb * price_per_gb_hour) * hours_per_month, 2)

def always_on_vs_scheduled():
    always_on = container_compute_cost(vcpu=0.5, memory_gb=1, hours_per_month=HOURS_PER_MONTH)
    scheduled_hours = 1 * 30            # the pipeline runs for about an hour a day
    scheduled = container_compute_cost(vcpu=0.5, memory_gb=1, hours_per_month=scheduled_hours)
    return always_on, scheduled

if __name__ == "__main__":
    always_on, scheduled = always_on_vs_scheduled()
    print(f"pipeline container, always on ({HOURS_PER_MONTH} h/month): ${always_on}/month")
    print(f"same container, scheduled (~1 h/day, 30 h/month):      ${scheduled}/month")
    print(f"ratio: {round(always_on / scheduled, 1)}x more expensive to run it always on")

    storage_month = 277 * 0.023          # Chapter 49's sensor-archive figure: 277 GB at $0.023/GB-month
    print(f"\nstorage (from Chapter 49): ${round(storage_month, 2)}/month")
    print(f"compute (scheduled pipeline): ${scheduled}/month")
    total = round(storage_month + scheduled, 2)
    print(f"total estimate: ${total}/month")
