import { HttpClient, HttpHandler, HttpHeaders, HttpXhrBackend } from "@angular/common/http";
import { throwError } from "rxjs";
import { catchError, map, tap } from 'rxjs/operators'

const httpClient = new HttpClient(new HttpXhrBackend({
    build: () => new XMLHttpRequest()
}));


export class ClientMetaData {

    static get Ip(): Promise<string | undefined> {
        return this.getIp();
    }

    static getIp(): Promise<string | undefined> {
        return httpClient.get<any>('https://geolocation-db.com/json/', { responseType: 'json' }).pipe(map(res => res['IPv4'])).toPromise();
    }
}