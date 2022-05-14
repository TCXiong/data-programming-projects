import geopandas
import re
import netaddr
from bisect import bisect
import pandas as pd

ips = pd.read_csv("ip2location.csv")
def lookup_region(ip):
    ip = re.sub("[a-z]{1}", "0", ip)
    ip = int(netaddr.IPAddress(ip))
    idx = bisect(ips["low"], ip)
    return ips.iloc[idx-1]["region"]


class Filing:
    def __init__(self, html):
        self.dates = []
        self.addresses = []
        self.sic = None
        self.temp = []
        if re.findall(r"SIC=(.+?)&amp",html):
            self.sic = int(re.findall(r"SIC=(.+?)&amp",html)[0])
        raw = re.findall(r"\d{4}-\d{2}-\d{2}", html)
        for i in raw:
            if i[:2]=='19'or i[:2]=='20':
                self.dates.append(i)
        
        for addr_html in re.findall(r'<div class="mailer">([\s\S]+?)</div>', html):
            lines = []
            for line in re.findall(r'<span class="mailerAddress">([\s\S]+?)</span>', addr_html):
                    lines.append(line.strip())
            self.temp.append("\n".join(lines))
        
        for j in self.temp:
            if not j == '':
                self.addresses.append(j)

    def state(self):
        for i in self.addresses:
            if re.findall(r"[A-Z]{2}\s\d{5}",i):
                res = re.findall(r"[A-Z]{2}\s\d{5}",i)
                return res[0][:2]
        return None