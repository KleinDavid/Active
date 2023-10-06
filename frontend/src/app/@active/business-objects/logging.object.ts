import * as StackTrace from 'stacktrace-js';

export class Logging {

    private static get timeStamp(): string {
        return '[' + (new Date()).toISOString().replace('Z', '').replace('T', ' ') + '] ';
    }

    constructor() { }

    static async log(log: string, data?: any) {
        console.log(await this.getString(log), data);
    }

    static async error(log: string) {
        console.error(await this.getString(log));
    }

    static async getString(log: string): Promise<string> {
        const time = this.timeStamp
        const stack = await this.getStack();

        const consoleWidth = 200;
        const padding = consoleWidth - (time.length + log.length + stack.length);
        return time + ' ' + log + ' '.repeat(padding > 0 ? padding : 1) + stack;
    }

    static async getStack(): Promise<string> {
        // const trace = await StackTrace.get();
        // const stacknumber = 21;
        // if (trace && trace.length >= stacknumber) {
        //     const list = trace[stacknumber].fileName!.split('/') 
        //     return list[list.length-1] + ':' + trace[stacknumber].lineNumber;
        // }
        return '';
    }
}