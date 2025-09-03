document.addEventListener('DOMContentLoaded', () => {

    function createAudioPlayer(containerId, apiUrl) {
        const container = document.getElementById(containerId);

        if (!container) return;

        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                if (data.length === 0) {
                    container.innerHTML = '<p>Belum ada musik yang diunggah.</p>';
                    return;
                }

                data.forEach(item => {
                    const musicItem = document.createElement('div');
                    musicItem.className = 'music-item';

                    const title = document.createElement('h3');
                    title.textContent = item.title;

                    const artist = document.createElement('p');
                    artist.textContent = `Artist: ${item.artist}`;

                    const audioElement = document.createElement('audio');
                    audioElement.controls = true;
                    audioElement.src = item.full_size_src;

                    musicItem.appendChild(title);
                    musicItem.appendChild(artist);
                    musicItem.appendChild(audioElement);

                    container.appendChild(musicItem);
                });
            })
            .catch(error => {
                console.error(`Error fetching data from ${apiUrl}:`, error);
                container.innerHTML = `<p>Gagal memuat musik. Silakan coba lagi nanti.</p>`;
            });
    }

    // Panggil fungsi untuk Songs dan Mixed Album
    createAudioPlayer('songs-container', '/data/songs.json');
    createAudioPlayer('mixed-album-container', '/data/mixed_album.json');
});
