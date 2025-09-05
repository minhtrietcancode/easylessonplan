/**
 * Custom API Error class
 */
export class APIError extends Error {
    constructor(message, status, errorCode, details) {
        super(message);
        this.name = 'APIError';
        this.status = status;
        this.errorCode = errorCode;
        this.details = details;
    }
}
