"use client"

import { useState, useCallback, useEffect } from "react"
import ChatBox from "./ChatBox"
import PlaylistView from "./PlaylistView"
import Sidebar from "./Sidebar"
import AudioPlayer from "./AudioPlayer"
import { sendMessage, checkHealth } from "../services/api"

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
  const [backendStatus, setBackendStatus] = useState("checking")
  
  const [currentTrack, setCurrentTrack] = useState(null)
  const [currentTrackIndex, setCurrentTrackIndex] = useState(null)

  useEffect(() => {
    const checkBackend = async () => {
      try {
        const health = await checkHealth()
        setBackendStatus(health.status === "ok" || health.status === "degraded" ? "connected" : "error")
      } catch {
        setBackendStatus("offline")
      }
    }
    checkBackend()
  }, [])

  const handleSendMessage = useCallback(async (userMessage) => {
    const newUserMessage = {
      id: Date.now(),
      type: "user",
      content: userMessage,
      timestamp: new Date(),
    }
  
    setMessages((prev) => [...prev, newUserMessage])
    setIsLoading(true)
  
    try {
      const response = await sendMessage(userMessage, messages.map(m => ({
        role: m.type === "user" ? "user" : "assistant",
        content: m.content
      })))
  
      const botResponse = {
        id: Date.now() + 1,
        type: "bot",
        content: response.response || "J'ai créé ta playlist !",
        timestamp: new Date(),
      }
  
      setMessages((prev) => [...prev, botResponse])
  
      if (response.playlist && Array.isArray(response.playlist.playlist) && response.playlist.playlist.length > 0) {
        const backendPlaylist = response.playlist
        
        const sportToMood = {
          "course_a_pied": "Énergique",
          "boxe": "Intense",
          "musculation": "Motivant",
          "marche_a_pied": "Relaxant",
          "echauffement": "Doux"
        }
  
        const sportToGenre = {
          "course_a_pied": "Running",
          "boxe": "Power",
          "musculation": "Workout",
          "marche_a_pied": "Ambient",
          "echauffement": "Chill"
        }
  
        const newPlaylist = {
          title: `Playlist ${backendPlaylist.sport.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}`,
          description: `Composée par IA • ${backendPlaylist.track_count} morceaux • ${backendPlaylist.bpm_range} BPM`,
          mood: sportToMood[backendPlaylist.sport] || "Énergique",
          tracks: backendPlaylist.playlist.map((track, index) => ({
            id: index + 1,
            title: track.title || "Titre inconnu",
            artist: track.artist || track.creator || "Artiste inconnu",
            duration: track.duration || "3:00",
            genre: sportToGenre[backendPlaylist.sport] || "Music",
            cover: `/album-cover-${index % 5}.jpg`,
            identifier: track.identifier,
            preview_url: track.preview_url,
            stream_url: track.stream_url || track.preview_url
          }))
        }
        
        setPlaylist(newPlaylist)
        
        console.log("✅ Playlist définie avec", backendPlaylist.playlist.length, "tracks")
      }
  
      setIsLoading(false)
    } catch (error) {
      console.error("Erreur:", error)
      
      const errorMessage = {
        id: Date.now() + 1,
        type: "bot",
        content: `❌ Erreur: ${error.message}\n\n💡 Assure-toi que le backend est lancé sur http://localhost:8000`,
        timestamp: new Date(),
      }
      
      setMessages((prev) => [...prev, errorMessage])
      setIsLoading(false)
    }
  }, [messages])

  const handleSuggestionClick = useCallback(
    (suggestion) => {
      handleSendMessage(suggestion)
    },
    [handleSendMessage],
  )

  const handlePlayTrack = useCallback((track, index) => {
    setCurrentTrack(track)
    setCurrentTrackIndex(index)
  }, [])

  const handleNextTrack = useCallback(() => {
    if (!playlist || currentTrackIndex === null) return
    
    const nextIndex = (currentTrackIndex + 1) % playlist.tracks.length
    setCurrentTrack(playlist.tracks[nextIndex])
    setCurrentTrackIndex(nextIndex)
  }, [playlist, currentTrackIndex])

  const handlePreviousTrack = useCallback(() => {
    if (!playlist || currentTrackIndex === null) return
    
    const prevIndex = currentTrackIndex === 0 ? playlist.tracks.length - 1 : currentTrackIndex - 1
    setCurrentTrack(playlist.tracks[prevIndex])
    setCurrentTrackIndex(prevIndex)
  }, [playlist, currentTrackIndex])

  const handleClosePlayer = useCallback(() => {
    setCurrentTrack(null)
    setCurrentTrackIndex(null)
  }, [])

  return (
    <div className="relative flex h-screen bg-[#050508] overflow-hidden">
      <div className="ambient-bg">
        <div className="ambient-orb ambient-orb-1"></div>
        <div className="ambient-orb ambient-orb-2"></div>
        <div className="ambient-orb ambient-orb-3"></div>
      </div>

      <div className="relative z-10 flex w-full">
        <Sidebar
          isOpen={sidebarOpen}
          onToggle={() => setSidebarOpen(!sidebarOpen)}
          onSuggestionClick={handleSuggestionClick}
        />

        <main className="flex-1 flex flex-col min-w-0">
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
                <span className={`w-2 h-2 rounded-full ${
                  backendStatus === "connected" ? "bg-emerald-400 animate-pulse" :
                  backendStatus === "checking" ? "bg-yellow-400 animate-pulse" :
                  "bg-red-400"
                }`}></span>
                {backendStatus === "connected" ? "Connecté" :
                 backendStatus === "checking" ? "Vérification..." :
                 "Déconnecté"}
              </div>
            </div>
          </header>

          <div className={`flex-1 flex gap-6 p-6 overflow-hidden ${currentTrack ? 'pb-24' : ''}`}>
            <div className={`flex-1 min-w-0 transition-all duration-500 ${playlist ? "lg:w-3/5" : "w-full"}`}>
              <ChatBox messages={messages} onSendMessage={handleSendMessage} isLoading={isLoading} />
            </div>

            {playlist && (
              <div className="hidden lg:block lg:w-2/5 min-w-[380px] animate-slide-in-right">
                <PlaylistView 
                  playlist={playlist} 
                  onPlayTrack={handlePlayTrack}
                  currentTrackId={currentTrack?.id}
                />
              </div>
            )}
          </div>
        </main>
      </div>

      {currentTrack && (
        <AudioPlayer
          currentTrack={currentTrack}
          onNext={handleNextTrack}
          onPrevious={handlePreviousTrack}
          onClose={handleClosePlayer}
        />
      )}
    </div>
  )
}

export default ChatPage
