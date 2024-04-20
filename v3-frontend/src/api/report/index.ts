import { request } from "@/utils/service"
import * as Report from "./types/report"

/** 获取质检报告 */
export function getReportApi() {
  return request<Report.ReportDataList>({
    url: "/report/",
    method: "get"
  })
}
