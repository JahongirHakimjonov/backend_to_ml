(function () {
    'use strict';

    var LANGS = [
        { code: 'uz', label: "O'zbek", prefix: '' },
        { code: 'ru', label: 'Русский', prefix: '/ru' },
        { code: 'en', label: 'English', prefix: '/en' }
    ];

    var currentLang = (document.documentElement.lang || 'uz').toLowerCase();
    var currentCfg = LANGS.find(function (l) { return l.code === currentLang; }) || LANGS[0];

    function pathWithoutPrefix() {
        var p = window.location.pathname;
        if (currentCfg.prefix && p.startsWith(currentCfg.prefix + '/')) {
            p = p.slice(currentCfg.prefix.length);
        } else if (currentCfg.prefix && p === currentCfg.prefix) {
            p = '/';
        }
        return p || '/';
    }

    function buildSwitcher() {
        var path = pathWithoutPrefix();
        var container = document.createElement('div');
        container.className = 'lang-switcher-wrapper';

        var select = document.createElement('select');
        select.className = 'lang-switcher';
        select.setAttribute('aria-label', 'Tilni tanlash / Выбор языка / Language');
        select.style.cssText = [
            'margin: 0 0.5rem',
            'padding: 0.3rem 0.5rem',
            'background: transparent',
            'color: inherit',
            'border: 1px solid currentColor',
            'border-radius: 4px',
            'cursor: pointer',
            'font-size: 0.85rem',
            'font-family: inherit'
        ].join(';');

        LANGS.forEach(function (l) {
            var opt = document.createElement('option');
            opt.value = l.prefix + path;
            opt.textContent = l.label;
            if (l.code === currentLang) opt.selected = true;
            // option fonida light theme bo'lishi uchun
            opt.style.color = '#000';
            opt.style.background = '#fff';
            select.appendChild(opt);
        });

        select.addEventListener('change', function (e) {
            var target = e.target.value;
            var picked = LANGS.find(function (l) { return (l.prefix + path) === target; });
            if (picked) {
                try { localStorage.setItem('preferred-lang', picked.code); } catch (_) { /* ignore */ }
            }
            window.location.href = target;
        });

        container.appendChild(select);
        return container;
    }

    function inject() {
        var target = document.querySelector('.right-buttons') || document.querySelector('.menu-bar');
        if (!target) return;
        if (target.querySelector('.lang-switcher-wrapper')) return;
        target.appendChild(buildSwitcher());
    }

    function maybeRedirectToPreferred() {
        // Faqat uz home (default) sahifada
        if (currentLang !== 'uz') return;
        var p = window.location.pathname;
        if (p !== '/' && p !== '/index.html' && p !== '') return;
        if (sessionStorage.getItem('lang-auto-redirected')) return;

        var preferred;
        try { preferred = localStorage.getItem('preferred-lang'); } catch (_) { return; }
        if (!preferred || preferred === 'uz') return;

        var cfg = LANGS.find(function (l) { return l.code === preferred; });
        if (!cfg) return;
        sessionStorage.setItem('lang-auto-redirected', '1');
        window.location.replace(cfg.prefix + '/');
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () {
            inject();
            maybeRedirectToPreferred();
        });
    } else {
        inject();
        maybeRedirectToPreferred();
    }
})();
