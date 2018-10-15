import { Component, OnInit, NgModule, ViewChild } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { ProxiesService } from '../service/proxies.service';;
import { Router, ActivatedRoute } from '@angular/router';
import { Angular2Csv } from 'angular2-csv/Angular2-csv';
import Swal from 'sweetalert2';
import {MatTableDataSource, MatSort, MatPaginator} from '@angular/material';
import {SelectionModel} from '@angular/cdk/collections';

@Component({
  selector: 'app-proxies',
  templateUrl: './proxies.component.html',
  styleUrls: ['./proxies.component.css'],
  providers: [ProxiesService]
})
export class ProxiesComponent implements OnInit {
  @ViewChild(MatSort)sort: MatSort;
  @ViewChild(MatPaginator)paginator: MatPaginator;
  displayedColumns1 = [
    'select',
    'ip',
    'port',
    'action'
  ];
  proxies:any;
  dataSource1:any;
  selection:any;
  tmp_data:any;
  constructor(private fb:FormBuilder, private proxiesService: ProxiesService, private router: Router) {
  	this.proxies = fb.group({
      proxies_list:['']
    })
  }

  ngOnInit() {
    this.proxiesService.proxiesLoad()
        .subscribe(
            res_data => {
              //clear all forms
                let data=res_data.json();
                this.tmp_data = data;
                for (let i = 0; i < this.tmp_data.length; i++){
                  this.tmp_data[i]['action']=null;
                }

                this.dataSource1 = new MatTableDataSource( this.tmp_data.slice() );
                this.selection = new SelectionModel(true, []);
                this.dataSource1.sort = this.sort;
                this.dataSource1.paginator = this.paginator;

                this.router.navigate(['/home/proxies']);
            },
            error => {
              //alert errors
    });
  }

  ngAfterViewInit() {
    // this.dataSource1.sort = this.sort;
    // this.dataSource1.paginator = this.paginator;
  }

  isAllSelected() {
    const numSelected = this.selection.selected.length;
    const numRows = this.dataSource1.data.length;
    return numSelected === numRows;
  }

  /** Selects all rows if they are not all selected; otherwise clear selection. */
  masterToggle() {
    this.isAllSelected() ?
        this.selection.clear() :
        this.dataSource1.data.forEach(row => this.selection.select(row));
  }

  validate_ipaddress_port(str){
  	// if ":"'s count is 1 then
  	let proxy_tmp 		= ""; // gmail_account tmp variable
  	let port_tmp 		= ""; // password tmp variable
  	let resJson			= {}; // return value variable
  	let proxy_re		= /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
  	let port_re			= /[0-9]+$/;
  	if ( ( str.split(":").length - 1 ) === 1 ){
  		// correct string type
  		let split_res 	= str.split(":");
  		proxy_tmp 		= split_res[0].trim().toLowerCase();
  		port_tmp 		= split_res[1];
  		if ( proxy_re.test( proxy_tmp ) && ( ( port_re.test( port_tmp ) ) && ( parseInt(port_tmp)  < 65536 ) ) ){
  			resJson["ip"] 	= proxy_tmp;
  			resJson["port"] = port_tmp;
        return resJson;
  		} else {
  			return false;
  		}
  	} else {
  		// not correct string
  		return false;
  	}
  	
  }

  save_proxy(){
    if (this.tmp_data.length>0){
      this.proxiesService.proxies(this.tmp_data)
          .subscribe(
              data => {
                //clear all forms
                  data = data.json();
                  if (data['stat'] === 'success'){
                    //save data succesfully alert
                    Swal("Nice!", "Proxy lists are saved!", "success");
                  }
                  this.router.navigate(['/home/proxies']);
              },
              error => {
                //alert errors
      });
    } else {
      Swal("Wrong!", "No data to be saved.", "error");
    }

  }

  delete_proxy(){
  	this.proxies.reset();
    Swal("Clear!", "All data is cleared.", "success");
  }

  test_proxy(){
  	console.log("test_proxy");
  }

  export_proxy(){
    let exportJsonArray = this.tmp_data;
    if (this.tmp_data.length > 0){
      for (let i = 0; i < exportJsonArray.length ; i ++){
        delete exportJsonArray[i]["id"];
        delete exportJsonArray[i]["action"];
      }
      new Angular2Csv(exportJsonArray, 'Proxy Lists');
    } else {
      Swal("Wrong!", "No data to be exported.", "error");
    }
  }

  import_proxy(fileInput: any){
  	if (fileInput.target.files[0]){
		let fileReaded 			= fileInput.target.files[0]; 
		let reader: FileReader 	= new FileReader();
		reader.readAsText(fileReaded);
		let exist_flag	= 0;
		reader.onload = (e) => {
			let csv: string 	= reader.result;
			let allTextLines 	= csv.split(/\r|\n|\r/);
			let res_import		= [];
			let data = [];
			for ( let i = 0; i < allTextLines.length; i++ ) {
				if ( allTextLines[i] != "" ){
					data = allTextLines[i].split( ',' );
					if ( data.length == 2 ){
						let ip_tmp 		= data[0].replace( new RegExp('"','g') , '' );
						let port_tmp 	= data[1].replace( new RegExp('"','g') , '' );
						let proxy_re	= /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
  						let port_re		= /[0-9]+$/;
  						if ( proxy_re.test( ip_tmp ) && ( ( port_re.test( port_tmp ) ) && ( parseInt(port_tmp)  < 65536 ) ) ){
							exist_flag = 1;
							res_import.push({"action":null,"ip":ip_tmp,"port":port_tmp});
						} else {
              Swal("Wrong!", "No Match CSV Data Style.", "error");
							return false;
						}
					}
				}	
			}
			if ( exist_flag == 0 )
			{
        Swal("Wrong!", "No Match CSV Data Style.", "error");
				return false;
			}
			else
			{
				this.tmp_data = res_import;
        this.dataSource1 = new MatTableDataSource( this.tmp_data.slice() );
        this.selection = new SelectionModel(true, []);
        this.dataSource1.sort = this.sort;
        this.dataSource1.paginator = this.paginator;
        this.proxies.reset();
			}
		}
	}
}

  saveItemToTable(){
    let saveSubRes = true;
    if (this.proxies.value["proxies_list"] != ''){
      if (this.validate_ipaddress_port(this.proxies.value["proxies_list"])){
        let saveItemTmp = this.validate_ipaddress_port(this.proxies.value["proxies_list"]);
        for (let i = 0; i < this.tmp_data.length; i++){
          if ((this.tmp_data[i].ip == saveItemTmp["ip"]) && (this.tmp_data[i].port == saveItemTmp["port"])){
            saveSubRes = false;
          }
        }
        if (saveSubRes) {
          this.tmp_data.push(this.validate_ipaddress_port(this.proxies.value["proxies_list"]))
          this.dataSource1 = new MatTableDataSource( this.tmp_data.slice() );
          this.selection = new SelectionModel(true, []);
          this.dataSource1.sort = this.sort;
          this.dataSource1.paginator = this.paginator;
          this.proxies.reset();
        } else {
          Swal("Wrong!", "This data is in list already.", "error");
        }
      }
      else
      {
        Swal("Wrong!", "Please input Correct Data.", "error");  
      }
      
    } else {
      Swal("Wrong!", "Please input Data.", "error");
    }
  }

  delete_item(ipVal:any, portVal:any){
    Swal({
      title: 'Are you sure?',
      text: 'You will not be able to recover before refresh this page!',
      type: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Yes, delete it!',
      cancelButtonText: 'No, keep it'
    }).then((result) => {
      if (result.value) {
        for (let i = 0; i < this.tmp_data.length; i ++){
                if ((this.tmp_data[i].ip == ipVal) && (this.tmp_data[i].port == portVal)){
                  this.tmp_data.splice(i,1);
                }
              }

        this.dataSource1 = new MatTableDataSource( this.tmp_data.slice() );
        this.selection = new SelectionModel(true, []);
        this.dataSource1.sort = this.sort;
        this.dataSource1.paginator = this.paginator;
        Swal(
          'Deleted!',
          'Your proxy data has been deleted from list. Please click "save to bot" button for saving data.',
          'success'
        )
      } else if (result.dismiss === Swal.DismissReason.cancel) {
        Swal(
          'Cancelled',
          'Your proxy data is safe.',
          'error'
        )
      }
    })
  }

  async edit_item( ipVal:any, portVal:any ){
    let subres = false;
    let editable_data;
    let checkbit = true;

    for (let i = 0; i < this.tmp_data.length; i++){
      if ((this.tmp_data[i].ip == ipVal) && (this.tmp_data[i].port == portVal)){
        editable_data = this.tmp_data[i].ip + ":" + this.tmp_data[i].port;
      }
    }

    await Swal({
      title: 'Please input new ip and port.',
      input: 'text',
      inputPlaceholder: 'Enter your name or nickname',
      inputValue : editable_data,
      showCancelButton: true,
      inputValidator: (value) => {
        let valueArray = value.split(":");
        let resEdit = {};
        if (valueArray.length ==2){
          let proxy_re    = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
          let port_re     = /[0-9]+$/;
          if ( proxy_re.test( valueArray[0].trim() ) && ( ( port_re.test( valueArray[1].trim() ) ) && ( parseInt(valueArray[1].trim())  < 65536 ) ) ){

            resEdit["ip"] = valueArray[0].trim();
            resEdit["port"] = parseInt(valueArray[1].trim());

            for (let i = 0; i < this.tmp_data.length; i++){
              if ((this.tmp_data[i].ip == resEdit["ip"]) && (this.tmp_data[i].port == resEdit["port"])){
                checkbit = false;
              }
            }

            if (checkbit){
              for (let i = 0; i < this.tmp_data.length; i++){
                if ((this.tmp_data[i].ip == ipVal) && (this.tmp_data[i].port == portVal)){
                  this.tmp_data[i].ip   = resEdit["ip"];
                  this.tmp_data[i].port = resEdit["port"];
                }
              }
              this.dataSource1 = new MatTableDataSource( this.tmp_data.slice() );
              this.selection = new SelectionModel(true, []);
              this.dataSource1.sort = this.sort;
              this.dataSource1.paginator = this.paginator;
              subres = true;
            }

          } else {
            subres = false;
          }
        } else {
          subres = false;
        }
        return !value && 'You need to write something!'
      }
    })
    if(subres){
      Swal("Nice!", "Proxy data is saved. Please click 'save to bot' button for saving all data.", "success");  
    } else {
      if (!checkbit){
        Swal("Wrong!", "This data is in list already.", "error");  
      } else {
        Swal("Wrong!", "Please input correct data.", "error");  
      }
    }
  }
}
