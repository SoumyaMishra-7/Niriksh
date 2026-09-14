export type StaffStatus='Pending'|'Accepted'|'In Progress'|'Completed'
export type StaffTask={id:string;title:string;location:string;reason:string;description:string;priority:'critical'|'high'|'warning'|'normal';status:StaffStatus;time:string;type:'shelf'|'queue'|'camera';stock?:number;prediction?:string;confidence?:number}
