export function formatDateTime(value) {
  if (!value) {
    return "Not available";
  }

  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return String(value);
  }
  return date.toLocaleString();
}

export function formatLabel(value) {
  if (!value) {
    return "Not available";
  }
  return String(value)
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

export function toDisplayList(value) {
  if (value === null || value === undefined || value === "") {
    return [];
  }
  if (Array.isArray(value)) {
    return value.map((item) =>
      typeof item === "object" ? JSON.stringify(item) : String(item),
    );
  }
  if (typeof value === "object") {
    return Object.entries(value).map(
      ([key, item]) =>
        `${formatLabel(key)}: ${
          typeof item === "object" ? JSON.stringify(item) : String(item)
        }`,
    );
  }
  return [String(value)];
}
