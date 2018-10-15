import { Injectable } from '@angular/core';
// import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Http, Response, RequestOptions, Headers, Request } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map'

@Injectable()
export class GmailaccountService {
	private url = 'http://localhost:8000/api/v1/savegmail/';
	constructor(private httpclient: Http) { }

    getHeader() {
        const headers = new Headers();
        //headers.append('content-type', 'application/x-www-form-urlencoded');
        headers.append('content-type', 'application/json');
        return headers;
    }

	gmailAccount(gmail_account: any) {
        const requestOptions = new RequestOptions({
          headers: this.getHeader()
        });  
		return this.httpclient.
			post(this.url, JSON.stringify(gmail_account), requestOptions)
		    .map(user => {
		        // login successful if there's a jwt token in the response
		        if (user) {
		            // store user details and jwt token in local storage to keep user logged in between page refreshes
		            localStorage.setItem('gmail_account', JSON.stringify(user));
		        }
		        return user;
	    });
	}

	gmailAccountLoad(){
        const requestOptions = new RequestOptions({
          headers: this.getHeader()
        });  
		return this.httpclient.
			get(this.url)
		    .map(user => {
		        // login successful if there's a jwt token in the response
		        if (user) {
		            // store user details and jwt token in local storage to keep user logged in between page refreshes
		            localStorage.setItem('gmail_account', JSON.stringify(user));
		        }
		        return user;
	    });
	}
}