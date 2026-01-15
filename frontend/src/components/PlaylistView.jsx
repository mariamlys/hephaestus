"use client"

import { useState } from "react"

function PlaylistView({ playlist }) {
  const [playingTrack, setPlayingTrack] = useState(null)
  const [hoveredTrack, setHoveredTrack] = useState(null)

  const handlePlayTrack = (trackId) => {
    setPlayingTrack(playingTrack === trackId ? null : trackId)
  }

  const getGradientStyle = (index) => {
    const colors = [
      ["#6366f1", "#9333ea"],
      ["#ec4899", "#e11d48"],
      ["#06b6d4", "#2563eb"],
      ["#f59e0b", "#ea580c"],
      ["#10b981", "#14b8a6"],
      ["#8b5cf6", "#9333ea"],
    ]
    const [from, to] = colors[index % colors.length]
    return { background: `linear-gradient(135deg, ${from}, ${to})` }
  }

  const totalDuration = playlist.tracks.reduce((acc, track) => {
    const duration = track.duration
    
    // Ignorer les durées "N/A"
    if (!duration || duration === "N/A") {
      return acc
    }
    
    const parts = duration.split(":")
    if (parts.length !== 2) {
      return acc
    }
    
    const min = Number(parts[0]) || 0
    const sec = Number(parts[1]) || 0
    return acc + min * 60 + sec
  }, 0)
  
  const formatTotalDuration = (seconds) => {
    if (seconds === 0) return "? min"
    const min = Math.floor(seconds / 60)
    return min + " min"
  }

  return (
    <div className="h-full glass rounded-2xl overflow-hidden flex flex-col border-gradient">
      <div className="relative p-6 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-indigo-600/30 via-purple-600/20 to-pink-600/30"></div>
        <div className="absolute inset-0 bg-gradient-to-t from-[#111118] via-transparent to-transparent"></div>

        <div className="relative">
          <div className="flex items-start gap-4">
            <div className="w-20 h-20 rounded-xl bg-gradient-accent flex items-center justify-center shadow-2xl animate-pulse-glow">
              <svg width="36" height="36" viewBox="0 0 24 24" fill="none">
                <path d="M9 18V5l12-2v13" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                <circle cx="6" cy="18" r="3" stroke="white" strokeWidth="2" />
                <circle cx="18" cy="16" r="3" stroke="white" strokeWidth="2" />
              </svg>
            </div>
            <div className="flex-1 min-w-0">
              <span className="inline-block px-2 py-0.5 rounded-full bg-white/10 text-[10px] font-medium text-white/70 uppercase tracking-wider mb-2">
                Playlist IA
              </span>
              <h2 className="text-xl font-bold text-white truncate">{playlist.title}</h2>
              <p className="text-sm text-white/50 mt-1">{playlist.description}</p>
            </div>
          </div>

          <div className="flex items-center gap-6 mt-5">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-white/10 flex items-center justify-center">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M9 18V5l12-2v13" />
                  <circle cx="6" cy="18" r="3" />
                  <circle cx="18" cy="16" r="3" />
                </svg>
              </div>
              <div>
                <p className="text-lg font-bold text-white">{playlist.tracks.length}</p>
                <p className="text-[10px] text-white/40 uppercase">Titres</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-white/10 flex items-center justify-center">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="10" />
                  <polyline points="12 6 12 12 16 14" />
                </svg>
              </div>
              <div>
                <p className="text-lg font-bold text-white">{formatTotalDuration(totalDuration)}</p>
                <p className="text-[10px] text-white/40 uppercase">Durée</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-white/10 flex items-center justify-center">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z" />
                </svg>
              </div>
              <div>
                <p className="text-lg font-bold text-white">{playlist.mood}</p>
                <p className="text-[10px] text-white/40 uppercase">Mood</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto px-4 pb-4">
        <div className="space-y-1">
          {playlist.tracks.map((track, index) => {
            const isPlaying = playingTrack === track.id
            const isHovered = hoveredTrack === track.id

            return (
              <div
                key={track.id}
                onClick={() => handlePlayTrack(track.id)}
                onMouseEnter={() => setHoveredTrack(track.id)}
                onMouseLeave={() => setHoveredTrack(null)}
                className={
                  isPlaying
                    ? "group flex items-center gap-3 px-3 py-2.5 rounded-xl cursor-pointer transition-all duration-200 bg-gradient-to-r from-indigo-500/20 to-purple-500/20 border border-indigo-500/30"
                    : "group flex items-center gap-3 px-3 py-2.5 rounded-xl cursor-pointer transition-all duration-200 hover:bg-white/5"
                }
              >
                <div className="w-8 h-8 flex items-center justify-center text-sm">
                  {isPlaying ? (
                    <div className="flex items-end gap-0.5 h-4">
                      <span
                        className="w-1 bg-indigo-400 rounded-full animate-bounce-bar"
                        style={{ height: "60%" }}
                      ></span>
                      <span
                        className="w-1 bg-purple-400 rounded-full animate-bounce-bar"
                        style={{ height: "100%", animationDelay: "0.15s" }}
                      ></span>
                      <span
                        className="w-1 bg-pink-400 rounded-full animate-bounce-bar"
                        style={{ height: "40%", animationDelay: "0.3s" }}
                      ></span>
                    </div>
                  ) : isHovered ? (
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" className="text-white">
                      <polygon points="5,3 19,12 5,21" />
                    </svg>
                  ) : (
                    <span className="text-white/30 font-medium">{index + 1}</span>
                  )}
                </div>

                <div
                  className="w-10 h-10 rounded-lg overflow-hidden flex-shrink-0 flex items-center justify-center"
                  style={getGradientStyle(index)}
                >
                  <svg
                    width="18"
                    height="18"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="white"
                    strokeWidth="2"
                    className="opacity-80"
                  >
                    <path d="M9 18V5l12-2v13" />
                    <circle cx="6" cy="18" r="3" />
                    <circle cx="18" cy="16" r="3" />
                  </svg>
                </div>

                <div className="flex-1 min-w-0">
                  <p
                    className={
                      isPlaying
                        ? "text-sm font-medium truncate transition-colors text-gradient"
                        : "text-sm font-medium truncate transition-colors text-white"
                    }
                  >
                    {track.title}
                  </p>
                  <p className="text-xs text-white/40 truncate">{track.artist}</p>
                </div>

                <span className="hidden sm:block px-2 py-0.5 rounded-full bg-white/5 text-[10px] text-white/50 font-medium">
                  {track.genre}
                </span>

                <span className="text-xs text-white/30 w-10 text-right font-mono">{track.duration}</span>
              </div>
            )
          })}
        </div>
      </div>

      <div className="p-4 border-t border-white/5 bg-black/20">
        <div className="flex gap-3">
          <button className="flex-1 flex items-center justify-center gap-2 py-3 bg-gradient-primary hover:opacity-90 text-white rounded-xl font-medium text-sm transition-all glow-sm">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
              <polygon points="5,3 19,12 5,21" />
            </svg>
            Tout lire
          </button>
          <button className="flex items-center justify-center w-12 h-12 rounded-xl glass hover:bg-white/10 transition-all">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z" />
            </svg>
          </button>
          <button className="flex items-center justify-center w-12 h-12 rounded-xl glass hover:bg-white/10 transition-all">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="18" cy="5" r="3" />
              <circle cx="6" cy="12" r="3" />
              <circle cx="18" cy="19" r="3" />
              <line x1="8.59" y1="13.51" x2="15.42" y2="17.49" />
              <line x1="15.41" y1="6.51" x2="8.59" y2="10.49" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  )
}

export default PlaylistView
