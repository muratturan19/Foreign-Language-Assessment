import { CLOSING_MESSAGE } from "../constants";

export function normalizeMessageContent(value: string): string {
  return value.replace(/\s+/g, " ").trim();
}

export function isClosingMessageContent(content: string): boolean {
  return normalizeMessageContent(content) === normalizeMessageContent(CLOSING_MESSAGE);
}
