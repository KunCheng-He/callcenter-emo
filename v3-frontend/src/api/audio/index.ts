import { request } from "@/utils/service"
import type * as Audio from "./types/audio"

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
  return request<Audio.AudioBinData>({
    url: "/get-audio/",
    method: "get",
    params: {
      path: path
    }
  })
}
