document.addEventListener('DOMContentLoaded', () => {
    // --- LOGIKA FORMULIR SUBSCRIBE ---
    const form = document.getElementById('subscribe-form');
    const message = document.getElementById('subscribe-message');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            fetch('/subscribe', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: email })
            })
            .then(response => response.json())
            .then(data => {
                message.textContent = data.message;
                if (data.success) {
                    message.style.color = 'blue';
                    form.reset();
                } else {
                    message.style.color = 'red';
                }
            })
            .catch(error => {
                message.textContent = 'Terjadi kesalahan. Silakan coba lagi.';
                message.style.color = 'red';
                console.error('Error:', error);
            });
        });
    }

    // --- LOGIKA SLIDER GAMBAR OTOMATIS ---
    const imageSliderContainer = document.getElementById('home-image-slider');
    if (imageSliderContainer) {
        fetch('/data/home_gallery.json')
            .then(response => response.json())
            .then(data => {
                if (data.length === 0) {
                    console.error('Tidak ada gambar yang ditemukan dari API.');
                    return;
                }
                data.forEach(image => {
                    const slide = document.createElement('div');
                    slide.className = 'slider-item';
                    const img = document.createElement('img');
                    img.src = image.src;
                    img.alt = image.title;
                    slide.appendChild(img);
                    imageSliderContainer.appendChild(slide);
                });
                let slideIndex = 0;
                const slides = imageSliderContainer.querySelectorAll('.slider-item');
                function showSlides() {
                    if (slides.length === 0) return;
                    for (let i = 0; i < slides.length; i++) { slides[i].style.display = 'none'; }
                    slides[slideIndex].style.display = 'block';
                    slideIndex++;
                    if (slideIndex >= slides.length) { slideIndex = 0; }
                    setTimeout(showSlides, 5000);
                }
                showSlides();
            })
            .catch(error => { console.error('Error fetching home gallery:', error); });
    }

    // --- LOGIKA SLIDER VIDEO GESER MANUAL ---
    const videoSliderContainer = document.getElementById('home-video-slider');
    if (videoSliderContainer) {
        fetch('/data/home_videos.json')
            .then(response => response.json())
            .then(data => {
                if (data.length === 0) {
                    videoSliderContainer.innerHTML = '<p>Belum ada video yang diunggah.</p>';
                    return;
                }
                data.forEach(video => {
                    const videoWrapper = document.createElement('div');
                    videoWrapper.className = 'video-item';
                    const videoElement = document.createElement('video');
                    videoElement.controls = true;
                    videoElement.src = video.full_size_src;
                    const videoTitle = document.createElement('h3');
                    videoTitle.textContent = video.title;
                    videoWrapper.appendChild(videoElement);
                    videoWrapper.appendChild(videoTitle);
                    videoSliderContainer.appendChild(videoWrapper);
                });
                let isDragging = false, startPos = 0, scrollLeft = 0;
                videoSliderContainer.addEventListener('mousedown', (e) => {
                    isDragging = true;
                    videoSliderContainer.classList.add('active-drag');
                    startPos = e.pageX - videoSliderContainer.offsetLeft;
                    scrollLeft = videoSliderContainer.scrollLeft;
                });
                videoSliderContainer.addEventListener('mouseleave', () => { isDragging = false; videoSliderContainer.classList.remove('active-drag'); });
                videoSliderContainer.addEventListener('mouseup', () => { isDragging = false; videoSliderContainer.classList.remove('active-drag'); });
                videoSliderContainer.addEventListener('mousemove', (e) => {
                    if (!isDragging) return;
                    e.preventDefault();
                    const x = e.pageX - videoSliderContainer.offsetLeft;
                    const walk = (x - startPos) * 2;
                    videoSliderContainer.scrollLeft = scrollLeft - walk;
                });
            })
            .catch(error => {
                console.error('Error fetching videos:', error);
                videoSliderContainer.innerHTML = '<p>Gagal memuat video.</p>';
            });
    }

    // --- LOGIKA KUTIPAN HARIAN ---
    const quotes = [
        { quote: "Setiap seniman dulunya adalah seorang amatir.", author: "Ralph Waldo Emerson" },
        { quote: "Seni adalah garis di sekitar pikiranmu.", author: "Gustav Klimt" },
        { quote: "Jadilah dirimu sendiri; semua orang sudah ada.", author: "Oscar Wilde" },
        { quote: "Lukisan adalah puisi bisu, dan puisi adalah lukisan yang berbicara.", author: "Simonides" }
    ];
    const quoteElement = document.getElementById('daily-quote');
    const authorElement = document.getElementById('quote-author');
    if (quoteElement && authorElement) {
        const randomQuote = quotes[Math.floor(Math.random() * quotes.length)];
        quoteElement.textContent = `"${randomQuote.quote}"`;
        authorElement.textContent = `- ${randomQuote.author}`;
    }

    // --- LOGIKA GALERI MINI ---
    const miniGalleryContainer = document.getElementById('mini-gallery');
    if (miniGalleryContainer) {
        fetch('/data/gallery.json') // Mengambil semua gambar dari semua kategori
            .then(response => response.json())
            .then(data => {
                if (data.length === 0) {
                    miniGalleryContainer.innerHTML = '<p>Galeri belum memiliki gambar.</p>';
                    return;
                }

                // Acak urutan gambar dan ambil 9 gambar pertama
                const shuffledImages = data.sort(() => 0.5 - Math.random());
                const selectedImages = shuffledImages.slice(0, 9);

                selectedImages.forEach(image => {
                    const galleryItem = document.createElement('div');
                    galleryItem.className = 'gallery-item';
                    const img = document.createElement('img');
                    img.src = image.src;
                    img.alt = image.title;
                    galleryItem.appendChild(img);
                    miniGalleryContainer.appendChild(galleryItem);
                });
            })
            .catch(error => {
                console.error('Error fetching mini gallery:', error);
                miniGalleryContainer.innerHTML = '<p>Gagal memuat galeri mini.</p>';
            });
    }
});
