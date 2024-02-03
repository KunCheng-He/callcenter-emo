import { request } from "@/utils/service"
import * as Audio from "./types/audio"

/** 获取未审计音频 */
export function getNOCheckAudioApi() {
  return request<Audio.GetAudioResponseData>({
    url: "/audio/",
    method: "get",
    params: {
      checked: "False"
    }
  })
}

/** 获取音频文件 */
export function getAudioApi(path: string) {
  return request<Blob>({
    url: "/get-audio/",
    method: "get",
    params: {
      path: path
    }
  })
}

/** 更新音频文件数据项 */
export function updateAudioCheckedApi(id: number) {
  return request<Audio.AudioData>({
    url: `/audio/${id}/`,
    method: "patch",
    data: {
      checked: true
    }
  })
}

/** 添加剪辑音频片段 */
export function addAudioPartApi(data: Audio.AddAudioPartData) {
  return request<Audio.AddAudioPartResponse>({
    url: "/audio-part/",
    method: "post",
    data: data
  })
}
