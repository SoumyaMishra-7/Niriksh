import { lazy,Suspense } from 'react'
import { BrowserRouter,Route,Routes } from 'react-router-dom'
import { Navbar } from './components/layout/Navbar'
import { Footer,FinalCta } from './components/layout/Footer'
import { Hero } from './components/landing/Hero'
import { ValueStrip } from './components/landing/ValueStrip'
import { Features } from './components/landing/Features'
import { Process } from './components/landing/Process'
import { StoreMap } from './components/landing/StoreMap'
import { Privacy } from './components/landing/Privacy'
import { Offline } from './components/landing/Offline'
import { Workflow } from './components/landing/Workflow'
import { MobileCompanion } from './components/landing/MobileCompanion'
import { EdgeImpact } from './components/landing/EdgeImpact'
const DashboardShell=lazy(()=>import('./components/dashboard/DashboardShell').then(m=>({default:m.DashboardShell})))
const Overview=lazy(()=>import('./pages/dashboard/ManagerOverview'))
const LiveStore=lazy(()=>import('./pages/dashboard/ManagerLiveStore'))
const Shelves=lazy(()=>import('./pages/dashboard/Shelves'))
const Queues=lazy(()=>import('./pages/dashboard/Queues'))
const ShopperAnalytics=lazy(()=>import('./pages/dashboard/ShopperAnalytics'))
const Actions=lazy(()=>import('./pages/dashboard/Actions'))
const Reports=lazy(()=>import('./pages/dashboard/Reports'))
const EdgeHealth=lazy(()=>import('./pages/dashboard/EdgeHealth'))
const StaffApp=lazy(()=>import('./components/staff/StaffApp'))
function Landing(){return <><Navbar/><Hero/><ValueStrip/><Features/><Process/><StoreMap/><Privacy/><Offline/><Workflow/><MobileCompanion/><EdgeImpact/><FinalCta/><Footer/></>}
export default function App(){return <BrowserRouter><Suspense fallback={<div className="route-loader" aria-label="Loading"><i/><span>Loading intelligence...</span></div>}><Routes><Route path="/" element={<Landing/>}/><Route path="/staff/*" element={<StaffApp/>}/><Route path="/dashboard" element={<DashboardShell/>}><Route index element={<Overview/>}/><Route path="live-store" element={<LiveStore/>}/><Route path="shelves" element={<Shelves/>}/><Route path="queues" element={<Queues/>}/><Route path="shopper-analytics" element={<ShopperAnalytics/>}/><Route path="actions" element={<Actions/>}/><Route path="reports" element={<Reports/>}/><Route path="edge-health" element={<EdgeHealth/>}/></Route></Routes></Suspense></BrowserRouter>}
