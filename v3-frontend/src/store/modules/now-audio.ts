import { ref } from "vue"
import { defineStore } from "pinia"
import { type AudioData } from "@/api/audio/types/audio"

export const useNowAudioStore = defineStore("now-audio", () => {
  /** 当前未审核音频 */
  const noCheckAudio = ref<AudioData | null>(null)

  /** 所有音频请求后端url */
  const oriAudioUrl = ref<string>("")
  const leftAudioUrl = ref<string>("")
  const rightAudioUrl = ref<string>("")

  /** 音频对应的情感 */
  const frameNum = ref<number>(0)
  const leftEmotion = ref<number[] | null>(null)
  const rightEmotion = ref<number[] | null>(null)

  return {
    noCheckAudio,
    oriAudioUrl,
    leftAudioUrl,
    rightAudioUrl,
    frameNum,
    leftEmotion,
    rightEmotion
  }
})
