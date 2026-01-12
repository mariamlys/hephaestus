// Service API pour communiquer avec le backend FastAPI
const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000"

/**
 * Envoie un message au chatbot et récupère la réponse
 * @param {string} message - Le message de l'utilisateur
 * @returns {Promise<Object>} - La réponse du bot avec la playlist
 */
export async function sendMessage(message) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    })

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error("Erreur lors de l'envoi du message:", error)
    throw error
  }
}

/**
 * Récupère l'historique des conversations
 * @returns {Promise<Array>} - Liste des messages
 */
export async function getHistory() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/history`)

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error("Erreur lors de la récupération de l'historique:", error)
    throw error
  }
}

/**
 * Vérifie si le backend est en ligne
 * @returns {Promise<boolean>}
 */
export async function checkHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`)
    return response.ok
  } catch (error) {
    return false
  }
}
