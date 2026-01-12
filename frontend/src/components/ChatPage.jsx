"use client"

import { useState, useCallback } from "react"
import ChatBox from "./ChatBox"
import PlaylistView from "./PlaylistView"
import Sidebar from "./Sidebar"

function ChatPage() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: "bot",
      content:
        "Hey ! Je suis ton assistant musical intelligent. Dis-moi ce que tu fais ou comment tu te sens, et je te compose une playlist parfaite.",
      timestamp: new Date(),
    },
  ])
  const [playlist, setPlaylist] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(true)

  const handleSendMessage = useCallback(async (userMessage) => {
    const newUserMessage = {
      id: Date.now(),
      type: "user",
      content: userMessage,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, newUserMessage])
    setIsLoading(true)

    // Simulation (sera remplacé par l'appel API)
    setTimeout(() => {
      const botResponse = {
        id: Date.now() + 1,
        type: "bot",
        content: `Parfait ! J'analyse "${userMessage}" et je compose ta playlist personnalisée...`,
        timestamp: new Date(),
      }

      setMessages((prev) => [...prev, botResponse])

      setPlaylist({
        title: `Playlist ${userMessage}`,
        description: "Composée par IA selon ton mood",
        mood: "Energique",
        tracks: [
          {
            id: 1,
            title: "Electric Dreams",
            artist: "Synthwave Masters",
            duration: "3:45",
            genre: "Electronic",
            cover: "/album-cover-neon.jpg",
          },
          {
            id: 2,
            title: "Midnight Run",
            artist: "Night Runners",
            duration: "4:12",
            genre: "Dance",
            cover: "/dark-album-cover.png",
          },
          {
            id: 3,
            title: "Pulse",
            artist: "Beat Architects",
            duration: "3:30",
            genre: "EDM",
            cover: "/album-cover-abstract.jpg",
          },
          {
            id: 4,
            title: "Neon Lights",
            artist: "City Sounds",
            duration: "3:58",
            genre: "Synthpop",
            cover: "/album-cover-city.png",
          },
          {
            id: 5,
            title: "Velocity",
            artist: "Tempo Rising",
            duration: "4:05",
            genre: "Electronic",
            cover: "/album-cover-speed.jpg",
          },
        ],
      })

      setIsLoading(false)
    }, 2500)
  }, [])

  const handleSuggestionClick = useCallback(
    (suggestion) => {
      handleSendMessage(suggestion)
    },
    [handleSendMessage],
  )

  return (
    <div className="relative flex h-screen bg-[#050508] overflow-hidden">
      {/* Ambient background */}
      <div className="ambient-bg">
        <div className="ambient-orb ambient-orb-1"></div>
        <div className="ambient-orb ambient-orb-2"></div>
        <div className="ambient-orb ambient-orb-3"></div>
      </div>

      {/* Content */}
      <div className="relative z-10 flex w-full">
        <Sidebar
          isOpen={sidebarOpen}
          onToggle={() => setSidebarOpen(!sidebarOpen)}
          onSuggestionClick={handleSuggestionClick}
        />

        <main className="flex-1 flex flex-col min-w-0">
          {/* Header */}
          <header className="flex items-center justify-between px-6 py-4 glass-strong">
            <div className="flex items-center gap-4">
              <button
                className="p-2.5 rounded-xl glass hover:bg-white/10 transition-all lg:hidden"
                onClick={() => setSidebarOpen(!sidebarOpen)}
              >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="3" y1="6" x2="21" y2="6" />
                  <line x1="3" y1="12" x2="21" y2="12" />
                  <line x1="3" y1="18" x2="21" y2="18" />
                </svg>
              </button>
              <div className="flex items-center gap-3">
                <div className="relative">
                  <div className="w-10 h-10 rounded-xl bg-gradient-accent flex items-center justify-center glow-sm">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                      <path
                        d="M9 18V5l12-2v13"
                        stroke="white"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      />
                      <circle cx="6" cy="18" r="3" stroke="white" strokeWidth="2" />
                      <circle cx="18" cy="16" r="3" stroke="white" strokeWidth="2" />
                    </svg>
                  </div>
                </div>
                <div>
                  <h1 className="text-lg font-semibold tracking-tight">
                    <span className="text-gradient">MusicBot</span>
                    <span className="text-white/60 font-normal ml-1.5 text-sm">AI</span>
                  </h1>
                  <p className="text-xs text-white/40">Powered by Ollama</p>
                </div>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full glass text-xs text-white/60">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                Connecté
              </div>
            </div>
          </header>

          {/* Content */}
          <div className="flex-1 flex gap-6 p-6 overflow-hidden">
            <div className={`flex-1 min-w-0 transition-all duration-500 ${playlist ? "lg:w-3/5" : "w-full"}`}>
              <ChatBox messages={messages} onSendMessage={handleSendMessage} isLoading={isLoading} />
            </div>

            {playlist && (
              <div className="hidden lg:block lg:w-2/5 min-w-[380px] animate-slide-in-right">
                <PlaylistView playlist={playlist} />
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  )
}

export default ChatPage
