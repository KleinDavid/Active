import { Component } from '@angular/core';
import { BackendService } from './@active/services/backend.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html'
})
export class AppComponent {
  
  constructor(backendService: BackendService) {
    backendService.register();
  }
}
