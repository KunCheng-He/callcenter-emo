export interface EmotionData {
  url: string
  audio_id: string
  recognition_time: string
  frame_num: number
  left_emotions: number[]
  right_emotions: number[]
}

export type EmotionDataList = Array<EmotionData>
