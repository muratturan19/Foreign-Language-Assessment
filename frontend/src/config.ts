export const APP_CONFIG = {
  MODE: (import.meta.env.VITE_APP_MODE as 'PORTAL' | 'STANDALONE') || 'STANDALONE',
  IS_PORTAL: import.meta.env.VITE_APP_MODE === 'PORTAL',
};
