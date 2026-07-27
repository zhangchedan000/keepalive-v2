#!/usr/bin/env python3
import os,json,time,random,hashlib,argparse,signal,gzip,urllib.request
from pathlib import Path
from datetime import datetime,date

STATE=Path('/var/lib/keepalive-v2')
PROFILE=STATE/'profile.json'
STATUS=STATE/'status.json'
DATA=STATE/'data.json'
STOP=False


def seed():
    return int(hashlib.sha256(os.uname().nodename.encode()).hexdigest()[:12],16)


def load_profile():
    STATE.mkdir(parents=True,exist_ok=True)
    if PROFILE.exists():
        return json.loads(PROFILE.read_text())
    r=random.Random(seed())
    p={'cpu_bias':r.uniform(.9,1.1),'memory_bias':r.uniform(.9,1.1),'network_bias':r.uniform(.7,1.3),'interval':r.uniform(.5,1.5)}
    PROFILE.write_text(json.dumps(p,indent=2))
    return p


def net_bytes():
    total=0
    try:
        for line in open('/proc/net/dev').readlines()[2:]:
            _,v=line.split(':',1)
            x=v.split()
            total+=int(x[0])+int(x[8])
    except:
        pass
    return total


def mem_percent():
    try:
        d={}
        for l in open('/proc/meminfo'):
            k,v=l.split(':',1)
            d[k]=int(v.split()[0])
        return (d['MemTotal']-d['MemAvailable'])/d['MemTotal']*100
    except:
        return 0


def cpu_task():
    data=b'x'*1024*1024
    end=time.time()+random.randint(1,3)
    while time.time()<end:
        gzip.compress(data)
        hashlib.sha256(data).digest()


def download_task(size=1024*1024):
    try:
        url=f'https://speed.cloudflare.com/__down?bytes={size}'
        with urllib.request.urlopen(url,timeout=20) as r:
            while r.read(65536):
                pass
    except:
        pass


def stop(*_):
    global STOP
    STOP=True

signal.signal(signal.SIGTERM,stop)
signal.signal(signal.SIGINT,stop)


def main():
    p=load_profile()
    ap=argparse.ArgumentParser()
    ap.add_argument('--status',action='store_true')
    args=ap.parse_args()
    if args.status:
        print(json.dumps(json.loads(STATUS.read_text()) if STATUS.exists() else p,indent=2))
        return

    data={'start':date.today().isoformat(),'network_start':net_bytes()}
    rng=random.Random(seed())

    while not STOP:
        cpu=os.getloadavg()[0]/max(1,os.cpu_count())*100
        mem=mem_percent()

        if cpu < 20*p['cpu_bias']:
            cpu_task()

        if rng.random()<0.15:
            download_task(rng.randint(512,3072)*1024)

        status={
            'profile':p,
            'cpu':round(cpu,2),
            'memory':round(mem,2),
            'network_total_gb':round((net_bytes()-data['network_start'])/1024**3,3),
            'cycle_days':7,
            'updated':datetime.now().isoformat()
        }
        STATUS.write_text(json.dumps(status,indent=2))
        time.sleep(rng.randint(20,60)*p['interval'])

if __name__=='__main__':
    main()
