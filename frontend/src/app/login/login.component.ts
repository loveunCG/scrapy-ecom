import { Component, OnInit } from '@angular/core';
import { AuthService } from '../service/auth.service';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})

export class LoginComponent implements OnInit {
	model: any = {};

	constructor(private authservice: AuthService, private router: Router) {}

	ngOnInit() {
	}

	login(){
        this.authservice.login(this.model.username, this.model.password)
            .subscribe(
                data => {
                    this.router.navigate(['/home']);
                },
                error => {
                    // this.alertService.error(error);
                    // this.loading = false;
        });
	}

}
