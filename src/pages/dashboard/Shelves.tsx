import { useMemo, useState } from 'react'
import { Boxes, CheckCircle2, PackageMinus, ScanLine, ShieldCheck, CalendarDays, Radio } from 'lucide-react'
import { shelves } from '../../data/shelves'
import type { Shelf } from '../../types/dashboard'
import { KpiCard } from '../../components/dashboard/KpiCard'
import { Card, DButton, Modal, PageHeader, SearchInput, Select, StatusBadge } from '../../components/dashboard/ui'
import { MiniChart } from '../../components/dashboard/Charts'

const stockHistory = [
  { time: '09:00', value: 86 }, { time: '10:00', value: 74 }, { time: '11:00', value: 63 },
  { time: '12:00', value: 51 }, { time: '13:00', value: 39 }, { time: '14:00', value: 27 }, { time: 'Now', value: 17 },
]
const replenishments = [
  ['08 Sep', '24 units', 'Completed'], ['05 Sep', '36 units', 'Completed'], ['01 Sep', '24 units', 'Completed'],
]

export default function Shelves() {
  const [search, setSearch] = useState(''), [status, setStatus] = useState('all'), [zone, setZone] = useState('all'), [category, setCategory] = useState('all'), [selected, setSelected] = useState<Shelf | null>(null)
  const zones = [...new Set(shelves.map(s => s.zone))], categories = [...new Set(shelves.map(s => s.category))]
  const rows = useMemo(() => shelves.filter(s =>
    (status === 'all' || (status === 'oos' ? s.availability === 0 : s.status === status)) &&
    (zone === 'all' || s.zone === zone) && (category === 'all' || s.category === category) &&
    (s.product + s.id + s.zone + s.category).toLowerCase().includes(search.toLowerCase())
  ), [search, status, zone, category])
  return <>
    <PageHeader eyebrow="SHELF INTELLIGENCE" title="Shelf intelligence" copy="See exactly where availability is falling, why it matters, and when a shelf is likely to go empty." actions={<div className="shelf-header-actions"><div className="header-date"><CalendarDays/><span><b>Sep 14, 2026</b><small>10:24 PM</small></span></div><StatusBadge status="normal" label="Live data" /></div>} />
    <div className="compact-kpis">
      <KpiCard label="Overall Availability" value="91.8%" note="+2.4% from yesterday" icon={Boxes} progress={91.8} trend={2.4} />
      <KpiCard label="Healthy Shelves" value="72 / 84" note="85.7% of shelves" icon={CheckCircle2} progress={85.7} />
      <KpiCard label="Low Stock" value="7" note="8.3% of shelves" icon={PackageMinus} tone="amber" progress={8.3} />
      <KpiCard label="Out of Stock" value="2" note="2.4% of shelves" icon={PackageMinus} tone="red" progress={2.4} />
      <KpiCard label="Planogram Issues" value="3" note="3.6% of shelves" icon={ScanLine} tone="violet" progress={3.6} />
    </div>
    <Card className="filters shelf-filters">
      <SearchInput value={search} onChange={setSearch} placeholder="Search shelf, SKU or product" />
      <Select label="Status" value={status} onChange={setStatus}><option value="all">All status</option><option value="critical">Critical</option><option value="warning">High</option><option value="attention">Warning</option><option value="normal">Healthy</option><option value="oos">Out of stock</option></Select>
      <Select label="Zone" value={zone} onChange={setZone}><option value="all">All zones</option>{zones.map(z => <option key={z}>{z}</option>)}</Select>
      <Select label="Category" value={category} onChange={setCategory}><option value="all">All categories</option>{categories.map(c => <option key={c}>{c}</option>)}</Select>
    </Card>
    <Card className="data-table intelligence-table"><table><thead><tr><th>Shelf</th><th>Product / SKU</th><th>Availability</th><th>Severity</th><th>Predicted stock-out</th><th>AI confidence</th><th>Recommendation</th></tr></thead><tbody>{rows.map(s => <tr key={s.id} onClick={() => setSelected(s)} tabIndex={0}>
      <td><b>Shelf {s.id}</b><small>{s.zone}</small></td><td><b>{s.product}</b><small>SKU {s.id}-COKE-{s.category.slice(0, 3).toUpperCase()}</small></td>
      <td><div className="availability"><span><i className={s.availability === 0 ? 'critical' : ''} style={{ width: `${s.availability}%` }} /></span><b>{s.availability}%</b></div></td>
      <td><StatusBadge status={s.availability === 0 ? 'critical' : s.status} label={s.availability === 0 ? 'OOS' : s.status === 'critical' ? 'Critical' : s.status === 'warning' ? 'High' : s.status === 'attention' ? 'Warning' : 'Healthy'} /></td>
      <td><b>{s.oos}</b></td><td><span className="confidence-pill">{s.confidence}%</span></td><td><button className="recommend-link">{s.recommendation} →</button></td>
    </tr>)}</tbody></table></Card>
    <Modal open={!!selected} onClose={() => setSelected(null)} title={`Shelf ${selected?.id} · ${selected?.product}`}>
      {selected && <ShelfDetail shelf={selected} />}
    </Modal>
  </>
}

function ShelfDetail({ shelf }: { shelf: Shelf }) {
  return <div className="shelf-detail">
    <div className="detail-hero-grid">
      <div className="ai-shelf"><span><ShieldCheck /> LOCAL VISION DETECTION</span>{[1, 2, 3, 4, 5].map((x, i) => <i key={x} className={i >= 3 || shelf.availability === 0 ? 'empty' : ''}><b>{i >= 3 || shelf.availability === 0 ? 'EMPTY' : 'DETECTED'}</b></i>)}</div>
      <div className="detail-summary"><div><small>CURRENT STOCK</small><strong>{shelf.availability}%</strong><StatusBadge status={shelf.status} /></div><div><small>PREDICTED OOS</small><strong>{shelf.oos}</strong><span>{shelf.confidence}% AI confidence</span></div><div className="detail-action"><small>RECOMMENDATION</small><b>{shelf.recommendation}</b></div></div>
    </div>
    <div className="detail-two-col"><Card><div className="d-section-head"><div><h2>Stock trend</h2><p>Depletion velocity over the current trading window.</p></div><span className="trend down">−69%</span></div><MiniChart type="shelf" /></Card><Card><div className="d-section-head"><div><h2>Historical replenishment</h2><p>Recent replenishment events for this shelf.</p></div></div><div className="replenishment-list">{replenishments.map(([date, qty, state]) => <div key={date}><b>{date}</b><span>{qty}</span><StatusBadge status="normal" label={state} /></div>)}</div></Card></div>
    <div className="detail-insight"><ShieldCheck /><div><b>Why this prediction?</b><span>Model combines current facing availability, depletion velocity, recent replenishment cadence, and local shopper traffic.</span></div><strong>{shelf.confidence}% confidence</strong></div>
  </div>
}
