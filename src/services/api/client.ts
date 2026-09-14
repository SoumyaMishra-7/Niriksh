const API_URL=import.meta.env.VITE_API_URL??'http://localhost:8000/api/v1'
export class ApiError extends Error{constructor(public status:number,message:string){super(message)}}
export async function api<T>(path:string,init?:RequestInit):Promise<T>{const res=await fetch(`${API_URL}${path}`,{...init,headers:{'Content-Type':'application/json',...init?.headers}});if(!res.ok){const body=await res.json().catch(()=>({detail:res.statusText}));throw new ApiError(res.status,body.detail)}return res.json()}
