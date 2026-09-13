import { ArrowUpRight } from 'lucide-react'
export function Button({href,children,secondary=false,dark=false}:{href:string;children:React.ReactNode;secondary?:boolean;dark?:boolean}) { return <a href={href} className={`button ${secondary?'secondary':''} ${dark?'on-dark':''}`}>{children}<ArrowUpRight size={16}/></a> }
