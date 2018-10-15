import { Injectable } from '@angular/core';
// import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Http, Response, RequestOptions, Headers, Request } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map'

@Injectable()
export class CheckoutService {
	private url = 'http://localhost:8000/api/v1/billings/';
	constructor(private httpclient: Http) { }

    getHeader() {
        const headers = new Headers();
        //headers.append('content-type', 'application/x-www-form-urlencoded');
        headers.append('content-type', 'application/json');
        return headers;
    }

	checkoutProfile(checkout: any){
        const requestOptions = new RequestOptions({
          headers: this.getHeader()
        });
		return this.httpclient.
			post(this.url, JSON.stringify(checkout), requestOptions)
		    .map(user => {
		        // login successful if there's a jwt token in the response
		        if (user) {
		            // store user details and jwt token in local storage to keep user logged in between page refreshes
		            localStorage.setItem('currentUser', JSON.stringify(user));
		        }
		        return user;
	    });
  }
}
