import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GmailAccountsComponent } from './gmail-accounts.component';

describe('GmailAccountsComponent', () => {
  let component: GmailAccountsComponent;
  let fixture: ComponentFixture<GmailAccountsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ GmailAccountsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GmailAccountsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
