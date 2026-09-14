import { motion,useReducedMotion } from 'framer-motion'
import type { LucideIcon } from 'lucide-react'
import { Card,Trend } from './ui'
export function KpiCard({label,value,note,trend,icon:Icon,tone='green'}:{label:string;value:string;note?:string;trend?:number;icon:LucideIcon;tone?:string}){const reduce=useReducedMotion();return <motion.div initial={reduce?false:{opacity:0,y:12}} animate={{opacity:1,y:0}}><Card className="kpi-card"><div className={`kpi-icon ${tone}`}><Icon/></div><span>{label}</span><strong>{value}</strong><footer>{trend!==undefined?<Trend value={trend}/>:<small>{note}</small>}</footer></Card></motion.div>}
