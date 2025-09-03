    document.addEventListener('DOMContentLoaded', () => {
        const galleryContainer = document.getElementById('gallery-container');
        const loadingMessage = document.getElementById('loading-message');
        const noImagesMessage = document.getElementById('no-images-message');
        const categoryButtons = document.querySelectorAll('.category-button');

        function fetchImages(url) {
            galleryContainer.innerHTML = '';
            loadingMessage.style.display = 'block';
            noImagesMessage.style.display = 'none';

            fetch(url)
                .then(response => response.json())
                .then(images => {
                    loadingMessage.style.display = 'none';
                    if (images.length === 0) {
                        noImagesMessage.style.display = 'block';
                        return;
                    }

                    images.forEach(image => {
                        const card = document.createElement('div');
                        card.classList.add('card');

                        const img = document.createElement('img');
                        img.src = image.src; // <-- Ini URL thumbnail
                        img.alt = image.title;
                        img.dataset.fullSizeSrc = image.full_size_src; // <-- URL ukuran penuh

                        const title = document.createElement('h9');
                        title.textContent = image.title;

                        card.appendChild(img);
                        card.appendChild(title);
                        galleryContainer.appendChild(card);
                    });
                })
                .catch(error => {
                    loadingMessage.textContent = 'Gagal memuat gambar.';
                    console.error('Error fetching gallery data:', error);
                });
        }

        // Muat semua gambar saat halaman pertama kali dimuat
        fetchImages('/data/gallery/semua.json');

        // Tambahkan event listener untuk tombol kategori
        categoryButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const category = e.target.dataset.category;

                categoryButtons.forEach(btn => btn.classList.remove('active'));
                e.target.classList.add('active');

                let url = '/data/gallery/semua.json';
                if (category !== 'semua') {
                    url = `/data/gallery/${category}.json`;
                }

                fetchImages(url);
            });
        });
    });
