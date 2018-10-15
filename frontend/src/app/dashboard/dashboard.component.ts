import { DashboardService } from './dashboard.service';
import { Component, OnInit, NgModule, ViewChild } from '@angular/core';
import { MatTableDataSource, MatSort, MatPaginator } from '@angular/material';
import { taskData, checkoutProfileData, proxy } from './dashboard.model';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css'],
  providers: [DashboardService]
})
export class DashboardComponent implements OnInit {

  @ViewChild(MatSort) sort: MatSort;
  @ViewChild(MatPaginator) paginator: MatPaginator;
  displayedColumns = [
    'id',
    'site',
    'product',
    'size',
    'start_time',
    'profile',
    'proxy',
    'status',
    'action'
  ];
  dataSource: any;

  constructor(private dashboardService: DashboardService) { }

  ngOnInit() {
    this.dashboardService.loadTasksFromDB().subscribe(tasks => {
      this.dashboardService.task_data = tasks;
      this.dataSource = new MatTableDataSource(this.dashboardService.task_data);
      this.dataSource.sort = this.sort;
      this.dataSource.paginator = this.paginator;
    });
  }

  ngAfterViewInit() {
  }


  generateTasksCSV() {
    this.dashboardService.generateTaskCSV();
  }

  applyFilter(filterValue: string) {
    filterValue = filterValue.trim();
    filterValue = filterValue.toLowerCase();
    this.dataSource.filter = filterValue;
  }


  trimInvertedCommas(value: string): string {
    let ret = value.replace(/["]/g, "");
    return ret;
  }

  import_tasks(fileInput: any) {
    if (fileInput.target.files[0]) {
      let fileReaded = fileInput.target.files[0];
      let reader: FileReader = new FileReader();

      reader.onload = () => {
        let csv: string = reader.result;
        //let allTextLines = csv.split(/\r|\n|\r/);
        let allTextLines = csv.split(/\n/);
        let res_import = [];
        let data = [];
        let tasks: taskData[] = [];

        for (let i = 0; i < allTextLines.length; i++) {

          if (allTextLines[i] != "") {
            data = allTextLines[i].split(',');
            if (data.length == 13) {

              let newTask:taskData = {
                id : Number(this.trimInvertedCommas(String(data[0]))),
                size: Number(this.trimInvertedCommas(String(data[1]))),
                product: this.trimInvertedCommas(String(data[2])),
                start_time: this.trimInvertedCommas(String(data[3])),
                quantity : this.trimInvertedCommas(String(data[4])),
                completed_date : this.trimInvertedCommas(String(data[5])),
                keyword : this.trimInvertedCommas(String(data[6])),
                checkout_type: this.trimInvertedCommas(String(data[7])),
                status: this.trimInvertedCommas(String(data[8])),
                action: this.trimInvertedCommas(String(data[9])),
                checkout_id:  Number(this.trimInvertedCommas(String(data[10]))),
                proxy_id: Number(this.trimInvertedCommas(String(data[11]))),
                site_id: Number(this.trimInvertedCommas(String(data[12]))),
              };
              tasks.push(newTask);
              console.log("task added {i}");
            }
          }
        }
        this.dashboardService.task_data = tasks;
        this.dashboardService.saveTasksToDB();
      }
      reader.readAsText(fileReaded);
    }
  }



}
