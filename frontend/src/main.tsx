//src/main.tsx

import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import { ErrorBoundary } from "./components/ErrorBoundary";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </StrictMode>,
);

if (import.meta.env.PROD) {
  window.addEventListener("error", () => {
    // Sentry.captureException(event.error)
  });

  window.addEventListener("unhandledrejection", () => {
    // Sentry.captureException(event.reason)
  });
}
