import { request } from "@/utils/service"
import type * as SERModel from "./types/sermodel"

/** 上传语音情感识别模型API */
export function serModelApi(formdata: SERModel.SERModelRequestData) {
  return request<SERModel.SERModelResponseData>({
    url: "/ser-model/",
    method: "post",
    data: formdata,
    headers: {
      "Content-Type": "multipart/form-data"
    }
  })
}

/** 获取语音情感识别模型API */
export function getSERModelApi() {
  return request<SERModel.ModelsData>({
    url: "/ser-model/",
    method: "get"
  })
}
