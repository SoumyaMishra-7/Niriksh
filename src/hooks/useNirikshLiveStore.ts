import { useEffect,useRef,useState } from 'react'
export type LiveEvent={event:string;timestamp:string;payload:Record<string,unknown>}
export function useNirikshLiveStore(storeId='store-hyd'){
 const [status,setStatus]=useState<'connecting'|'connected'|'reconnecting'|'offline'>('connecting'),[lastEvent,setLastEvent]=useState<LiveEvent|null>(null);const retry=useRef(0)
 useEffect(()=>{let active=true,ws:WebSocket|undefined,timer:number|undefined
  function connect(){if(!active)return;const base=(import.meta.env.VITE_WS_URL??'ws://localhost:8000').replace(/\/$/,'');setStatus(retry.current?'reconnecting':'connecting');ws=new WebSocket(`${base}/ws/stores/${storeId}`);ws.onopen=()=>{retry.current=0;setStatus('connected')};ws.onmessage=e=>{try{setLastEvent(JSON.parse(e.data))}catch{return}};ws.onclose=()=>{if(!active)return;setStatus('offline');timer=window.setTimeout(connect,Math.min(1000*2**retry.current++,15000))}}
  connect();return()=>{active=false;clearTimeout(timer);if(ws){ws.onclose=null;ws.close()}}
 },[storeId]);return{status,lastEvent}
}
