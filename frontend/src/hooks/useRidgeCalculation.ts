//ars/hooks/useRidgeCalculation.ts

import { useState } from "react"
import { calculateRidge } from "../api/ridgeApi"
import { normalizeError } from "../utils/normalizeError"
import type { CalculateRequest, CalculateResponse } from "../types/apiTypes"

export const useRidgeCalculation = () => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const execute = async (
    data: CalculateRequest
  ): Promise<CalculateResponse | null> => {
    try {
      setLoading(true)
      setError(null)

      const res = await calculateRidge(data)
      return res
    } catch (err: unknown) {
      setError(normalizeError(err))
      return null
    } finally {
      setLoading(false)
    }
  }

  return { loading, error, execute }
}