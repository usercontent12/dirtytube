document.addEventListener('DOMContentLoaded', function() {
    const likeBtn = document.getElementById('likeBtn');
    const likeCountEl = document.getElementById('likeCount');

    if (likeBtn && likeCountEl) {
        // Check if already liked (from localStorage)
        const videoUuid = likeBtn.dataset.uuid;
        const likedVideos = JSON.parse(localStorage.getItem('likedVideos') || '[]');
        
        if (likedVideos.includes(videoUuid)) {
            likeBtn.classList.add('liked');
            likeBtn.querySelector('span').textContent = 'Liked';
        }

        likeBtn.addEventListener('click', async function() {
            // Prevent multiple clicks
            if (this.disabled) return;
            this.disabled = true;

            const uuid = this.dataset.uuid;
            
            // Check if already liked
            if (likedVideos.includes(uuid)) {
                showNotification('You already liked this video!', 'info');
                this.disabled = false;
                return;
            }

            try {
                // Add loading state
                const originalText = this.querySelector('span').textContent;
                this.querySelector('span').textContent = 'Liking...';
                this.style.opacity = '0.6';

                // Send like request
                const response = await fetch(`/api/like/${uuid}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });

                const data = await response.json();

                if (data.success) {
                    // Update like count with animation
                    const currentCount = parseInt(likeCountEl.textContent.replace(/,/g, ''));
                    animateCount(likeCountEl, currentCount, data.likes);

                    // Update button state
                    this.classList.add('liked');
                    this.querySelector('span').textContent = 'Liked';
                    this.style.opacity = '1';

                    // Store in localStorage
                    likedVideos.push(uuid);
                    localStorage.setItem('likedVideos', JSON.stringify(likedVideos));

                    // Show success notification
                    showNotification('Thanks for liking! ❤️', 'success');

                    // Add celebration animation
                    celebrateAnimation(this);
                } else {
                    throw new Error(data.error || 'Failed to like video');
                }
            } catch (error) {
                console.error('Error liking video:', error);
                this.querySelector('span').textContent = originalText;
                this.style.opacity = '1';
                showNotification('Failed to like video. Please try again.', 'error');
            } finally {
                this.disabled = false;
            }
        });
    }
});

// Animate count change
function animateCount(element, start, end) {
    const duration = 500;
    const startTime = performance.now();
    
    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const current = Math.floor(start + (end - start) * easeOutQuad(progress));
        element.textContent = formatNumber(current);
        
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }
    
    requestAnimationFrame(update);
}

// Easing function
function easeOutQuad(t) {
    return t * (2 - t);
}

// Format number with commas
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Show notification
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existing = document.querySelector('.notification');
    if (existing) {
        existing.remove();
    }

    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    notification.style.cssText = `
        position: fixed;
        top: 80px;
        right: 20px;
        padding: 16px 24px;
        border-radius: 8px;
        background: ${type === 'success' ? 'var(--success)' : type === 'error' ? 'var(--danger)' : 'var(--primary-color)'};
        color: white;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        z-index: 10000;
        animation: slideInRight 0.3s ease;
        max-width: 300px;
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Celebration animation
function celebrateAnimation(button) {
    const rect = button.getBoundingClientRect();
    const heartCount = 10;

    for (let i = 0; i < heartCount; i++) {
        const heart = document.createElement('div');
        heart.textContent = '❤️';
        heart.style.cssText = `
            position: fixed;
            left: ${rect.left + rect.width / 2}px;
            top: ${rect.top + rect.height / 2}px;
            font-size: 20px;
            pointer-events: none;
            z-index: 10000;
            animation: heartFloat ${1 + Math.random()}s ease-out forwards;
            opacity: 1;
        `;
        
        // Random direction
        const angle = (Math.PI * 2 * i) / heartCount;
        const distance = 50 + Math.random() * 50;
        const tx = Math.cos(angle) * distance;
        const ty = Math.sin(angle) * distance - 50;
        
        heart.style.setProperty('--tx', `${tx}px`);
        heart.style.setProperty('--ty', `${ty}px`);
        
        document.body.appendChild(heart);
        
        setTimeout(() => heart.remove(), 1000);
    }
}

// Add animation styles
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }

    @keyframes heartFloat {
        to {
            transform: translate(var(--tx), var(--ty));
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);