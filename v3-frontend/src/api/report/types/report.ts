export interface ReportData {
  frame_num: number
  left_emotions: number[]
  right_emotions: number[]
  orig_file_path: string
  left_file_path: string
  right_file_path: string
  upload_time: string
  username: string
}

export type ReportDataList = Array<ReportData>
