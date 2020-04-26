import { Component, OnInit } from '@angular/core';
import {HttpClient} from '@angular/common/http';

@Component({
  selector: 'app-auth',
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.component.css']
})
export class AuthComponent implements OnInit {

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
  }

  getInfo() {
    const response = this.http.get('https://cnclibwebapi.azurewebsites.net/api/Info');
    response.subscribe((data) => console.log(data));
  }

  auth(id: string) {
    const response = this.http.get('https://cnclibwebapi.azurewebsites.net/' + id);
    response.subscribe((data) => console.log(data));
  }

  getUsers() {
    const response = this.http.get('https://cnclibwebapi.azurewebsites.net/api/User');
    response.subscribe((data) => console.log(data));
  }

}
