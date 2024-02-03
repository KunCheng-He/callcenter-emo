import { request } from "@/utils/service"
import * as Ding from "./types/ding"

/** 添加剪辑音频片段 */
export function addDingLabelApi(data: Ding.AddDingLabelData) {
  return request<Ding.DingLabelData>({
    url: "/ding-label/",
    method: "post",
    data: data
  })
}
