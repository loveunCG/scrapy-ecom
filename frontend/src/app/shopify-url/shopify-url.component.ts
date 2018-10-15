import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { ShopifyurlService } from '../service/shopifyurl.service';
import { Router, ActivatedRoute } from '@angular/router';
import { Angular2Csv } from 'angular2-csv/Angular2-csv';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-shopify-url',
  templateUrl: './shopify-url.component.html',
  styleUrls: ['./shopify-url.component.css']
})
export class ShopifyURLComponent implements OnInit {
  // const Swal = require('sweetalert2');
	shopify_urls:any;
  constructor(private fb:FormBuilder, private shopifyurlService: ShopifyurlService, private router: Router) {
  	this.shopify_urls = fb.group({
      shopify_urls:['']
    });
  }
  ngOnInit() {
    this.shopifyurlService.shopifyURLLoad()
              .subscribe(
                  res_data => {
                    //clear all forms
                      let data=res_data.json();
                      let strRes = "";
                      if ( data.length > 0 ){
                        for ( let i = 0; i < data.length; i++ ){
                          strRes = strRes + data[i].url ;
                          if ( i < ( data.length - 1 ) ){
                            strRes = strRes + '\n';
                          }
                        }
                        this.shopify_urls.value["shopify_urls"] = strRes;
                        this.shopify_urls.patchValue(this.shopify_urls.value);
                      }
                      this.router.navigate(['/home/shopify-url']);
                  },
                  error => {
                    //alert errors
          });
  }

  // get email and password and validate
  validate_url(str){
  	// if ":"'s count is 1 then
  	let url_tmp 		= ""; // url tmp variable
  	let res 			  = {}; // return value variable
  	let url_re		 = /^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$/;
  	if ( str ){
  		// correct string type
  		url_tmp 		  = str;
  		if ( url_re.test( url_tmp ) ){
  			res["url"] 	= url_tmp;
  		} else {
  			return false;
  		}
  	} else {
  		// not correct string
  		return false;
  	}
  	return res;
  }

  //split every line from textarea
  split_string(str){
  	let tmp_res 		= str.split("\n"); 	// each item of textarea
  	let res 			= []; 				//result array
  	let res_item_json	= {}; 				//json item of result array {"email":"","password":""}
  	let check_flag		= true; 			//validate all or not
  	let tmp 			= "";
  	for ( let i = 0; i < tmp_res.length; i ++ ){
  		//remove white space
  		tmp = tmp_res[i];
  		if ( tmp == '' ){
  			continue;
  		} else {
  			res_item_json = this.validate_url( tmp )
  			if ( res_item_json ){

  				res.push( res_item_json );
  			} else {

  				check_flag = false;
  				break;
  			}
  		}
  	}
  	//return array if all can be validated.
  	if ( check_flag === false ){

  		return false;
  	} else {
		res = res.filter((value, index, array) => 
     		!array.filter((v, i) => JSON.stringify(value) == JSON.stringify(v) && i < index).length);
  		return res;
  	}
  }

  save_url(){
  	if ( this.shopify_urls.value["shopify_urls"] != "" ) {
  		let res = this.split_string( this.shopify_urls.value["shopify_urls"] )
	  	if ( res ) {
        console.log(res);
	  		this.shopifyurlService.shopifyURL(res)
	            .subscribe(
	                data => {
	                  //clear all forms
	                    data = data.json();
	                    if ( data['stat'] === 'success' ){
	                      //save data succesfully alert
	                      // alert("Shopify URLs are saved.");
                        Swal("Nice!", "Shopify URLs are saved.", "success");
	                      // this.gmail_account.reset();
	                    }
	                    this.router.navigate(['/home/shopify-url']);
	                },
	                error => {
	                  //alert errors
	        });
	  	}
	  	else
	  	{
	  		// alert( "Please input Correct Data." );
        Swal("Wrong!", "Please input Correct Data.", "error");
	  	}	
  	}
  	else
  	{
  		// alert( "Please Input Data first." );
      Swal("Wrong!", "Please Input Data first.", "error");
  	}
  	
  }

  clear_url(){
  	this.shopify_urls.reset();
    Swal("Clear!", "All data is cleared.", "success");
  }

  export_url(){
  	if ( this.shopify_urls.value["shopify_urls"] != "" ) {
  		let res = this.split_string( this.shopify_urls.value["shopify_urls"] )
	  	if ( res ) {
		    new Angular2Csv(res, 'Shopify URLs');
	  	}
	  	else
	  	{
	  		// alert( "Please input Correct Data." );
        Swal("Wrong!", "Please input Correct Data.", "error");
	  	}	
  	}
  	else
  	{
  		// alert( "Please Input Data first." );
      Swal("Wrong!", "Please Input Data first.", "error");
  	}
  }

  import_url(fileInput: any){
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
			for ( let i = 0; i < allTextLines.length; i++ )
			{
				if ( allTextLines[i] != "" )
				{
          console.log(allTextLines[i]);
					data = allTextLines[i].split( ',' );
					if ( data.length == 1 )
					{
						let url_tmp 		= data[0].replace( new RegExp('"','g') , '' );
						let url_re      = /^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$/;
						if ( url_re.test( url_tmp ) )
						{
							exist_flag = 1;
							res_import.push({"url":url_tmp});
						}
						else
						{
							// alert("No Match CSV Data Style");
              Swal("Wrong!", "No Match CSV Data Style.", "error");
							return false;
						}
					}
				}	
			}
			if ( exist_flag == 0 )
			{
				// alert("No Match CSV Data Style");
        Swal("Wrong!", "No Match CSV Data Style.", "error");
				return false;
			}
			else
			{
				let suffix = "";
				let res_text = "";

				//create plain text by using json content
				for ( var i = 0; i < res_import.length; i++ ) {
					suffix = "\n";
					if ( i == ( res_import.length - 1 ) )
					{
						suffix = "";
					}
					res_text = res_text + res_import[i]["url"] + suffix;
				}
				//create plain text by using json content
				this.shopify_urls.value["shopify_urls"] = res_text;
				this.shopify_urls.patchValue(this.shopify_urls.value);
			}
		}
	}
  } 
}

