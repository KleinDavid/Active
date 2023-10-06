import { Injectable } from "@angular/core";
import { Websocket } from "../business-objects/websocket.object";
import { Config } from "../business-objects/config.object";


@Injectable({ providedIn: "root" })
export class BackendService {

    private websocket = new Websocket('backend-connection');

    async register(): Promise<boolean> {
        if (await this.websocket.connect(Config.WEBSOCKET + Config.SERVER_URL)) {
            const answer = await this.websocket.sendRequest('register');
        }
        return true;
    }
}