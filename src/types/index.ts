import type { LucideIcon } from 'lucide-react'
export type Feature = { title: string; description: string; points: string[]; icon: LucideIcon; type: 'shelf' | 'shopper' | 'queue' }
export type Zone = { id: string; name: string; shoppers: number; dwell: string; traffic: string; status: string; grid: string }
