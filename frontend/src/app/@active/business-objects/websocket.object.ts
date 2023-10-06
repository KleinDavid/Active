import { Subject, Observable, Observer, Subscription } from "rxjs";
import { WebsocketMessage } from "../models/websocket/websocket-message.model";
import { WebsocketConnectionState } from "../enumns/websocket-connection-state.enum";
import { Logging } from "./logging.object";

export class Websocket {
    get connectionState(): WebsocketConnectionState | undefined { return this.socket?.readyState; };
    id?: number;
    name?: string;
    onMessage: any;

    url?: string;

    private socket?: WebSocket;
    private receiveSubjects: Map<string, Subject<WebsocketMessage>> = new Map<string, Subject<WebsocketMessage>>();

    constructor(name?: string) {
        if (name) { this.name = name; }
    }

    async connect(url: string): Promise<boolean> {
        this.url = url ? url : this.url;
        if (!this.url) {
            Logging.error('No Websocket Url is set.');
        }
        Logging.log('Connecting Websocket: ' + url);
        const res = await this.buildConnection(url);
        res ?
            Logging.log('Connected to Websocket: ' + url) :
            Logging.error('Connection to websocket failed: ' + url);
        return res;
    }

    sendRequest(messageString: string): Promise<WebsocketMessage> {
        const message = new WebsocketMessage(messageString);

        const subject = new Subject<WebsocketMessage>();
        this.receiveSubjects.set(message.Id, subject);
        this.pushMessage(message);

        return new Promise<WebsocketMessage>((resolve, rejects) => {
            subject.subscribe(message => { 
                resolve(message); 
                subject.complete(); 
                this.receiveSubjects.delete(message.Id) })
        });
    }

    onMessageReceive(event: MessageEvent): void {
        
        const data: WebsocketMessage = JSON.parse(event.data);
        Logging.log('Massage received: ', data);
        if (this.onMessage) { this.onMessage(event) };
        this.receiveSubjects.get(data.Id)?.next(data);
        this.receiveSubjects.delete(data.Id);
    }

    private pushMessage(message: any): void {
        if (this.socket?.readyState === WebsocketConnectionState.OPEN) {
            this.socket?.send(JSON.stringify(message));
            Logging.log('Send Message: ', message);
        } else {
            Logging.error('WebSocket is not open. Cannot send message. ' + this.url);
        }

    }

    private buildConnection(url?: string): Promise<boolean> {
        const subject = new Subject<boolean>();

        this.socket = new WebSocket(this.url!);

        this.socket.onopen = () => subject.next(true);
        this.socket.onclose = () => subject.next(false);
        this.socket.onmessage = this.onMessageReceive.bind(this);

        return new Promise<boolean>((resolve, reject) => {
            subject.subscribe(value => { resolve(value); subject.complete(); });
        });
    }
}
