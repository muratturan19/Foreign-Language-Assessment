/**
 * Encodes a string to base64, properly handling Unicode characters
 * @param str - The string to encode
 * @returns The base64-encoded string
 */
export function encodeStringToBase64(str: string): string {
  // Convert the string to UTF-8 bytes, then to base64
  // This handles Unicode characters correctly
  const utf8Bytes = new TextEncoder().encode(str);
  let binary = '';
  for (let i = 0; i < utf8Bytes.length; i++) {
    binary += String.fromCharCode(utf8Bytes[i]);
  }
  return btoa(binary);
}

/**
 * Decodes a base64 string back to the original string
 * @param base64 - The base64-encoded string
 * @returns The decoded string
 */
export function decodeBase64ToString(base64: string): string {
  const binary = atob(base64);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i);
  }
  return new TextDecoder().decode(bytes);
}
