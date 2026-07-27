#!/usr/bin/env python3
import os,json,time,random,hashlib,argparse,signal,gzip,urllib.request
from pathlib import Path
from datetime import datetime,date,timedelta
from config_loader import load_config
from hardware_profile import get_hardware_profile
from benchmark_profile import get_benchmark_profile

STATE=Path('/var/lib/keepalive-v2')
PROFILE=STATE/'profile.json'
STATUS=STATE/'status.json'
DATA=STATE/'data.json'
LOG=STATE/'keepalive.log'
STOP=False
cache=[]


def log(x):
    STATE.mkdir(parents=True,exist_ok=True)
    with open(LOG,'a') as f:
        f.write(datetime.now().isoformat()+' '+x+'\n')


def seed():
    return int(hashlib.sha256(os.uname().nodename.encode()).hexdigest()[:12],16)


def profile():
    STATE.mkdir(parents=True,exist_ok=True)
    if PROFILE.exists():
        return json.loads(PROFILE.read_text())
    r=random.Random(seed())
    hw=get_hardware_profile()
    if hw['memory_class']=='large':
        cache=r.randint(512,1024)
    elif hw['memory_class']=='medium':
        cache=r.randint(256,512)
    else:
        cache=r.randint(128,256)
    p={'cpu_bias':r.uniform(.9,1.1),'memory_bias':r.uniform(.9,1.1),'network_bias':r.uniform(.7,1.3),'interval':r.uniform(.5,1.5),'cache_mb':cache}
    PROFILE.write_text(json.dumps(p,indent=2))
    return p


def cpu_percent():
    def read():
        with open('/proc/stat') as f:
            vals=list(map(int,f.readline().split()[1:]))
        return sum(vals), vals[3]+(vals[4] if len(vals)>4 else 0)
    try:
        a,b=read();time.sleep(.5);c,d=read()
        return round((1-(d-b)/max(1,c-a))*100,2)
    except:
        return 0


def mem():
    try:
        d={}
        for l in open('/proc/meminfo'):
            k,v=l.split(':',1);d[k]=int(v.split()[0])
        return round((d['MemTotal']-d['MemAvailable'])/d['MemTotal']*100,2)
    except:
        return 0


def net():
    total=0
    try:
        for l in open('/proc/net/dev').readlines()[2:]:
            _,v=l.split(':',1);a=v.split();total+=int(a[0])+int(a[8])
    except:
        pass
    return total


def cpu_job():
    d=b'x'*1024*1024
    end=time.time()+random.randint(1,3)
    while time.time()<end:
        gzip.compress(d);hashlib.sha256(d).digest()


def cache_job(n):
    global cache
    while len(cache)*8<n:
        try:cache.append(bytearray(8*1024*1024))
        except MemoryError:break


def net_job(size):
    try:
        with urllib.request.urlopen(f'https://speed.cloudflare.com/__down?bytes={size}',timeout=20) as r:
            while r.read(65536):pass
    except:pass


def stop(*_):
    global STOP;STOP=True

signal.signal(signal.SIGTERM,stop)
signal.signal(signal.SIGINT,stop)


def main():
    cfg=load_config();p=profile();bench=get_benchmark_profile();r=random.Random(seed())
    a=argparse.ArgumentParser();a.add_argument('--status',action='store_true');args=a.parse_args()
    if args.status:
        print(json.dumps(json.loads(STATUS.read_text()) if STATUS.exists() else {'profile':p,'hardware':bench},indent=2));return
    start=net();cycle=date.today();log('started')
    while not STOP:
        if date.today()>=cycle+timedelta(days=cfg.get('cycle_days',7)):
            cycle=date.today();start=net()
        cpu=cpu_percent();m=mem()
        if cpu < cfg.get('cpu_target',20)*p['cpu_bias']:cpu_job()
        if m < cfg.get('memory_target',25)*p['memory_bias']:cache_job(p['cache_mb'])
        if cfg.get('network_test') and r.random()<0.15:net_job(r.randint(512,3072)*1024)
        s={'profile':p,'hardware':bench['hardware'],'benchmark':bench,'config':cfg,'cpu':cpu,'memory':m,'cache_mb':len(cache)*8,'network_gb':round((net()-start)/1024**3,3),'cycle':str(cycle),'updated':datetime.now().isoformat()}
        STATUS.write_text(json.dumps(s,indent=2));DATA.write_text(json.dumps(s,indent=2))
        time.sleep(r.randint(20,60)*p['interval'])
    log('stopped')

if __name__=='__main__':main()
