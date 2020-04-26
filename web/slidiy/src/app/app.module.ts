import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { SettingsComponent } from './settings/settings.component';
import {FormsModule} from '@angular/forms';
import {AuthComponent} from './auth/auth.component';

@NgModule({
  declarations: [
    AppComponent,
    SettingsComponent,
    AuthComponent
  ],
  imports: [
    BrowserModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
