import { Component } from '@angular/core';
import { BackendService } from './@active/services/backend.service';
import { ClientMetaData } from './@active/business-objects/client-meta-data.object';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html'
})
export class AppComponent {
  
  constructor(backendService: BackendService) {
    backendService.register();
    this.initActive();
  }

  async initActive(): Promise<void> {
    
    const IP = await ClientMetaData.Ip;
    console.log('david', IP);
  }
}
