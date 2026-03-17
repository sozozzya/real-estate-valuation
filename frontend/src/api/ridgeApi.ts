//src/api/ridgeApi.ts

import { api } from "./httpClient"
import type { CalculateRequest, CalculateResponse } from "../types/apiTypes"

export const calculateRidge = async (
  data: CalculateRequest
): Promise<CalculateResponse> => {
  const response = await api.post<CalculateResponse>("/calculate", data)
  return response.data
}

export const downloadReport = async () => {
  const response = await api.get("/report", {
    responseType: "blob"
  })
  return response.data
}