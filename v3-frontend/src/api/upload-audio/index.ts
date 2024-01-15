import { request } from "@/utils/service"
import type * as Upload from "./types/upload"

export function uploadApi(formdata: Upload.UploadRequestData) {
  return request<Upload.UploadResponseData>({
    url: "/upload/",
    method: "post",
    formdata,
    headers: {
      "Content-Type": "multipart/form-data"
    }
  })
}
