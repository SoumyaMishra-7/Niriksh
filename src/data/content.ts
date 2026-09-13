import { Boxes, Footprints, UsersRound, PackageSearch, TimerReset, ScanLine, CloudOff, EyeOff } from 'lucide-react'
import type { Feature, Zone } from '../types'
export const navItems = [['Platform','platform'],['Intelligence','intelligence'],['Privacy','privacy'],['How It Works','how-it-works'],['About','about']] as const
export const features: Feature[] = [
 { title:'Shelf Intelligence', description:'Know what is available, what is running low, and what needs attention before shoppers find an empty shelf.', points:['Availability & low-stock detection','Stock-out prediction','Replenishment recommendations'], icon:Boxes, type:'shelf' },
 { title:'Shopper Intelligence', description:'Understand how spaces perform through anonymous, temporary signals—not customer identities.', points:['Footfall & dwell time','Anonymous zone transitions','Privacy-safe heatmaps'], icon:Footprints, type:'shopper' },
 { title:'Queue Intelligence', description:'See pressure building at checkout and give teams enough time to respond.', points:['Live queue estimation','Congestion prediction','Counter recommendations'], icon:UsersRound, type:'queue' },
]
export const zones: Zone[] = [
 {id:'entrance',name:'Entrance',shoppers:8,dwell:'0m 42s',traffic:'+14%',status:'Steady flow',grid:'entrance'},
 {id:'grocery',name:'Grocery',shoppers:19,dwell:'5m 06s',traffic:'+8%',status:'Active',grid:'grocery'},
 {id:'fashion',name:'Fashion',shoppers:7,dwell:'3m 12s',traffic:'−4%',status:'Normal',grid:'fashion'},
 {id:'electronics',name:'Electronics',shoppers:12,dwell:'4m 18s',traffic:'+23%',status:'High engagement',grid:'electronics'},
 {id:'checkout',name:'Checkout',shoppers:6,dwell:'2m 08s',traffic:'+17%',status:'Watch queue',grid:'checkout'},
]
export const impacts = [
 [PackageSearch,'Reduce Stock-Out Risk','Predict shelf depletion before products disappear.'],
 [TimerReset,'Reduce Checkout Congestion','Forecast queue growth before wait times become excessive.'],
 [ScanLine,'Improve Store Visibility','Understand traffic and dwell patterns anonymously.'],
 [CloudOff,'Lower Cloud Dependence','Process camera intelligence locally.'],
] as const
export const privacyBadges = ['No Face Recognition','No Persistent Customer Identity','No Cross-Store Tracking','No Raw Video Cloud Upload','Metadata-Only Sync']
export const privacyIcon = EyeOff
