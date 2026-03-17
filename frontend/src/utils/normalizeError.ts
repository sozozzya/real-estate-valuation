//src/utils/normalizeError.ts

import axios from "axios";

export const normalizeError = (err: unknown): string => {
  if (axios.isAxiosError(err)) {
    const data = err.response?.data;

    if (typeof data === "string") {
      return data;
    }

    if (data?.detail) {
      return data.detail;
    }

    if (data?.message) {
      return data.message;
    }

    if (data?.error) {
      return data.error;
    }

    return "Ошибка сервера";
  }

  if (err instanceof Error) {
    return err.message;
  }

  return "Неизвестная ошибка";
};
