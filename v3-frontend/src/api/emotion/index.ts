import { request } from "@/utils/service"
import type * as Emotion from "./types/emotion"

/** 获取音频文件 */
export function getEmotionForAudioApi(id: number) {
  return request<Emotion.EmotionDataList>({
    url: "/emotion/",
    method: "get",
    params: {
      audio: id
    }
  })
}
