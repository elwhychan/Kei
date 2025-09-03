document.addEventListener('DOMContentLoaded', () => {
    const videosContainer = document.getElementById('videos-container');

    if (videosContainer) {
        fetch('/data/videos.json')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(videos => {
                if (videos.length === 0) {
                    videosContainer.innerHTML = '<p>Belum ada video yang diunggah.</p>';
                    return;
                }

                videos.forEach(video => {
                    const videoWrapper = document.createElement('div');
                    videoWrapper.className = 'video-item';

                    const videoElement = document.createElement('video');
                    videoElement.controls = true;
                    videoElement.src = video.full_size_src;

                    const videoTitle = document.createElement('h3');
                    videoTitle.textContent = video.title;

                    videoWrapper.appendChild(videoElement);
                    videoWrapper.appendChild(videoTitle);

                    videosContainer.appendChild(videoWrapper);
                });
            })
            .catch(error => {
                console.error('Error fetching videos:', error);
                videosContainer.innerHTML = '<p>Gagal memuat video. Silakan coba lagi nanti.</p>';
            });
    }
});
