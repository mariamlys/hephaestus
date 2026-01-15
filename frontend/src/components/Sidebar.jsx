// "use client"

// const suggestions = [
//   {
//     icon: "running",
//     text: "Session cardio",
//     query: "Une playlist énergique pour 30 min de running",
//     color: "from-orange-500 to-red-500",
//   },
//   {
//     icon: "meditation",
//     text: "Méditation",
//     query: "Musique zen pour méditer et se relaxer",
//     color: "from-cyan-500 to-blue-500",
//   },
//   {
//     icon: "gym",
//     text: "Musculation",
//     query: "Des beats puissants pour la salle de sport",
//     color: "from-violet-500 to-purple-500",
//   },
//   {
//     icon: "work",
//     text: "Deep Focus",
//     query: "Musique de concentration sans paroles",
//     color: "from-emerald-500 to-teal-500",
//   },
//   {
//     icon: "party",
//     text: "Soirée",
//     query: "Playlist festive pour une soirée entre amis",
//     color: "from-pink-500 to-rose-500",
//   },
// ]

// const icons = {
//   running: (
//     <svg
//       width="18"
//       height="18"
//       viewBox="0 0 24 24"
//       fill="none"
//       stroke="currentColor"
//       strokeWidth="2"
//       strokeLinecap="round"
//       strokeLinejoin="round"
//     >
//       <circle cx="12" cy="5" r="2" />
//       <path d="M7 20l3-5-2-3 3-3 4 3-2 7" />
//     </svg>
//   ),
//   meditation: (
//     <svg
//       width="18"
//       height="18"
//       viewBox="0 0 24 24"
//       fill="none"
//       stroke="currentColor"
//       strokeWidth="2"
//       strokeLinecap="round"
//       strokeLinejoin="round"
//     >
//       <circle cx="12" cy="12" r="10" />
//       <path d="M12 6v6l4 2" />
//     </svg>
//   ),
//   gym: (
//     <svg
//       width="18"
//       height="18"
//       viewBox="0 0 24 24"
//       fill="none"
//       stroke="currentColor"
//       strokeWidth="2"
//       strokeLinecap="round"
//       strokeLinejoin="round"
//     >
//       <path d="M6 4v16M18 4v16M6 12h12M4 8h4M16 8h4M4 16h4M16 16h4" />
//     </svg>
//   ),
//   work: (
//     <svg
//       width="18"
//       height="18"
//       viewBox="0 0 24 24"
//       fill="none"
//       stroke="currentColor"
//       strokeWidth="2"
//       strokeLinecap="round"
//       strokeLinejoin="round"
//     >
//       <rect x="2" y="3" width="20" height="14" rx="2" ry="2" />
//       <line x1="8" y1="21" x2="16" y2="21" />
//       <line x1="12" y1="17" x2="12" y2="21" />
//     </svg>
//   ),
//   party: (
//     <svg
//       width="18"
//       height="18"
//       viewBox="0 0 24 24"
//       fill="none"
//       stroke="currentColor"
//       strokeWidth="2"
//       strokeLinecap="round"
//       strokeLinejoin="round"
//     >
//       <path d="M5.8 11.3L2 22l10.7-3.8M15 7l-5.5 5.5" />
//       <path d="M22 2L11 13" />
//       <path d="M9 4l1.5 1.5M4 9l1.5 1.5M19 14l1.5 1.5M14 19l1.5 1.5" />
//     </svg>
//   ),
// }

// function Sidebar({ isOpen, onToggle, onSuggestionClick }) {
//   return (
//     <>
//       {/* Overlay mobile */}
//       {isOpen && <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 lg:hidden" onClick={onToggle} />}

//       <aside
//         className={`${
//           isOpen ? "translate-x-0" : "-translate-x-full"
//         } fixed lg:relative inset-y-0 left-0 w-72 flex flex-col glass-strong z-50 transition-transform duration-300 ease-out`}
//       >
//         {/* Logo */}
//         <div className="flex items-center justify-between p-5 border-b border-white/5">
//           <div className="flex items-center gap-3">
//             <div className="w-10 h-10 rounded-xl bg-gradient-accent flex items-center justify-center animate-pulse-glow">
//               <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
//                 <path d="M9 18V5l12-2v13" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
//                 <circle cx="6" cy="18" r="3" stroke="white" strokeWidth="2" />
//                 <circle cx="18" cy="16" r="3" stroke="white" strokeWidth="2" />
//               </svg>
//             </div>
//             <div>
//               <span className="text-base font-semibold text-gradient">MusicBot</span>
//               <p className="text-[10px] text-white/40 uppercase tracking-wider">AI Playlist Generator</p>
//             </div>
//           </div>
//           <button onClick={onToggle} className="p-2 rounded-lg hover:bg-white/5 transition-colors lg:hidden">
//             <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
//               <line x1="18" y1="6" x2="6" y2="18" />
//               <line x1="6" y1="6" x2="18" y2="18" />
//             </svg>
//           </button>
//         </div>

//         {/* Navigation */}
//         <nav className="flex-1 p-4 overflow-y-auto">
//           <div className="mb-8">
//             <h3 className="text-[10px] font-semibold text-white/30 uppercase tracking-wider mb-3 px-3">Menu</h3>
//             <button className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl bg-white/5 border border-white/10 text-white mb-1.5 group">
//               <div className="w-8 h-8 rounded-lg bg-gradient-primary flex items-center justify-center">
//                 <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
//                   <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
//                 </svg>
//               </div>
//               <span className="text-sm font-medium">Nouvelle conversation</span>
//             </button>
//             <button className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-white/50 hover:bg-white/5 hover:text-white transition-all mb-1.5">
//               <div className="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center">
//                 <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
//                   <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z" />
//                 </svg>
//               </div>
//               <span className="text-sm">Mes playlists</span>
//             </button>
//             <button className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-white/50 hover:bg-white/5 hover:text-white transition-all">
//               <div className="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center">
//                 <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
//                   <circle cx="12" cy="12" r="3" />
//                   <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4" />
//                 </svg>
//               </div>
//               <span className="text-sm">Paramètres</span>
//             </button>
//           </div>

//           <div>
//             <h3 className="text-[10px] font-semibold text-white/30 uppercase tracking-wider mb-3 px-3">
//               Suggestions rapides
//             </h3>
//             <div className="space-y-1.5">
//               {suggestions.map((item, index) => (
//                 <button
//                   key={index}
//                   className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-white/60 hover:bg-white/5 hover:text-white transition-all group"
//                   onClick={() => onSuggestionClick(item.query)}
//                 >
//                   <div
//                     className={`w-8 h-8 rounded-lg bg-gradient-to-br ${item.color} flex items-center justify-center opacity-80 group-hover:opacity-100 transition-opacity`}
//                   >
//                     {icons[item.icon]}
//                   </div>
//                   <span className="text-sm">{item.text}</span>
//                   <svg
//                     className="w-4 h-4 ml-auto opacity-0 group-hover:opacity-50 transition-opacity"
//                     viewBox="0 0 24 24"
//                     fill="none"
//                     stroke="currentColor"
//                     strokeWidth="2"
//                   >
//                     <polyline points="9 18 15 12 9 6" />
//                   </svg>
//                 </button>
//               ))}
//             </div>
//           </div>
//         </nav>

//         {/* Footer */}
//         <div className="p-4 border-t border-white/5">
//           <div className="flex items-center gap-3 px-3 py-2">
//             <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center text-xs font-semibold">
//               U
//             </div>
//             <div className="flex-1 min-w-0">
//               <p className="text-sm font-medium text-white truncate">Utilisateur</p>
//               <p className="text-xs text-white/40">Mode local</p>
//             </div>
//             <div className="flex items-center gap-1">
//               <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
//             </div>
//           </div>
//         </div>
//       </aside>
//     </>
//   )
// }

// export default Sidebar


"use client"

const suggestions = [
  {
    icon: "running",
    text: "Session cardio",
    query: "Playlist pour course à pied 30 min",  // ✅ Mot-clé "course" détectable
    color: "from-orange-500 to-red-500",
  },
  {
    icon: "meditation",
    text: "Méditation",
    query: "Musique zen pour échauffement et relaxation",  // ✅ Mot-clé "échauffement"
    color: "from-cyan-500 to-blue-500",
  },
  {
    icon: "gym",
    text: "Musculation",
    query: "Playlist musculation pour 45 min",  // ✅ Mot-clé "musculation"
    color: "from-violet-500 to-purple-500",
  },
  {
    icon: "work",
    text: "Marche",
    query: "Musique calme pour marcher 30 min",  // ✅ Mot-clé "marche"
    color: "from-emerald-500 to-teal-500",
  },
  {
    icon: "party",
    text: "Boxe",
    query: "Playlist intense pour session de boxe",  // ✅ Mot-clé "boxe"
    color: "from-pink-500 to-rose-500",
  },
]

const icons = {
  running: (
    <svg
      width="18"
      height="18"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="12" cy="5" r="2" />
      <path d="M7 20l3-5-2-3 3-3 4 3-2 7" />
    </svg>
  ),
  meditation: (
    <svg
      width="18"
      height="18"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="12" cy="12" r="10" />
      <path d="M12 6v6l4 2" />
    </svg>
  ),
  gym: (
    <svg
      width="18"
      height="18"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M6 4v16M18 4v16M6 12h12M4 8h4M16 8h4M4 16h4M16 16h4" />
    </svg>
  ),
  work: (
    <svg
      width="18"
      height="18"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="12" cy="5" r="2" />
      <path d="M7 20l3-5-2-3 3-3 4 3-2 7" />
    </svg>
  ),
  party: (
    <svg
      width="18"
      height="18"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M5.8 11.3L2 22l10.7-3.8M15 7l-5.5 5.5" />
      <path d="M22 2L11 13" />
      <path d="M9 4l1.5 1.5M4 9l1.5 1.5M19 14l1.5 1.5M14 19l1.5 1.5" />
    </svg>
  ),
}

function Sidebar({ isOpen, onToggle, onSuggestionClick }) {
  return (
    <>
      {/* Overlay mobile */}
      {isOpen && <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 lg:hidden" onClick={onToggle} />}

      <aside
        className={`${
          isOpen ? "translate-x-0" : "-translate-x-full"
        } fixed lg:relative inset-y-0 left-0 w-72 flex flex-col glass-strong z-50 transition-transform duration-300 ease-out`}
      >
        {/* Logo */}
        <div className="flex items-center justify-between p-5 border-b border-white/5">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-accent flex items-center justify-center animate-pulse-glow">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
                <path d="M9 18V5l12-2v13" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                <circle cx="6" cy="18" r="3" stroke="white" strokeWidth="2" />
                <circle cx="18" cy="16" r="3" stroke="white" strokeWidth="2" />
              </svg>
            </div>
            <div>
              <span className="text-base font-semibold text-gradient">MusicBot</span>
              <p className="text-[10px] text-white/40 uppercase tracking-wider">AI Playlist Generator</p>
            </div>
          </div>
          <button onClick={onToggle} className="p-2 rounded-lg hover:bg-white/5 transition-colors lg:hidden">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 overflow-y-auto">
          <div className="mb-8">
            <h3 className="text-[10px] font-semibold text-white/30 uppercase tracking-wider mb-3 px-3">Menu</h3>
            <button className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl bg-white/5 border border-white/10 text-white mb-1.5 group">
              <div className="w-8 h-8 rounded-lg bg-gradient-primary flex items-center justify-center">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
                  <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
                </svg>
              </div>
              <span className="text-sm font-medium">Nouvelle conversation</span>
            </button>
            <button className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-white/50 hover:bg-white/5 hover:text-white transition-all mb-1.5">
              <div className="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z" />
                </svg>
              </div>
              <span className="text-sm">Mes playlists</span>
            </button>
            <button className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-white/50 hover:bg-white/5 hover:text-white transition-all">
              <div className="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="3" />
                  <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4" />
                </svg>
              </div>
              <span className="text-sm">Paramètres</span>
            </button>
          </div>

          <div>
            <h3 className="text-[10px] font-semibold text-white/30 uppercase tracking-wider mb-3 px-3">
              Suggestions rapides
            </h3>
            <div className="space-y-1.5">
              {suggestions.map((item, index) => (
                <button
                  key={index}
                  className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-white/60 hover:bg-white/5 hover:text-white transition-all group"
                  onClick={() => onSuggestionClick(item.query)}
                >
                  <div
                    className={`w-8 h-8 rounded-lg bg-gradient-to-br ${item.color} flex items-center justify-center opacity-80 group-hover:opacity-100 transition-opacity`}
                  >
                    {icons[item.icon]}
                  </div>
                  <span className="text-sm">{item.text}</span>
                  <svg
                    className="w-4 h-4 ml-auto opacity-0 group-hover:opacity-50 transition-opacity"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                  >
                    <polyline points="9 18 15 12 9 6" />
                  </svg>
                </button>
              ))}
            </div>
          </div>
        </nav>

        {/* Footer */}
        <div className="p-4 border-t border-white/5">
          <div className="flex items-center gap-3 px-3 py-2">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center text-xs font-semibold">
              U
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-white truncate">Utilisateur</p>
              <p className="text-xs text-white/40">Mode local</p>
            </div>
            <div className="flex items-center gap-1">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
            </div>
          </div>
        </div>
      </aside>
    </>
  )
}

export default Sidebar