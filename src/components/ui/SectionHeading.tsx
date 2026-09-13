import { motion } from 'framer-motion'
import { fadeUp } from '../../lib/motion'
export function SectionHeading({ eyebrow, title, copy, light=false }:{eyebrow:string;title:string;copy?:string;light?:boolean}) { return <motion.div {...fadeUp} className={`section-heading ${light?'light':''}`}><span className="eyebrow">{eyebrow}</span><h2>{title}</h2>{copy&&<p>{copy}</p>}</motion.div> }
