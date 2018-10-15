import { CheckoutProfileComponent } from '../checkout-profile/checkout-profile.component';
import { GmailAccountsComponent } from '../gmail-accounts/gmail-accounts.component';
import { NgModule} from '@angular/core';
import { CommonModule} from '@angular/common';
import { Routes, RouterModule} from '@angular/router';
import { AuthGuard } from '../_guards/auth.guard';
import { Error404Component} from '../shared/components/error404/error404.component';
import { TaskCreatorComponent} from '../task-creator/task-creator.component';
import { DashboardComponent} from '../dashboard/dashboard.component';
import { SettingsComponent} from '../settings/settings.component';
import { ProxiesComponent} from '../proxies/proxies.component';
import { ShopifyURLComponent} from '../shopify-url/shopify-url.component';
import { HomeComponent} from './home.component';

import { HeaderComponent} from '../shared/components/header/header.component';
import { FooterComponent} from '../shared/components/footer/footer.component';
import { SidebarComponent} from '../shared/components/sidebar/sidebar.component';

import {
  MatInputModule,
  MatSortModule,
  MatFormFieldModule,
  MatPaginatorModule,
  MatTableModule,
  MatIconModule,
  MatButtonModule,
  MatButtonToggleModule,
  MatOptionModule,
  MatSelectModule,
  MatGridListModule,
  MatCardModule,
  MatListModule,
  MatDatepickerModule,
  MatCheckboxModule,
  MatNativeDateModule
} from '@angular/material';

import { FormsModule, ReactiveFormsModule} from '@angular/forms';

const appRoutes : Routes = [
	  {path: 'home', component: HomeComponent, children:[ 
		  {path: 'dashboard', component: DashboardComponent}, 
		  {path: 'task-creator', component: TaskCreatorComponent}, 
		  {path: 'checkout-profile', component: CheckoutProfileComponent}, 
		  {path: 'proxies', component: ProxiesComponent}, 
		  {path: 'settings', component: SettingsComponent}, 
		  {path: 'gmail-accounts', component: GmailAccountsComponent}, 
		  {path: 'shopify-url', component: ShopifyURLComponent},
		  {path: '404', component: Error404Component}, 
		  {path: '', redirectTo: '/home/dashboard', pathMatch: 'full'},
		  {path: '**', redirectTo: '/404'}
		], canActivate: [AuthGuard]}
 ];

@NgModule({
  imports: [
  	RouterModule.forChild(appRoutes),
  	FormsModule,
  	ReactiveFormsModule,
	MatInputModule,
	MatSortModule,
	MatFormFieldModule,
	MatPaginatorModule,
	MatTableModule,
	MatIconModule,
	MatButtonModule,
	MatButtonToggleModule,
	MatOptionModule,
	MatSelectModule,
	MatGridListModule,
	MatCardModule,
	MatListModule,
	MatDatepickerModule,
	MatCheckboxModule,
	MatNativeDateModule
  ],
  exports: [
  RouterModule,
  ],
  declarations: [
	    HomeComponent,
		DashboardComponent,
		TaskCreatorComponent,
		SettingsComponent,
		ProxiesComponent,
		CheckoutProfileComponent,
		GmailAccountsComponent,
		ShopifyURLComponent,
		Error404Component,
		HeaderComponent,
		FooterComponent,
		SidebarComponent
  	]
})
export class HomeModule {}