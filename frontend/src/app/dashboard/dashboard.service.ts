import { taskData, checkoutProfileData } from './dashboard.model';
import { Injectable } from '@angular/core';
import { Http, Response, RequestOptions, Headers, Request } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import { catchError } from 'rxjs/operators';
// Import RxJs required methods
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';

@Injectable()
export class DashboardService {

  private task_url = 'http://localhost:8000/api/v1/createtask/';
  private checkout_url = 'http://localhost:8000/api/v1/billings/';

  task_data: taskData[];

  constructor(private httpclient: Http) { }


  importData() {
    let response_data;
    this.saveTasksToDB().subscribe(
      (data) => {
        response_data = data;
        console.log(data);
      }
    );
  }



  getData() {
    let response_data;
    let tasks: taskData[];

    //this.loadTasksFromDB().subscribe((data) => {
    //  this.task_data = data;
    //  });
    //return this.task_data.slice();

   // this.task_data = response_data;

    //return tasks.slice();
  }

  getHeader() {
    const headers = new Headers();
    //headers.append('content-type', 'application/x-www-form-urlencoded');
    headers.append('content-type', 'application/json');
    return headers;
  }

  saveTasksToDB() {
    const requestOptions = new RequestOptions({
      headers: this.getHeader()
    });
    let ret: any;
    try {
      ret = this.httpclient.post(this.task_url, this.task_data).map((res: Response) => res.json()).subscribe(e=>console.log(e));

    } catch (e) {
      console.error(e);
    }

    return ret;
    }


  generateTaskCSV() {
    this.loadTasksFromDB().subscribe(tasks => {

      let csvContent = "data:text/csv;charset=utf-8,";

      csvContent = csvContent + this.fetchCSVFromObjects(tasks);
      const encodedUri = encodeURI(csvContent);
      window.open(encodedUri);
    });
  }


  private fetchCSVFromObjects(tasks: taskData[]): string {
    let csv: string;
    // Loop the array of objects
    for (let row = 0; row < tasks.length; row++) {
      const keysAmount = Object.keys(tasks[row]).length
      let keysCounter = 0

      // If this is the first row, generate the headings
      if (row === 0) {

        // Loop each property of the object
        for (const key in tasks[row]) {
          if (key != null) {
          // This is to not add a comma at the last cell
          // The '\r\n' adds a new line
          csv += key + (keysCounter + 1 < keysAmount ? ',' : '\r\n')
          keysCounter++
          }
        }
      } else {
        for (const key in tasks[row]) {
          if (key != null) {
            csv += tasks[row][key] + (keysCounter + 1 < keysAmount ? ',' : '\r\n')
            keysCounter++
            }
        }
      }

      keysCounter = 0
    }

    return csv;
  }

  loadTasksFromDB() {
    const requestOptions = new RequestOptions({
      headers: this.getHeader()
    });

    return this.httpclient.get(this.task_url).map(res => res.json());
  }
}
