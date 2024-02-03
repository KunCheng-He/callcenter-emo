export interface DingLabelData {
  url: string
  audio_part_id: string
  audio_role: string
  emotion_label: number
  text: string
  pleasure: number
  action: number
}

export type AddDingLabelData = {
  audio_part_id: string
  audio_role: string
  emotion_label: number
  text: string
  pleasure: number
  action: number
}
