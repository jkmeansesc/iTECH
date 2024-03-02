document.addEventListener("DOMContentLoaded", function() {
    var hasChildrenItems = document.querySelectorAll('.s-header__nav li.has-children');

    hasChildrenItems.forEach(function(item) {
        item.addEventListener('mouseenter', function() {
            var subMenu = this.querySelector('.sub-menu');
            if (subMenu) {
                subMenu.style.display = 'block';
            }
        });

        item.addEventListener('mouseleave', function() {
            var subMenu = this.querySelector('.sub-menu');
            if (subMenu) {
                subMenu.style.display = 'none';
            }
        });
    });
});