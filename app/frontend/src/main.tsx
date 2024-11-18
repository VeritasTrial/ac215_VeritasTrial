/**
 * @file main.tsx
 *
 * The main entry point for the application.
 */

import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { App } from "./App";
import "@radix-ui/themes/styles.css";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
