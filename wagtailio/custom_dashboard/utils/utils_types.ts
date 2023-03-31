export interface IObject<T> {
    [key: string]: T
}

export interface IImageBase64 {
    url: string
    base64: string
}

export interface IError {
    message: string
}