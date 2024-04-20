export interface UploadRequestData {
  cs_user_id: string
  ser_model_id: string
  file: string
}

export type UploadResponseData = {
  id: number
  cs_user_id: string
  ser_model_id: string
  upload_time: string
  file: string
}
