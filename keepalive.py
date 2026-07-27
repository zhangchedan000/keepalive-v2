#!/usr/bin/env python3
import os,json,time,random,hashlib,argparse,signal
from pathlib import Path

STATE=Path('/var/lib/keepalive-v2')
PROFILE=STATE/'profile.json'
STATUS=STATE/'status.json'
STOP=False


def seed():
    return int(hashlib.sha256((os.uname().nodename+str(os.getpid())).encode()).hexdigest()[:12],16)


def profile():
    STATE.mkdir(parents=True,exist_ok=True)
    if PROFILE.exists():
        return json.loads(PROFILE.read_text())
    r=random.Random(seed())
    p={
        'cpu_bias':round(r.uniform(.9,1.1),2),
        'memory_bias':round(r.uniform(.9,1.1),2),
        'network_bias':round(r.uniform(.7,1.3),2),
        'interval':round(r.uniform(.5,1.5),2)
    }
    PROFILE.write_text(json.dumps(p,indent=2))
    return p


def handle(*_):
    global STOP
    STOP=True

signal.signal(signal.SIGTERM,handle)
signal.signal(signal.SIGINT,handle)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--status',action='store_true')
    args=ap.parse_args()
    p=profile()
    if args.status:
        print(json.dumps(p,indent=2))
        return
    while not STOP:
        STATUS.write_text(json.dumps({'profile':p,'time':time.time()},indent=2))
        time.sleep(30)

if __name__=='__main__':
    main()
