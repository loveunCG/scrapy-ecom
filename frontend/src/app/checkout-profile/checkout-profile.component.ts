import { FormBuilder, Validators } from '@angular/forms';
import { Component, OnInit } from '@angular/core';
import { CheckoutService } from '../service/checkout.service';
import { Router, ActivatedRoute } from '@angular/router';
import { Angular2Csv } from 'angular2-csv/Angular2-csv';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-checkout-profile',
  templateUrl: './checkout-profile.component.html',
  styleUrls: ['./checkout-profile.component.css']
})
export class CheckoutProfileComponent implements OnInit {

  checkout:any;
  constructor(private fb:FormBuilder, private checkoutservice: CheckoutService, private router: Router) {
    this.checkout = fb.group({
      first_name:[null,[Validators.required,Validators.pattern('[^0-9]*')]],
      last_name:[null,[Validators.required,Validators.pattern('[^0-9]*')]],
      address_1:[null,Validators.required],
      address_2:[null,Validators.required],
      city:[null,Validators.required],
      state:[null,Validators.required],
      zipcode:[null,[Validators.required,Validators.pattern('[0-9]*')]],
      country:[null,Validators.required],
      email:[null,[Validators.required,Validators.email]],
      phone:[null,Validators.required],
      card:[null,Validators.required ],
      cvv:[null,Validators.required],
      expiryDate:[null,Validators.required],
      isPaypal:[null,Validators.required],
      paypalEmail:[null,[Validators.required,Validators.email]],
      paypalPassword:[null,Validators.required]
    })
  }

  ngOnInit() {


  }

  getErrorMessage() {
    return this.checkout.hasError('required') ? 'You must enter a value' :
        this.checkout.hasError('email') ? 'Not a valid email' :
            '';
  }

  saveCheckout(){
    // console.log('+++++',this.checkout.value);
        this.checkoutservice.checkoutProfile(this.checkout.value)
            .subscribe(
                data => {
                  //clear all forms
                    // data=data.json();
                    // if (data['stat'] === 'success'){
                    //   console.log('asdf')
                    //   //save data succesfully alert
                    //   //alert("Checkout Profile Created.");
                    //   Swal("Nice!", "Checkout Profile Created!", "success");
                    //   // this.checkout.reset();
                    // }
                    this.checkout.reset();
                    Swal("Nice!", "Checkout Profile Created!", "success");
                    this.router.navigate(['/home/checkout-profile']);
                    console.log(data);
                },
                error => {
                  console.log('test');
                  //alert errors
        });    
  }
  
  exportProfile(){
    var tmp_array = [];
    tmp_array.push(this.checkout.value);
    new Angular2Csv(tmp_array, 'Checkout profile');
  }
  csv2Array(fileInput: any){
    //read file from input
    // if (fileInput.target.files && fileInput.target.files.length>0){
      if (fileInput.target.files[0]){
        let tarr = [];
        let fileReaded = fileInput.target.files[0]; 
        let reader: FileReader = new FileReader();
        reader.readAsText(fileReaded);

          reader.onload = (e) => {
          let csv: string = reader.result;
          let allTextLines = csv.split(/\r|\n|\r/);
          let headers = allTextLines[0].split(',');
          let lines = [];

          for (let i = 0; i < allTextLines.length; i++) {
            // split content based on comma
            let data = allTextLines[i].split(',');
            if (data.length === headers.length) {
              for (let j = 0; j < headers.length; j++) {
                tarr.push(data[j]);
              }
             // log each row to see output 
             lines.push(tarr);
            }
          }
          // all rows in the csv file 
          if (tarr && tarr.length == 16){
            for (let i = 0; i < 16; i++)
            {
              if (i==12){
                let tmp = new Date(tarr[i]);
                let date_string;
                let tmp_year = tmp.getFullYear();
                let tmp_month;
                let tmp_date;
                if( tmp.getMonth() < 10 ){
                  tmp_month = '0' + tmp.getMonth();
                } else {
                  tmp_month = tmp.getMonth() + '';
                }
                tmp_date = tmp.getDate();
                date_string = tmp_year + '-' + tmp_month + '-' + tmp_date;
                this.checkout.value[Object.keys(this.checkout.value)[i]] = date_string;
                this.checkout.patchValue(this.checkout.value);
              } else {
                this.checkout.value[Object.keys(this.checkout.value)[i]] = tarr[i];
                this.checkout.patchValue(this.checkout.value);
              }
              // this.checkout.value[Object.keys(this.checkout.value)[i]] = tarr[i];
              // this.checkout.patchValue(this.checkout.value);
            }
          } else {
            //alert("No match CSV data style.")
            Swal("Wrong!", "No match CSV data style!", "error");
          }
        }
      } 
  }
  // importProfile(){

  //   $('#OpenImgUpload').click(function(){ $('#imgupload').trigger('click'); });
  // }
}

