#!/usr/bin/env python3
import os,json,time,random,hashlib,argparse,signal,gzip
from pathlib import Path

STATE=Path('/var/lib/keepalive-v2')
PROFILE=STATE/'profile.json'
STATUS=STATE/'status.json'
STOP=False


def seed():
    host=os.uname().nodename
    return int(hashlib.sha256(host.encode()).hexdigest()[:12],16)


def load_profile():
    STATE.mkdir(parents=True,exist_ok=True)
    if PROFILE.exists():
        return json.loads(PROFILE.read_text())
    r=random.Random(seed())
    p={
        'cpu_bias':r.uniform(0.9,1.1),
        'memory_bias':r.uniform(0.9,1.1),
        'network_bias':r.uniform(0.7,1.3),
        'interval':r.uniform(0.5,1.5),
        'style':r.choice(['light','balanced','active'])
    }
    PROFILE.write_text(json.dumps(p,indent=2))
    return p


def cpu_load():
    data=os.getloadavg()[0]
    cores=os.cpu_count() or 1
    return min(100,data/cores*100)


def memory_load():
    try:
        info={}
        for line in open('/proc/meminfo'):
            k,v=line.split(':',1)
            info[k]=int(v.split()[0])
        return (info['MemTotal']-info.get('MemAvailable',0))/info['MemTotal']*100
    except:
        return 0


def cpu_task(seconds=1):
    end=time.time()+seconds
    data=b'x'*1024*1024
    while time.time()<end:
        gzip.compress(data)
        hashlib.sha256(data).digest()


def handle(*_):
    global STOP
    STOP=True

signal.signal(signal.SIGTERM,handle)
signal.signal(signal.SIGINT,handle)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--status',action='store_true')
    args=ap.parse_args()
    p=load_profile()

    if args.status:
        print(json.dumps(p,indent=2))
        return

    rng=random.Random(seed())
    while not STOP:
        cpu=cpu_load()
        mem=memory_load()

        if cpu < 20*p['cpu_bias']:
            cpu_task(rng.randint(1,3))

        STATUS.write_text(json.dumps({
            'profile':p,
            'cpu':round(cpu,2),
            'memory':round(mem,2),
            'time':time.time()
        },indent=2))

        time.sleep(rng.randint(20,60)*p['interval'])

if __name__=='__main__':
    main()
