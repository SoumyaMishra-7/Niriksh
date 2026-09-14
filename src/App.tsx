import { lazy, Suspense } from 'react'
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { Navbar } from './components/layout/Navbar'
import { Footer, FinalCta } from './components/layout/Footer'
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
const DashboardShell = lazy(() => import('./components/dashboard/DashboardShell').then(m => ({ default: m.DashboardShell })))
const Shelves = lazy(() => import('./pages/dashboard/Shelves'))
const Queues = lazy(() => import('./pages/dashboard/Queues'))
const ShopperAnalytics = lazy(() => import('./pages/dashboard/ShopperAnalytics'))
const EdgeHealth = lazy(() => import('./pages/dashboard/EdgeHealth'))
const SignIn = lazy(() => import('./pages/SignIn'))
function ProtectedDashboard(){return localStorage.getItem('niriksh_auth')==='true' ? <DashboardShell/> : <Navigate to="/signin" replace state={{from:window.location.pathname}}/>}
function Landing(){return <><Navbar/><Hero/><ValueStrip/><Features/><Process/><StoreMap/><Privacy/><Offline/><Workflow/><MobileCompanion/><EdgeImpact/><FinalCta/><Footer/></>}
export default function App(){return <BrowserRouter><Suspense fallback={<div className="route-loader" aria-label="Loading"><i/><span>Loading intelligence...</span></div>}><Routes><Route path="/" element={<Landing/>}/><Route path="/signin" element={<SignIn/>}/><Route path="/dashboard" element={<ProtectedDashboard/>}><Route index element={<Navigate to="shelves" replace/>}/><Route path="shelves" element={<Shelves/>}/><Route path="queues" element={<Queues/>}/><Route path="shopper-analytics" element={<ShopperAnalytics/>}/><Route path="edge-health" element={<EdgeHealth/>}/></Route><Route path="*" element={<Navigate to="/dashboard/shelves" replace/>}/></Routes></Suspense></BrowserRouter>}
