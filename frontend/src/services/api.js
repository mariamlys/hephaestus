
const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000"

/**
 * @param {string}
 * @param {Array}
 * @returns {Promise<Object>}
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
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `Erreur HTTP: ${response.status}`)
    }

    const data = await response.json()
    console.log("📥 Réponse reçue:", data)
    
    return data
    
  } catch (error) {
    console.error("❌ Erreur lors de l'envoi du message:", error)
    
    if (error.message.includes("Failed to fetch")) {
      throw new Error("❌ Backend inaccessible. Assure-toi que le serveur est lancé sur http://localhost:8000")
    }
    
    throw error
  }
}

/**
 * @returns {Promise<Object>}
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
    
    return {
      messages: [],
      total: 0,
      showing: 0,
      error: error.message
    }
  }
}

/**
 * @returns {Promise<Object>}
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
 * @returns {Promise<Array>} 
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
 *
 * @returns {Promise<Object>} 
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
 *
 * @returns {Promise<boolean>} 
 */
export async function isBackendAvailable() {
  try {
    const health = await checkHealth()
    return health.status === "ok" || health.status === "degraded"
  } catch {
    return false
  }
}

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