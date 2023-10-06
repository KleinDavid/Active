export class LocalStorage {
    set clientId(clientId: string) {
        localStorage.setItem('clientId', clientId);
    }
    get clientId(): string | null {
        return localStorage.getItem('clientId');
    }
}