import React, { useEffect, useMemo, useState } from "react";
import ReactDOM from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ChatPanel } from "./components/ChatPanel";
import "./index.css";

const queryClient = new QueryClient();

const THEME_STORAGE_KEY = "fla-theme";

type Theme = "light" | "dark";

function App() {
  const getInitialTheme = useMemo<() => Theme>(() => {
    return () => {
      if (typeof window === "undefined") {
        return "light";
      }
      const stored = window.localStorage.getItem(THEME_STORAGE_KEY);
      if (stored === "light" || stored === "dark") {
        return stored;
      }
      return "light";
    };
  }, []);

  const [theme, setTheme] = useState<Theme>(getInitialTheme);

  useEffect(() => {
    if (typeof window === "undefined" || typeof document === "undefined") return;
    const root = document.documentElement;
    root.classList.toggle("dark", theme === "dark");
    root.dataset.theme = theme;
    try {
      window.localStorage.setItem(THEME_STORAGE_KEY, theme);
    } catch {
      // ignore storage failures
    }
  }, [theme]);

  const toggleTheme = () => {
    setTheme((prev) => (prev === "dark" ? "light" : "dark"));
  };

  return (
    <div
      className={`min-h-screen transition-colors duration-300 ${
        theme === "dark"
          ? "bg-[#071525] text-slate-100"
          : "bg-[#F0F4F8] text-slate-900"
      }`}
    >
      <div className="mx-auto flex max-w-6xl flex-col gap-6 px-4 py-10">
        <header className="flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-4">
            <img
              src={theme === "dark" ? "/talksim_logo_dark.svg" : "/talksim_logo.svg"}
              alt="TalkSim"
              className="h-20 w-auto"
            />
          </div>
          <button
            type="button"
            onClick={toggleTheme}
            className="inline-flex items-center gap-1.5 rounded-full px-3 py-1.5 text-xs text-slate-400 transition hover:text-slate-600 dark:text-slate-500 dark:hover:text-slate-300"
            aria-label="Tema değiştir"
          >
            {theme === "dark" ? "Açık Tema" : "Koyu Tema"}
          </button>
        </header>
        <ChatPanel />
        <footer className="text-center text-xs text-slate-500 dark:text-slate-400">
          İngilizce konuşma pratiği için tasarlandı · Tüm yönlendirmeler ve değerlendirmeler Türkçe arayüz üzerinden sunulur
        </footer>
      </div>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </React.StrictMode>
);
