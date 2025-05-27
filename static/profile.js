document.addEventListener('DOMContentLoaded', function() {
    const followBtn = document.querySelector('.follow-btn');
    if (followBtn) {
        followBtn.addEventListener('click', async function() {
            const username = this.dataset.username;
            const action = this.textContent.trim().toLowerCase();
            const btn = this;
            
            btn.disabled = true;
            btn.textContent = 'Processing...';
            
            try {
                const response = await fetch(`/follow/${username}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({action: action})
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    btn.textContent = data.action === 'follow' ? 'Unfollow' : 'Follow';
                    // Update follower count if needed
                    const followerCount = document.querySelector('.profile-stats span:nth-child(2)');
                    if (followerCount) {
                        followerCount.textContent = `${data.follower_count} followers`;
                    }
                } else {
                    alert(data.error || 'An error occurred');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Network error occurred');
            } finally {
                btn.disabled = false;
            }
        });
    }
});