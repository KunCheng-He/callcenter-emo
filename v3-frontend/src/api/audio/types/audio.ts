export interface AudioData {
  url: string
  orig_file_path: string
  left_file_path: string
  right_file_path: string
  upload_event_id: string
  checked: Boolean
}

export type GetAudioResponseData = Array<AudioData>
