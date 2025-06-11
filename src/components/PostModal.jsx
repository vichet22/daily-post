import { useEffect } from 'react'
import { useApp } from '../context/AppContext'
import './PostModal.css'

const PostModal = () => {
  const { selectedPost, dispatch, ACTIONS } = useApp()

  useEffect(() => {
    if (selectedPost) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = 'unset'
    }

    return () => {
      document.body.style.overflow = 'unset'
    }
  }, [selectedPost])

  const handleClose = () => {
    dispatch({ type: ACTIONS.SET_SELECTED_POST, payload: null })
  }

  const handleBackdropClick = (e) => {
    if (e.target === e.currentTarget) {
      handleClose()
    }
  }

  const getCategoryColor = (category) => {
    const colors = {
      'SPORT': '#ff9500',
      'NEWS': '#34c759',
      'POLITICS': '#007aff'
    }
    return colors[category] || '#4285f4'
  }

  if (!selectedPost) return null

  return (
    <div className="post-modal-overlay" onClick={handleBackdropClick}>
      <div className="post-modal">
        <button className="modal-close-button" onClick={handleClose}>
          ✕
        </button>
        
        <div className="modal-header">
          <img 
            src={selectedPost.image} 
            alt={selectedPost.title}
            className="modal-image"
          />
          <div 
            className="modal-category-badge"
            style={{ backgroundColor: getCategoryColor(selectedPost.category) }}
          >
            {selectedPost.category}
          </div>
        </div>

        <div className="modal-content">
          <div className="modal-meta">
            <span className="modal-date">{selectedPost.date}</span>
            <span className="modal-read-time">{selectedPost.readTime}</span>
          </div>

          <h1 className="modal-title">{selectedPost.title}</h1>

          <div className="modal-author">
            <div className="author-avatar">👤</div>
            <span>By {selectedPost.author}</span>
          </div>

          <div className="modal-body">
            <p className="modal-excerpt">{selectedPost.excerpt}</p>
            
            <div className="modal-full-content">
              <p>{selectedPost.content}</p>
              
              {/* Extended content for demo */}
              <p>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod 
                tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, 
                quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
              </p>
              
              <p>
                Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore 
                eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, 
                sunt in culpa qui officia deserunt mollit anim id est laborum.
              </p>

              <h3>Key Points</h3>
              <ul>
                <li>Important development in the story</li>
                <li>Analysis of current situation</li>
                <li>Future implications and predictions</li>
                <li>Expert opinions and commentary</li>
              </ul>

              <p>
                Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium 
                doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore 
                veritatis et quasi architecto beatae vitae dicta sunt explicabo.
              </p>
            </div>
          </div>

          <div className="modal-actions">
            <button 
              className="share-button"
              onClick={() => {
                if (navigator.share) {
                  navigator.share({
                    title: selectedPost.title,
                    text: selectedPost.excerpt,
                    url: window.location.href
                  })
                } else {
                  navigator.clipboard.writeText(window.location.href)
                  alert('Link copied to clipboard!')
                }
              }}
            >
              📤 Share Article
            </button>
            
            <button 
              className="close-button"
              onClick={handleClose}
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default PostModal
