import { NgModule} from '@angular/core';
import { Routes, RouterModule} from '@angular/router';
import { LoginComponent } from '../login/login.component';
import { HomeModule } from '../home/home.module';

const appRoutes : Routes = [  
  {path: 'login', component: LoginComponent, data: {title: 'Login', breadcrumb: 'Login' } },
  {path: 'home', loadChildren: 'app/home/home.module#HomeModule'}, 
  {path: '', redirectTo: '/login', pathMatch: 'full', data: {title: 'Login' } }  
  ];

@NgModule({
  imports: [
  RouterModule.forRoot(appRoutes),
  HomeModule
  ],
  exports: [RouterModule],
  declarations: []
})
export class AppRoutingModule {}