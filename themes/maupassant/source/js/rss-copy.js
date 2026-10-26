/*点击导航栏的 RSS，复制订阅地址到剪贴板并提示*/
!function (window, document) {
    var link = document.getElementById('rss-copy');
    if (!link) return;

    var toastTimer;
    function showToast(html, duration) {
        var toast = document.getElementById('rss-toast');
        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'rss-toast';
            toast.setAttribute('role', 'status');
            toast.setAttribute('aria-live', 'polite');
            document.body.appendChild(toast);
        }
        toast.innerHTML = html;
        // 强制回流，保证每次点击都重新播放动画
        toast.className = '';
        void toast.offsetWidth;
        toast.className = 'show';
        clearTimeout(toastTimer);
        toastTimer = setTimeout(function () {
            toast.className = '';
        }, duration);
    }

    function fallbackCopy(text) {
        var textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.setAttribute('readonly', '');
        textarea.style.position = 'fixed';
        textarea.style.top = '-1000px';
        document.body.appendChild(textarea);
        textarea.select();
        var ok = false;
        try {
            ok = document.execCommand('copy');
        } catch (e) {}
        document.body.removeChild(textarea);
        return ok;
    }

    function copy(text) {
        if (navigator.clipboard && window.isSecureContext) {
            return navigator.clipboard.writeText(text).then(function () {
                return true;
            }, function () {
                return fallbackCopy(text);
            });
        }
        return Promise.resolve(fallbackCopy(text));
    }

    link.addEventListener('click', function (event) {
        // 保留 Cmd/Ctrl/Shift/中键点击的默认行为（新标签页打开订阅源）
        if (event.metaKey || event.ctrlKey || event.shiftKey || event.button !== 0) return;
        event.preventDefault();

        var feed = link.getAttribute('data-feed') || link.href;
        copy(feed).then(function (ok) {
            if (ok) {
                showToast('<strong>RSS 地址已复制</strong><span>粘贴到你常用的阅读器即可订阅</span><code>' + feed + '</code>', 3000);
            } else {
                showToast('<strong>复制失败，请手动复制</strong><code>' + feed + '</code>', 6000);
            }
        });
    });
}(window, document);
