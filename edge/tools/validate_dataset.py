import argparse
from pathlib import Path
def main():
 p=argparse.ArgumentParser();p.add_argument('root');p.add_argument('--classes',type=int,required=True);a=p.parse_args();errors=[];labels=list(Path(a.root).rglob('*.txt'))
 for f in labels:
  for n,line in enumerate(f.read_text().splitlines(),1):
   try:
    values=[float(x) for x in line.split()];cls=int(values[0]);assert len(values)==5 and 0<=cls<a.classes and all(0<=x<=1 for x in values[1:])
   except Exception:errors.append(f'{f}:{n}')
 print(f'labels={len(labels)} errors={len(errors)}')
 if errors:raise SystemExit('\n'.join(errors[:20]))
if __name__=='__main__':main()
