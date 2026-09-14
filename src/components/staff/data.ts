import type { StaffTask } from './types'
export const initialStaffTasks:StaffTask[]=[
 {id:'ACT-1042',title:'Replenish Shelf A3',location:'Grocery · Aisle 2 · Shelf A3',reason:'Stock-out predicted in 24 minutes',description:'Bring Coca-Cola stock from the backroom and replenish the shelf.',priority:'critical',status:'Pending',time:'2 min ago',type:'shelf',stock:17,prediction:'24 minutes',confidence:92},
 {id:'ACT-1043',title:'Open Counter 4',location:'Checkout',reason:'Queue congestion predicted in 7 min',description:'Open Counter 4 to reduce expected waiting time.',priority:'high',status:'Pending',time:'3 min ago',type:'queue',prediction:'12 customers in 7 min',confidence:90},
 {id:'ACT-1044',title:'Check Camera 3',location:'Electronics',reason:'Camera visibility degraded',description:'Check the lens, remove any obstruction and verify the camera angle.',priority:'warning',status:'Pending',time:'6 min ago',type:'camera',confidence:68},
]
export const staffAlerts=[['critical','Shelf B4 running low','Predicted stock-out in 18 minutes','View task'],['high','Queue increasing','Checkout queue may become congested','View'],['warning','Camera 3 needs attention','Visibility confidence dropped','View task']] as const
