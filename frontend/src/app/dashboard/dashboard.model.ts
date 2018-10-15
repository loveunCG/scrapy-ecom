export interface taskData {
  id: number;
    size: number;
    product: string;
    start_time: string,
    quantity: string,
    completed_date: string,
    keyword: string,
    checkout_type:string,
    status: string,
    action: string,
    checkout_id: number,
    proxy_id : number,
    site_id: number;
}

export interface checkoutProfileData {
  id: number;
  profile: string;
}

export interface ShopifyUrl {
  id: number;
  url: string;
}

export interface proxy {
  id: number;
  ip: string;
  port: number;
}


