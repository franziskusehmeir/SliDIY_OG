import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.css']
})
export class SettingsComponent implements OnInit {
  range: number;

  constructor() { }

  ngOnInit(): void {
  }


  readRange(range) {
    console.log(range);
  }

}
