export interface AudioData {
  url: string
  orig_file_path: string
  left_file_path: string
  right_file_path: string
  upload_event_id: string
  checked: Boolean
}

export interface AddAudioPartResponse {
  url: string
  user_id: string
  cut_audio_path: string
  start_time: number
  end_time: number
  part_path: string
}

export type GetAudioResponseData = Array<AudioData>

export type AddAudioPartData = {
  user_id: string
  cut_audio_path: string
  start_time: number
  end_time: number
}

export type GetAudioPartResponseData = Array<AddAudioPartResponse>
