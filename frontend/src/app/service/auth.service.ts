import { Injectable } from '@angular/core';
// import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Http, Response, RequestOptions, Headers, Request } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map'
 
@Injectable()
export class AuthService {
	private url = 'http://localhost:8000/api/v1/login/';
    constructor(private httpclient: Http) { }

    getHeader(): Headers {
        const headers = new Headers();
        //headers.append('content-type', 'application/x-www-form-urlencoded');
      headers.append('content-type', 'application/json');
        return headers;
    }

    login(username: string, password: string) {
    	console.log(username);

      let response = null;
      
      try {
        const requestOptions = new RequestOptions({
          headers: this.getHeader()
        });      

      response = this.httpclient.
          post(this.url, { 'username': username, 'password': password, 'csrfmiddlewaretoken': '{{ csrf_token }}'}, requestOptions)
            .map(user => {
                // login successful if there's a jwt token in the response
                if (user) {
                    // store user details and jwt token in local storage to keep user logged in between page refreshes
                    localStorage.setItem('currentUser', JSON.stringify(user));
                }
 
                return user;
            });
      } catch(e) {
        console.log(e)
      }
  
      
        return response; 
    }
 
    logout() {
        // remove user from local storage to log user out
        localStorage.removeItem('currentUser');
    }
}