import { Injectable } from "@angular/core";
import { Websocket } from "../business-objects/websocket.object";


@Injectable({ providedIn: "root" })
export class WebsocketService {
    private websocketList: Websocket[] = [];

    getNewWebsocket(name?: string): Websocket {
        let websocket: Websocket;
        if (name) {
            websocket = new Websocket(name);
        } else {
            websocket = new Websocket();
        }
        this.registerWebsocket(websocket);
        return websocket;
    }

    registerWebsocket(websocket: Websocket): void {
        if (!websocket.id) {
            // websocket.id = this.generateWebsocketId();
            this.websocketList.push(websocket);
        }
    }

    destroyWebsocket(id: number): void {
        this.getWebsocketById(id)?.destroy();
        this.websocketList = this.websocketList.filter(websocket => websocket.id !== id);
    }

    getWebsocketById(id: number): Websocket | undefined {
        return this.websocketList.find(websocket => websocket.id === id);
    }

    getWebsocketByName(name: string): Websocket | undefined {
        return this.websocketList.find(websocket => websocket.name === name);
    }
}