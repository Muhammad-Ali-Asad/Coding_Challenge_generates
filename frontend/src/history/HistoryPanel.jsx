import "react"
import { useState, useEffect } from "react"
import { MCQChallenge } from "../challenge/MCQChallenge.jsx";
import { useApi } from "../utils/api.js";

export function HistoryPanel() {
    const { makeRequest } = useApi()
    const [history, setHistory] = useState([])
    const [isLoading, setIsLoading] = useState(true)
    const [error, setError] = useState(null)

    useEffect(() => {
        fetchHistory()
    }, [])

    const fetchHistory = async () => {
        setIsLoading(true)
        setError(null)

        try {
            const data = await makeRequest("my-history")
            console.log(data)
            setHistory(data.challenges)
        } catch (err) {
            setError("Failed to load history.")
        } finally {
            setIsLoading(false)
        }
    }

    if (isLoading) {
        return <div className="loading">Loading history...</div>
    }

    if (error) {
        return <div className="error-message">
            <p>{error}</p>
            <button onClick={fetchHistory}>Retry</button>
        </div>
    }

    const handleResetHistory = async () => {
        try {
            await makeRequest("my-history", { method: "DELETE" })
            setHistory([])
        } catch (err) {
            setError("Failed to delete history.")
        }
    }

    return <div className="history-panel">
        <div className="history-header">
            <h2>History</h2>
            <button onClick={handleResetHistory} className="reset-button" style={{ backgroundColor: "#ff4444", color: "white", padding: "8px 16px", border: "none", borderRadius: "4px", cursor: "pointer" }}>
                Reset History
            </button>
        </div>
        {history.length === 0 ? <p>No challenge history</p> :
            <div className="history-list">
                {history.map((challenge) => {
                    return <MCQChallenge
                        challenge={challenge}
                        key={challenge.id}
                        showExplanation
                    />
                })}
            </div>
        }
    </div>
}