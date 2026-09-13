import { motion } from 'framer-motion'
import { Check } from 'lucide-react'
import { features } from '../../data/content'
import { fadeUp } from '../../lib/motion'
import { SectionHeading } from '../ui/SectionHeading'
import { FeatureVisual } from './FeatureVisuals'
export function Features(){return <section id="intelligence" className="section features"><SectionHeading eyebrow="ONE CONNECTED PLATFORM" title="One camera network. Multiple layers of intelligence." copy="Every signal becomes context. Every insight points toward a clear operational decision."/><div className="feature-grid">{features.map((f,i)=><motion.article {...fadeUp} transition={{...fadeUp.transition,delay:i*.1}} className="feature-card" key={f.title}><div className="feature-head"><span className="icon-box"><f.icon size={20}/></span><span>0{i+1}</span></div><h3>{f.title}</h3><p>{f.description}</p><ul>{f.points.map(x=><li key={x}><Check size={14}/>{x}</li>)}</ul><FeatureVisual type={f.type}/></motion.article>)}</div></section>}
