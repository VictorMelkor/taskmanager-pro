    document.addEventListener('DOMContentLoaded', () => {
    const track = document.querySelector('.carousel-track');
    const slides = Array.from(track.children);
    const prevButton = document.querySelector('.carousel-btn.prev');
    const nextButton = document.querySelector('.carousel-btn.next');

    let currentIndex = slides.findIndex(slide => slide.classList.contains('current-slide'));

    function updateSlide(newIndex) {
        slides[currentIndex].classList.remove('current-slide');
        slides[newIndex].classList.add('current-slide');
        currentIndex = newIndex;
    }

    prevButton.addEventListener('click', () => {
        let newIndex = currentIndex - 1;
        if (newIndex < 0) newIndex = slides.length - 1;
        updateSlide(newIndex);
    });

    nextButton.addEventListener('click', () => {
        let newIndex = currentIndex + 1;
        if (newIndex >= slides.length) newIndex = 0;
        updateSlide(newIndex);
    });
    });
