from netaddr import IPNetwork


def convert(network, netmask):
    entry = IPNetwork(f"{network}/{netmask}")
    answer = {}
    answer["slashbits"] = f"/{getattr(entry, 'prefixlen')}"
    answer["bits"] = getattr(entry, "prefixlen")
    answer["hostmask"] = str(entry.hostmask)
    answer["netmask"] = str(entry.netmask)
    answer["network"] = network
    answer["net_netmask"] = f"{network}/{answer['netmask']}"
    answer["net_bits"] = f"{network}/{answer['bits']}"
    answer["net_hostmask"] = f"{network}/{answer['hostmask']}"
    return answer


class FilterModule:  # pylint: disable=too-few-public-methods
    def filters(self):
        return {"convert": convert}
