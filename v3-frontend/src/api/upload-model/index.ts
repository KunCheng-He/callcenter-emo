import { request } from "@/utils/service"
import type * as SERModel from "./types/sermodel"

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
