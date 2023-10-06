import {default as jsonData} from '../../../assets/config.json';

export class Config {
    static HTTP: string = jsonData.http;
    static WEBSOCKET: string = jsonData.websocket;
    static SERVER_URL: string = jsonData.serverUrl;
}