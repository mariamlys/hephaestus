/**
 * api.js - Service API pour communiquer avec le backend FastAPI
 * =============================================================
 * Service pour gérer toutes les communications avec le backend Hephaestus
 */

// Configuration de l'URL du backend
const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000"

/**
 * Envoie un message au chatbot et récupère la réponse avec playlist
 * @param {string} message - Le message de l'utilisateur
 * @param {Array} conversationHistory - Historique de la conversation (optionnel)
 * @returns {Promise<Object>} - La réponse du bot avec la playlist
 * 
 * Exemple de réponse:
 * {
 *   response: "🎵 Playlist 🏃 Course à pied...",
 *   playlist: {
 *     sport: "course_a_pied",
 *     target_duration_min: 60,
 *     playlist: [...],
 *     bpm_range: "140-180"
 *   },
 *   error: null
 * }
 */
export async function sendMessage(message, conversationHistory = []) {
  try {
    console.log("📤 Envoi message:", message)
    
    const response = await fetch(`${API_BASE_URL}/api/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ 
        message,
        conversation_history: conversationHistory 
      }),
    })

    if (!response.ok) {
      // Gestion détaillée des erreurs HTTP
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `Erreur HTTP: ${response.status}`)
    }

    const data = await response.json()
    console.log("📥 Réponse reçue:", data)
    
    return data
    
  } catch (error) {
    console.error("❌ Erreur lors de l'envoi du message:", error)
    
    // Vérifier si c'est une erreur réseau
    if (error.message.includes("Failed to fetch")) {
      throw new Error("❌ Backend inaccessible. Assure-toi que le serveur est lancé sur http://localhost:8000")
    }
    
    throw error
  }
}

/**
 * Récupère l'historique des conversations
 * @returns {Promise<Object>} - Historique des messages
 * 
 * Exemple de réponse:
 * {
 *   messages: [...],
 *   total: 25,
 *   showing: 25
 * }
 */
export async function getHistory() {
  try {
    console.log("📤 Récupération de l'historique...")
    
    const response = await fetch(`${API_BASE_URL}/api/history`)

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`)
    }

    const data = await response.json()
    console.log("📥 Historique reçu:", data.total, "messages")
    
    return data
    
  } catch (error) {
    console.error("❌ Erreur lors de la récupération de l'historique:", error)
    
    // Retourner un objet vide plutôt que crasher
    return {
      messages: [],
      total: 0,
      showing: 0,
      error: error.message
    }
  }
}

/**
 * Vérifie si le backend est en ligne et fonctionnel
 * @returns {Promise<Object>} - Status du backend
 * 
 * Exemple de réponse:
 * {
 *   status: "ok" | "degraded",
 *   components: {
 *     ollama: "ok" | "error",
 *     mcp: "ok" | "error",
 *     api: "ok"
 *   }
 * }
 */
export async function checkHealth() {
  try {
    console.log("📤 Vérification du health check...")
    
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
    
    if (!response.ok) {
      return {
        status: "error",
        components: {
          api: "error",
          ollama: "unknown",
          mcp: "unknown"
        }
      }
    }
    
    const data = await response.json()
    console.log("📥 Health status:", data.status)
    
    return data
    
  } catch (error) {
    console.error("❌ Backend inaccessible:", error)
    
    return {
      status: "offline",
      components: {
        api: "offline",
        ollama: "unknown",
        mcp: "unknown"
      },
      error: error.message
    }
  }
}

/**
 * Récupère la liste des catégories de sport disponibles
 * @returns {Promise<Array>} - Liste des catégories
 * 
 * Exemple de réponse:
 * [
 *   "course_a_pied",
 *   "boxe",
 *   "musculation",
 *   "marche_a_pied",
 *   "echauffement"
 * ]
 */
export async function getCategories() {
  try {
    console.log("📤 Récupération des catégories...")
    
    const response = await fetch(`${API_BASE_URL}/categories`)

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`)
    }

    const data = await response.json()
    console.log("📥 Catégories reçues:", data)
    
    return data
    
  } catch (error) {
    console.error("❌ Erreur lors de la récupération des catégories:", error)
    
    // Retourner les catégories par défaut
    return [
      "course_a_pied",
      "boxe", 
      "musculation",
      "marche_a_pied",
      "echauffement"
    ]
  }
}

/**
 * Récupère les informations de base de l'API
 * @returns {Promise<Object>} - Informations sur l'API
 */
export async function getApiInfo() {
  try {
    const response = await fetch(`${API_BASE_URL}/`)

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`)
    }

    return await response.json()
    
  } catch (error) {
    console.error("❌ Erreur lors de la récupération des infos API:", error)
    return {
      app: "Hephaestus",
      version: "unknown",
      error: error.message
    }
  }
}

/**
 * Utilitaire: Formate un message pour l'historique
 * @param {string} role - "user" ou "assistant"
 * @param {string} content - Contenu du message
 * @returns {Object} - Message formaté pour l'API
 */
export function formatMessage(role, content) {
  return {
    role: role,
    content: content
  }
}

/**
 * Utilitaire: Vérifie si le backend est disponible
 * @returns {Promise<boolean>} - true si disponible, false sinon
 */
export async function isBackendAvailable() {
  try {
    const health = await checkHealth()
    return health.status === "ok" || health.status === "degraded"
  } catch {
    return false
  }
}

// Export par défaut d'un objet contenant toutes les fonctions
const api = {
  sendMessage,
  getHistory,
  checkHealth,
  getCategories,
  getApiInfo,
  formatMessage,
  isBackendAvailable,
  BASE_URL: API_BASE_URL
}

export default api