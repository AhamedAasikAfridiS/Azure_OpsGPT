import { Check, Copy } from "lucide-react";
import { useState } from "react";

function fallbackCopy(text) {
  const textarea = document.createElement("textarea");
  textarea.value = text;
  textarea.setAttribute("readonly", "");
  textarea.style.position = "fixed";
  textarea.style.opacity = "0";
  document.body.appendChild(textarea);
  textarea.select();
  const success = document.execCommand("copy");
  document.body.removeChild(textarea);
  return success;
}

export default function CopyButton({ text, label = "Copy" }) {
  const [state, setState] = useState("idle");

  async function handleCopy() {
    try {
      if (navigator.clipboard?.writeText) {
        await navigator.clipboard.writeText(text);
      } else if (!fallbackCopy(text)) {
        throw new Error("fallback copy failed");
      }
      setState("copied");
    } catch {
      setState("failed");
    } finally {
      window.setTimeout(() => setState("idle"), 1800);
    }
  }

  const copied = state === "copied";
  const failed = state === "failed";

  return (
    <button
      aria-label={`${label} webhook URL`}
      className={copied ? "primary-button compact-button" : "secondary-button compact-button"}
      onClick={handleCopy}
      type="button"
    >
      {copied ? <Check size={16} aria-hidden="true" /> : <Copy size={16} aria-hidden="true" />}
      {copied ? "Copied" : failed ? "Copy failed" : label}
    </button>
  );
}
