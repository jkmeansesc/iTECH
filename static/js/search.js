document.addEventListener("DOMContentLoaded", function() {
    var searchIcon = document.querySelector('.search-trigger.icon-magnifier');
    var searchForm = document.getElementById('search');
    var body = document.body;
    var header = document.querySelector('.header--main');
    var coverLayer = document.querySelector('.cover-layer.search-form-visible');

    // 点击搜索按钮时显示或隐藏搜索栏和覆盖层
    searchIcon.addEventListener('click', function(event) {
        event.preventDefault();
        searchForm.classList.toggle('is-visible');
        body.classList.toggle('search--visible'); // 切换 body 类
        header.classList.toggle('search--visible'); // 切换 header 类
        coverLayer.classList.toggle('is-visible'); // 切换覆盖层类
    });

    // 点击页面其他地方时隐藏搜索栏
    document.addEventListener('click', function(event) {
        // 检查点击事件是否发生在搜索按钮或搜索栏内部
        if (!searchIcon.contains(event.target) && !searchForm.contains(event.target)) {
            // 如果搜索栏当前可见，则隐藏
            if (searchForm.classList.contains('is-visible')) {
                searchForm.classList.remove('is-visible');
                body.classList.remove('search--visible'); // 移除 body 类
                header.classList.remove('search--visible'); // 移除 header 类
                coverLayer.classList.remove('is-visible'); // 移除覆盖层类
            }
        }
    });
});
