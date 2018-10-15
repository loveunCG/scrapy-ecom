import { AppRoutingModule } from './app-routing/app-routing.module';
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { AuthGuard } from './_guards/auth.guard';
import { HttpModule } from '@angular/http';
import { AppComponent } from './app.component';
import { HttpClientModule} from '@angular/common/http';
import { FormsModule, ReactiveFormsModule} from '@angular/forms';
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

import { LoginComponent } from './login/login.component';
// import { HomeModule } from './home/home.module';
import { AuthService } from './service/auth.service';
import { CheckoutService } from './service/checkout.service';
import { CreatetaskService } from './service/createtask.service';
import { GmailaccountService } from './service/gmailaccount.service';
import { ProxiesService } from './service/proxies.service';
import { ShopifyurlService } from './service/shopifyurl.service';
import {CdkTableModule} from '@angular/cdk/table';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent
  ],
  imports: [
    BrowserModule,
    // HttpClientModule,
    HttpModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    MatTableModule,
    MatInputModule,
    MatPaginatorModule,
    MatSortModule,
    MatFormFieldModule,
    MatIconModule,
    MatButtonModule,
    MatOptionModule,
    MatSelectModule,
    MatGridListModule,
    MatCardModule,
    MatListModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatCheckboxModule,
    FormsModule,
    ReactiveFormsModule,
    // HomeModule
  ],
  providers: [
    AuthService,
    AuthGuard,
    CheckoutService,
    CreatetaskService,
    GmailaccountService,
    ProxiesService,
    ShopifyurlService
  ],
  bootstrap: [AppComponent]
})
export class AppModule {}