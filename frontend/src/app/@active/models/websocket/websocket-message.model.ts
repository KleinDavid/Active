import { v4 as uuidv4 } from 'uuid';

export class WebsocketMessage {
    Id: string = uuidv4();
    Message?: string;
    constructor(message: string) { this.Message = message; }
}
