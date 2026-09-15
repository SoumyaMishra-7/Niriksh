import { useState } from 'react'
import { DoorOpen, Timer, UsersRound, TrendingUp, Clock3 } from 'lucide-react'
import { queues } from '../../data/queues'
import { QueueLine } from '../../components/dashboard/Charts'
import { KpiCard } from '../../components/dashboard/KpiCard'
import { Card, PageHeader, SectionHeader, StatusBadge, Tabs } from '../../components/dashboard/ui'

const peaks = [['12:00–1:00 PM', '9 people', 'Highest lunch build-up'], ['3:00–4:00 PM', '11 people', 'Highest average wait'], ['6:00–7:00 PM', '14 people', 'Friday peak pattern']]

export default function Queues() {
  const [tab, setTab] = useState('All counters')
  const visible = queues.filter(q => tab === 'All counters' || (tab === 'Open' ? q.status === 'Open' : q.status === 'Closed'))
  return <>
    <PageHeader eyebrow="QUEUE INTELLIGENCE" title="Queue intelligence" copy="Forecast congestion before it becomes a customer-experience problem." actions={<StatusBadge status="warning" label="1 congestion risk" />} />
    <div className="compact-kpis"><KpiCard label="Open counters" value="3 / 4" note="Counter 4 available" icon={DoorOpen}/><KpiCard label="Customers waiting" value="13" note="Across open counters" icon={UsersRound}/><KpiCard label="Avg wait" value="2.9 min" note="+0.6 min this hour" icon={Timer} tone="amber"/><KpiCard label="7-min forecast" value="22" note="+9 customers" icon={TrendingUp} tone="red"/><KpiCard label="Peak period" value="6–7 PM" note="Friday pattern" icon={Clock3} tone="violet"/></div>
    <section className="overview-section"><SectionHeader title="Counter status" copy="Current queue, expected wait, and short-horizon congestion forecast."/><Tabs items={['All counters','Open','Closed']} value={tab} onChange={setTab}/><div className="queue-grid">{visible.map(q => <Card className={`queue-card-d ${q.status === 'Closed' ? 'closed' : ''}`} key={q.id}><header><div><small>CHECKOUT</small><h3>{q.id}</h3></div><StatusBadge status={q.status === 'Closed' ? 'offline' : q.risk} label={q.status}/></header><div className="queue-main"><strong>{q.length}</strong><span>people<br/>now</span><b>{q.wait} min <small>est. wait</small></b></div><dl><div><dt>Arrival rate</dt><dd>{q.arrival}/min</dd></div><div><dt>Service rate</dt><dd>{q.service}/min</dd></div><div><dt>Predicted queue</dt><dd>{q.predicted} in {q.predictionTime}</dd></div></dl><footer><span className={q.risk === 'critical' ? 'risk-critical' : ''}>{q.recommendation}</span></footer></Card>)}</div></section>
    <div className="queue-intelligence-grid"><Card className="chart-panel"><SectionHeader title="Queue trend" copy="Observed queue size with short-horizon prediction."/><QueueLine/></Card><Card className="peak-card"><SectionHeader title="Historical peak periods" copy="Recurring congestion patterns from the last 30 days."/>{peaks.map(([time,count,note]) => <div className="peak-row" key={time}><div><b>{time}</b><span>{note}</span></div><strong>{count}</strong></div>)}</Card></div>
  </>
}
