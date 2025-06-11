import { useState, useEffect } from 'react'
import { Zap, CheckCircle, Edit, Trash2 } from 'lucide-react'
import './LiveUpdateIndicator.css'

const LiveUpdateIndicator = () => {
  const [lastUpdate, setLastUpdate] = useState(null)
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    const handlePostCreated = (event) => {
      setLastUpdate({
        type: 'created',
        message: `New post "${event.detail.post.title}" published!`,
        icon: <CheckCircle size={16} />
      })
      showIndicator()
    }

    const handlePostUpdated = (event) => {
      setLastUpdate({
        type: 'updated',
        message: `Post "${event.detail.post.title}" updated!`,
        icon: <Edit size={16} />
      })
      showIndicator()
    }

    const handlePostDeleted = (event) => {
      setLastUpdate({
        type: 'deleted',
        message: `Post deleted successfully!`,
        icon: <Trash2 size={16} />
      })
      showIndicator()
    }

    const showIndicator = () => {
      setIsVisible(true)
      setTimeout(() => {
        setIsVisible(false)
      }, 4000)
    }

    window.addEventListener('postCreated', handlePostCreated)
    window.addEventListener('postUpdated', handlePostUpdated)
    window.addEventListener('postDeleted', handlePostDeleted)

    return () => {
      window.removeEventListener('postCreated', handlePostCreated)
      window.removeEventListener('postUpdated', handlePostUpdated)
      window.removeEventListener('postDeleted', handlePostDeleted)
    }
  }, [])

  if (!isVisible || !lastUpdate) return null

  return (
    <div className={`live-update-indicator ${lastUpdate.type}`}>
      <div className="indicator-content">
        <Zap size={16} className="pulse-icon" />
        {lastUpdate.icon}
        <span>{lastUpdate.message}</span>
      </div>
    </div>
  )
}

export default LiveUpdateIndicator
