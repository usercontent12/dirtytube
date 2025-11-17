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
            if (this.disabled) return;
            this.disabled = true;

            const uuid = this.dataset.uuid;
            if (likedVideos.includes(uuid)) {
                showNotification('You already liked this video!', 'info');
                this.disabled = false;
                return;
            }

            try {
                const originalText = this.querySelector('span').textContent;
                this.querySelector('span').textContent = 'Liking...';
                this.style.opacity = '0.6';

                const response = await fetch(`/api/like/${uuid}`, { method: 'POST', headers: { 'Content-Type': 'application/json' }});
                const data = await response.json();

                if (data.success) {
                    const currentCount = parseInt(likeCountEl.textContent.replace(/,/g, ''));
                    animateCount(likeCountEl, currentCount, data.likes);

                    this.classList.add('liked');
                    this.querySelector('span').textContent = 'Liked';
                    this.style.opacity = '1';

                    likedVideos.push(uuid);
                    localStorage.setItem('likedVideos', JSON.stringify(likedVideos));

                    showNotification('Thanks for liking! ❤️', 'success');
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
        if (progress < 1) requestAnimationFrame(update);
    }
    requestAnimationFrame(update);
}

function easeOutQuad(t) { return t * (2 - t); }
function formatNumber(num) { return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); }

// Show notification
function showNotification(message, type = 'info') {
    const existing = document.querySelector('.notification');
    if (existing) existing.remove();

    c
