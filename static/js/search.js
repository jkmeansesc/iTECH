document.addEventListener("DOMContentLoaded", function() {
    var searchIcon = document.querySelector('.search-trigger.icon-magnifier');
    var searchForm = document.getElementById('search');
    var body = document.body;
    var header = document.querySelector('.header--main');
    var coverLayer = document.querySelector('.cover-layer.search-form-visible');

    // Show or hide search form and cover layer when clicking the search icon
    searchIcon.addEventListener('click', function(event) {
        event.preventDefault();
        searchForm.classList.toggle('is-visible');
        body.classList.toggle('search--visible'); // Toggle body class
        header.classList.toggle('search--visible'); // Toggle header class
        coverLayer.classList.toggle('is-visible'); // Toggle cover layer class
    });

    // Hide search form when clicking elsewhere on the page
    document.addEventListener('click', function(event) {
        // Check if the click event occurred outside the search icon or search form
        if (!searchIcon.contains(event.target) && !searchForm.contains(event.target)) {
            // If the search form is currently visible, hide it
            if (searchForm.classList.contains('is-visible')) {
                searchForm.classList.remove('is-visible');
                body.classList.remove('search--visible'); // Remove body class
                header.classList.remove('search--visible'); // Remove header class
                coverLayer.classList.remove('is-visible'); // Remove cover layer class
            }
        }
    });
});

// hide navigation bar
document.addEventListener('DOMContentLoaded', function() {
    let lastScrollTop = 0;
    const delta = 2 * window.innerHeight / 100;
    window.addEventListener('scroll', function() {
        let currentScroll = window.pageYOffset || document.documentElement.scrollTop;
        const header = document.querySelector('.header--main');

        if (currentScroll > lastScrollTop + delta) {
            header.classList.add('is-hidden'); // hide header
        } else if (currentScroll < lastScrollTop - delta) {
            header.classList.remove('is-hidden'); // present header
        }

        lastScrollTop = currentScroll <= 0 ? 0 : currentScroll;
    });
});