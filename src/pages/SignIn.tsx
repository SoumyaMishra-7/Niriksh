import { FormEvent, useState } from 'react'
import { ArrowLeft, Eye, EyeOff, LockKeyhole, Mail, ShieldCheck } from 'lucide-react'
import { Link, useLocation, useNavigate } from 'react-router-dom'

const DEMO_EMAIL = 'manager@niriksh.ai'
const DEMO_PASSWORD = 'niriksh123'

export default function SignIn() {
  const navigate = useNavigate()
  const location = useLocation()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const from = (location.state as { from?: string } | null)?.from || '/dashboard/shelves'

  function submit(event: FormEvent) {
    event.preventDefault()
    setError('')
    setLoading(true)
    window.setTimeout(() => {
      if (email.trim().toLowerCase() === DEMO_EMAIL && password === DEMO_PASSWORD) {
        localStorage.setItem('niriksh_auth', 'true')
        localStorage.setItem('niriksh_user', JSON.stringify({ name: 'Arjun Kumar', role: 'Store Manager', email: DEMO_EMAIL }))
        navigate(from, { replace: true })
      } else {
        setError('Incorrect email or password. Use the demo credentials shown below.')
        setLoading(false)
      }
    }, 350)
  }

  return <main className="signin-page">
    <div className="signin-shell">
      <Link to="/" className="signin-back"><ArrowLeft size={17}/> Back to Niriksh</Link>
      <section className="signin-card">
        <div className="signin-brand"><span>N</span><b>Niriksh</b></div>
        <div className="signin-heading"><div className="signin-icon"><LockKeyhole size={20}/></div><div><p>SECURE ACCESS</p><h1>Sign in to Niriksh</h1><span>Access your retail intelligence workspace.</span></div></div>
        <form onSubmit={submit}>
          <label>Email<input type="email" autoComplete="email" value={email} onChange={e=>setEmail(e.target.value)} placeholder="you@company.com" required/><Mail size={17}/></label>
          <label>Password<div className="signin-password"><input type={showPassword?'text':'password'} autoComplete="current-password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="Enter your password" required/><button type="button" onClick={()=>setShowPassword(v=>!v)} aria-label={showPassword?'Hide password':'Show password'}>{showPassword?<EyeOff size={17}/>:<Eye size={17}/>}</button></div></label>
          {error && <div className="signin-error">{error}</div>}
          <button className="signin-submit" disabled={loading}>{loading?'Signing in…':'Sign in'}</button>
        </form>
        <div className="signin-demo"><strong>Demo access</strong><span><b>Email</b> {DEMO_EMAIL}</span><span><b>Password</b> {DEMO_PASSWORD}</span></div>
        <div className="signin-privacy"><ShieldCheck size={16}/><span>Privacy-first edge analytics. Customer identities are never stored.</span></div>
      </section>
    </div>
  </main>
}
