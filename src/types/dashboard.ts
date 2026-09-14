export type Severity='normal'|'attention'|'warning'|'critical'|'offline'|'syncing'
export interface Store{ id:string; name:string; city:string; status:Severity }
export interface ZoneMetric{ id:string;name:string;occupancy:number;dwell:string;trend:number;alerts:number;status:Severity;cameras:number;grid:string }
export interface Shelf{ id:string;zone:string;product:string;category:string;availability:number;status:Severity;oos:string;confidence:number;recommendation:string }
export interface Queue{ id:string;status:'Open'|'Closed';length:number;wait:number;arrival:number;service:number;predicted:number;predictionTime:string;risk:Severity;recommendation:string }
export interface Alert{ id:string;type:string;title:string;location:string;time:string;severity:Severity;status:'New'|'Acknowledged' }
export type ActionStatus='Recommended'|'Assigned'|'Accepted'|'In Progress'|'Completed'|'Dismissed'
export interface ActionTask{ id:string;title:string;priority:Severity;source:string;employee:string;zone:string;created:string;due:string;status:ActionStatus }
export interface Camera{ id:string;zone:string;online:boolean;stream:string;visibility:number;confidence:number;issue?:string }
