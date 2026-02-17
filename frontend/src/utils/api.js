import { useAuth } from "@clerk/clerk-react"

export const useApi = () => {
    const { getToken } = useAuth()

    const makeRequest = async (endpoint, options = {}) => {
        const token = await getToken()
        const defaultOptions = {
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            }
        }

        const backendUrl = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000"
        const response = await fetch(`${backendUrl}/api/${endpoint}`, {
            ...defaultOptions,
            ...options,
        })

        if (!response.ok) {
            const errorData = await response.json().catch(() => null)
            if (response.status === 429) {
                throw new Error("Daily quota exceeded")
            }
            throw new Error(errorData?.detail || "An error occurred")
        }

        return response.json()
    }

    return { makeRequest }
}