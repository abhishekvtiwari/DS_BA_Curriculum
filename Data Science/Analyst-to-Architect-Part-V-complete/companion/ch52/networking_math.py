"""Chapter 52 companion: real CIDR and subnetting arithmetic for Riverstone's cloud network.
Riverstone Supplies is fictional; every name and number is invented."""
import ipaddress

def describe(cidr):
    net = ipaddress.ip_network(cidr)
    return {
        "cidr": cidr,
        "total_addresses": net.num_addresses,
        "usable_hosts": net.num_addresses - 5,   # cloud providers reserve 5 addresses per subnet (AWS convention)
        "first_address": str(net.network_address),
        "last_address": str(net.broadcast_address),
    }

if __name__ == "__main__":
    vpc = ipaddress.ip_network("10.0.0.0/16")
    print(f"VPC {vpc}: {vpc.num_addresses:,} total addresses")

    subnets = list(vpc.subnets(new_prefix=24))
    print(f"split into /24 subnets: {len(subnets)} subnets of {subnets[0].num_addresses} addresses each")

    plan = {
        "public-a (load balancer, Mumbai AZ-a)": subnets[0],
        "public-b (load balancer, Mumbai AZ-b)": subnets[1],
        "private-a (pipeline, database, AZ-a)": subnets[2],
        "private-b (pipeline, database, AZ-b)": subnets[3],
    }
    for name, subnet in plan.items():
        d = describe(str(subnet))
        print(f"  {name:<40} {d['cidr']:<12} usable hosts: {d['usable_hosts']}")

    remaining = len(subnets) - len(plan)
    print(f"\nsubnets allocated: {len(plan)}, remaining for future use: {remaining}")
