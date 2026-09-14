import { api } from './client';const store='/stores/store-hyd'
export const storeApi={list:()=>api('/stores'),overview:()=>api(`${store}/overview`),zones:()=>api(`${store}/zones`),activity:()=>api(`${store}/activity`)}
export const shelfApi={list:(q='')=>api(`${store}/shelves${q}`),get:(id:string)=>api(`/shelves/${id}`)}
export const queueApi={list:()=>api(`${store}/queues`)}
export const actionApi={list:()=>api(`${store}/actions`),accept:(id:string)=>api(`/actions/${id}/accept`,{method:'POST'}),start:(id:string)=>api(`/actions/${id}/start`,{method:'POST'}),complete:(id:string,note:string)=>api(`/actions/${id}/complete`,{method:'POST',body:JSON.stringify({resolution_note:note})})}
export const alertApi={list:()=>api(`${store}/alerts`),acknowledge:(id:string)=>api(`/alerts/${id}/acknowledge`,{method:'POST'}),dismiss:(id:string)=>api(`/alerts/${id}/dismiss`,{method:'POST'})}
export const analyticsApi={get:()=>api(`${store}/shopper-analytics`)}
export const edgeApi={health:()=>api(`${store}/edge-health`),connectivity:(online:boolean)=>api('/demo/connectivity',{method:'POST',body:JSON.stringify({online})})}
export const demoApi={start:()=>api('/demo/start',{method:'POST'}),stop:()=>api('/demo/stop',{method:'POST'}),reset:()=>api('/demo/reset',{method:'POST'})}
