document.addEventListener('DOMContentLoaded', function() {
    const slides = document.querySelectorAll('.slide');
    let currentIndex = 0;

    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.classList.remove('active');
            if (i === index) {
                slide.classList.add('active');
            }
        });
    }

    document.getElementById('moveRight').addEventListener('click', function() {
        currentIndex = (currentIndex + 1) % slides.length; // Увеличиваем индекс и переходим в начало, если это последний слайд.
        showSlide(currentIndex);
    });

    document.getElementById('moveLeft').addEventListener('click', function() {
        currentIndex = (currentIndex - 1 + slides.length) % slides.length; // Уменьшаем индекс и переходим в конец, если это первый слайд.
        showSlide(currentIndex);
    });

    showSlide(currentIndex); // Показываем первый слайд изначально.
});