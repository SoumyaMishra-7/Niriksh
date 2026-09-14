import argparse,asyncio,logging,os,threading
from niriksh_edge.config import CameraConfig
from niriksh_edge.detectors import NullDetector,YoloDetector,ContourProductDetector
from niriksh_edge.events import NirikshEventClient
from niriksh_edge.runtime.pipeline import EdgePipeline
def main():
    p=argparse.ArgumentParser(description='Niriksh local-only edge vision pipeline');p.add_argument('--config',default='configs/shelf_demo.yaml');p.add_argument('--source');p.add_argument('--model');p.add_argument('--visualize',action='store_true');args=p.parse_args();logging.basicConfig(level=os.getenv('NIRIKSH_LOG_LEVEL','INFO'),format='%(asctime)s %(levelname)s %(name)s %(message)s')
    config=CameraConfig.load(args.config)
    if args.source:config.source=int(args.source) if args.source.isdigit() else args.source
    detector=YoloDetector(args.model,config.raw.get('detection',{}).get('min_confidence',.45),[0] if config.role in ('entrance','checkout','general_zone') else None) if args.model else ContourProductDetector() if config.role=='shelf' else NullDetector();client=NirikshEventClient(os.getenv('NIRIKSH_BACKEND_URL','http://localhost:8000'),token=os.getenv('NIRIKSH_EDGE_TOKEN'));loop=asyncio.new_event_loop();threading.Thread(target=lambda:(asyncio.set_event_loop(loop),loop.run_until_complete(client.run())),daemon=True).start()
    try:EdgePipeline(config,detector,client).run(args.visualize)
    finally:client.stop()
if __name__=='__main__':main()
