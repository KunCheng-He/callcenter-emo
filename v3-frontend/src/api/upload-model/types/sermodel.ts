export interface SERModelRequestData {
  name: string
  path: string
}

export type SERModelResponseData = {
  url: number
  name: string
  path: string
}

export type ModelsData = Array<SERModelResponseData>
