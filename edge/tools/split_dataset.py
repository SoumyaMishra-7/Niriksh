import argparse,random,shutil
from pathlib import Path
def main():
 p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('output');p.add_argument('--val',type=float,default=.2);p.add_argument('--seed',type=int,default=42);a=p.parse_args();random.seed(a.seed);src=Path(a.source);items=list(src.glob('*.jpg'))+list(src.glob('*.png'));random.shuffle(items);cut=int(len(items)*(1-a.val))
 for split,files in [('train',items[:cut]),('val',items[cut:])]:
  for image in files:
   dest=Path(a.output)/'images'/split;dest.mkdir(parents=True,exist_ok=True);shutil.copy2(image,dest/image.name);label=src/image.with_suffix('.txt').name
   if label.exists():ld=Path(a.output)/'labels'/split;ld.mkdir(parents=True,exist_ok=True);shutil.copy2(label,ld/label.name)
 print(f'train={cut} val={len(items)-cut}')
if __name__=='__main__':main()
