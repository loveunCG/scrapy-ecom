import { Injectable } from '@angular/core';
// import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Http, Response, RequestOptions, Headers, Request } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map'

@Injectable()
export class ProxiesService {
	private url = 'http://localhost:8000/api/v1/proxies/';
	constructor(private httpclient: Http) { }
	
	getData1(){
		const requestOptions = new RequestOptions({
          headers: this.getHeader()
        });  
		return this.httpclient.
			get(this.url)
		    .map(user => {
		        // login successful if there's a jwt token in the response
		        if (user) {
		            // store user details and jwt token in local storage to keep user logged in between page refreshes
		            localStorage.setItem('proxies', JSON.stringify(user));
		        }
		        let res = JSON.stringify(user);
		        return res.slice();
	    });
	}

    getHeader() {
        const headers = new Headers();
        //headers.append('content-type', 'application/x-www-form-urlencoded');
        headers.append('content-type', 'application/json');
        return headers;
    }

	proxies(proxies: any){
        const requestOptions = new RequestOptions({
          headers: this.getHeader()
        });
		return this.httpclient.
			post(this.url, JSON.stringify(proxies), requestOptions)
		    .map(user => {
		        // login successful if there's a jwt token in the response
		        if (user) {
		            // store user details and jwt token in local storage to keep user logged in between page refreshes
		            localStorage.setItem('proxies', JSON.stringify(user));
		        }
		        return user;
	    });
	}
	proxiesLoad(){
        const requestOptions = new RequestOptions({
          headers: this.getHeader()
        });  
		return this.httpclient.
			get(this.url)
		    .map(user => {
		        // login successful if there's a jwt token in the response
		        if (user) {
		            // store user details and jwt token in local storage to keep user logged in between page refreshes
		            localStorage.setItem('proxies', JSON.stringify(user));
		        }
		        return user;
	    });
	}
	
}