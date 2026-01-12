"use client"

import { useState, useEffect } from "react"
import { Link } from "react-router-dom"

function LandingPage() {
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    setIsVisible(true)
  }, [])

  const features = [
    {
      icon: (
        <svg
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <circle cx="12" cy="12" r="10" />
          <polygon points="10 8 16 12 10 16 10 8" />
        </svg>
      ),
      title: "Playlists Intelligentes",
      description: "L'IA analyse ton mood et compose des playlists personnalisées en temps réel.",
    },
    {
      icon: (
        <svg
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M9 18V5l12-2v13" />
          <circle cx="6" cy="18" r="3" />
          <circle cx="18" cy="16" r="3" />
        </svg>
      ),
      title: "Musique sur Mesure",
      description: "Décris ton activité et reçois une sélection adaptée à ton énergie.",
    },
    {
      icon: (
        <svg
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M12 2a10 10 0 1 0 10 10H12V2z" />
          <path d="M12 2a10 10 0 0 1 10 10" />
          <circle cx="12" cy="12" r="6" />
        </svg>
      ),
      title: "IA Locale",
      description: "Propulsé par Ollama, ton assistant fonctionne entièrement en local.",
    },
  ]

  const activities = [
    { name: "Running", color: "from-orange-500 to-red-500" },
    { name: "Méditation", color: "from-cyan-500 to-blue-500" },
    { name: "Musculation", color: "from-violet-500 to-purple-500" },
    { name: "Travail", color: "from-emerald-500 to-teal-500" },
    { name: "Soirée", color: "from-pink-500 to-rose-500" },
  ]

  return (
    <div className="relative min-h-screen bg-[#050508] overflow-hidden">
      {/* Ambient background */}
      <div className="ambient-bg">
        <div className="ambient-orb ambient-orb-1"></div>
        <div className="ambient-orb ambient-orb-2"></div>
        <div className="ambient-orb ambient-orb-3"></div>
      </div>

      {/* Navigation */}
      <nav className="relative z-20 flex items-center justify-between px-6 lg:px-12 py-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-accent flex items-center justify-center glow-sm">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
              <path d="M9 18V5l12-2v13" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              <circle cx="6" cy="18" r="3" stroke="white" strokeWidth="2" />
              <circle cx="18" cy="16" r="3" stroke="white" strokeWidth="2" />
            </svg>
          </div>
          <div>
            <span className="text-lg font-semibold text-gradient">MusicBot</span>
            <span className="text-white/40 text-sm ml-1">AI</span>
          </div>
        </div>
        <Link
          to="/chat"
          className="px-5 py-2.5 bg-gradient-primary hover:opacity-90 text-white text-sm font-medium rounded-xl transition-all glow-sm"
        >
          Lancer le Chat
        </Link>
      </nav>

      {/* Hero Section */}
      <main className="relative z-10">
        <section className="flex flex-col items-center justify-center text-center px-6 pt-16 pb-24 lg:pt-24 lg:pb-32">
          <div
            className={`transition-all duration-1000 ${isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}
          >
            {/* Badge */}
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass text-sm text-white/70 mb-8">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              Propulsé par Ollama
            </div>

            {/* Titre */}
            <h1 className="text-4xl sm:text-5xl lg:text-7xl font-bold text-white mb-6 leading-tight">
              Ton assistant
              <br />
              <span className="text-gradient">musical intelligent</span>
            </h1>

            {/* Description */}
            <p className="text-lg lg:text-xl text-white/50 max-w-2xl mx-auto mb-10 leading-relaxed">
              Décris ton activité ou ton mood en langage naturel. L'IA compose une playlist parfaitement adaptée à ton
              moment.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link
                to="/chat"
                className="group flex items-center gap-3 px-8 py-4 bg-gradient-primary hover:opacity-90 text-white font-medium rounded-xl transition-all glow-primary"
              >
                <span>Commencer maintenant</span>
                <svg
                  className="w-5 h-5 group-hover:translate-x-1 transition-transform"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                >
                  <path d="M5 12h14M12 5l7 7-7 7" />
                </svg>
              </Link>
              <a
                href="#features"
                className="px-8 py-4 glass hover:bg-white/10 text-white/70 hover:text-white font-medium rounded-xl transition-all"
              >
                En savoir plus
              </a>
            </div>
          </div>

          {/* Activities Pills */}
          <div
            className={`flex flex-wrap justify-center gap-3 mt-16 transition-all duration-1000 delay-300 ${isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}
          >
            {activities.map((activity, index) => (
              <span
                key={index}
                className={`px-4 py-2 rounded-full bg-gradient-to-r ${activity.color} text-white text-sm font-medium opacity-80`}
              >
                {activity.name}
              </span>
            ))}
          </div>
        </section>

        {/* Features Section */}
        <section id="features" className="px-6 lg:px-12 py-20 lg:py-28">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-3xl lg:text-4xl font-bold text-white mb-4">
                Comment ça <span className="text-gradient">fonctionne</span>
              </h2>
              <p className="text-white/50 max-w-xl mx-auto">
                Une architecture moderne alliant IA conversationnelle et génération de playlists.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {features.map((feature, index) => (
                <div
                  key={index}
                  className="group p-8 rounded-2xl glass border-gradient hover:bg-white/5 transition-all"
                >
                  <div className="w-14 h-14 rounded-xl bg-gradient-accent flex items-center justify-center mb-6 glow-sm group-hover:scale-110 transition-transform">
                    {feature.icon}
                  </div>
                  <h3 className="text-xl font-semibold text-white mb-3">{feature.title}</h3>
                  <p className="text-white/50 leading-relaxed">{feature.description}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Architecture Section */}
        <section className="px-6 lg:px-12 py-20 lg:py-28">
          <div className="max-w-4xl mx-auto">
            <div className="p-8 lg:p-12 rounded-2xl glass border-gradient">
              <h3 className="text-2xl font-bold text-white mb-6 text-center">Architecture du Projet</h3>

              <div className="flex flex-col lg:flex-row items-center justify-between gap-8">
                {/* Frontend */}
                <div className="flex flex-col items-center text-center">
                  <div className="w-16 h-16 rounded-xl bg-gradient-to-br from-cyan-500 to-blue-500 flex items-center justify-center mb-3 glow-sm">
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
                      <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                      <line x1="3" y1="9" x2="21" y2="9" />
                    </svg>
                  </div>
                  <span className="text-white font-medium">Frontend</span>
                  <span className="text-white/40 text-sm">React + Tailwind</span>
                </div>

                {/* Arrow */}
                <svg
                  className="w-8 h-8 text-white/30 rotate-90 lg:rotate-0"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                >
                  <path d="M5 12h14M12 5l7 7-7 7" />
                </svg>

                {/* Backend */}
                <div className="flex flex-col items-center text-center">
                  <div className="w-16 h-16 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-500 flex items-center justify-center mb-3 glow-sm">
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
                      <rect x="2" y="2" width="20" height="8" rx="2" ry="2" />
                      <rect x="2" y="14" width="20" height="8" rx="2" ry="2" />
                      <line x1="6" y1="6" x2="6.01" y2="6" />
                      <line x1="6" y1="18" x2="6.01" y2="18" />
                    </svg>
                  </div>
                  <span className="text-white font-medium">Backend</span>
                  <span className="text-white/40 text-sm">Python + FastAPI</span>
                </div>

                {/* Arrow */}
                <svg
                  className="w-8 h-8 text-white/30 rotate-90 lg:rotate-0"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                >
                  <path d="M5 12h14M12 5l7 7-7 7" />
                </svg>

                {/* MCP + Ollama */}
                <div className="flex flex-col items-center text-center">
                  <div className="w-16 h-16 rounded-xl bg-gradient-accent flex items-center justify-center mb-3 animate-pulse-glow">
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
                      <circle cx="12" cy="12" r="3" />
                      <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" />
                    </svg>
                  </div>
                  <span className="text-white font-medium">MCP + Ollama</span>
                  <span className="text-white/40 text-sm">IA Locale</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Final */}
        <section className="px-6 lg:px-12 py-20 lg:py-28">
          <div className="max-w-3xl mx-auto text-center">
            <h2 className="text-3xl lg:text-4xl font-bold text-white mb-6">
              Prêt à découvrir ta nouvelle<span className="text-gradient"> playlist</span> ?
            </h2>
            <p className="text-white/50 mb-10 max-w-xl mx-auto">
              Interagis avec l'IA en langage naturel et laisse la magie opérer.
            </p>
            <Link
              to="/chat"
              className="inline-flex items-center gap-3 px-10 py-5 bg-gradient-primary hover:opacity-90 text-white text-lg font-medium rounded-xl transition-all glow-primary"
            >
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
              </svg>
              <span>Accéder au Chat</span>
            </Link>
          </div>
        </section>

        {/* Footer */}
        <footer className="px-6 lg:px-12 py-8 border-t border-white/5">
          <div className="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-gradient-accent flex items-center justify-center">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
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
              <span className="text-sm text-white/40">MusicBot AI — Projet MSc MSI 2028</span>
            </div>
            <p className="text-sm text-white/30">Propulsé par Ollama & Pixabay</p>
          </div>
        </footer>
      </main>
    </div>
  )
}

export default LandingPage
