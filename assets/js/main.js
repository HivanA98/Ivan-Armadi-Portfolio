/* ============================================================
 * main.js — lapisan interaksi dinamis
 * Prinsip refactor: SEMUA class animasi disuntikkan lewat JS
 * saat runtime, sehingga markup konten di index.html tidak
 * perlu diubah sama sekali.
 * ============================================================ */
(() => {
    'use strict';

    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    document.addEventListener('DOMContentLoaded', () => {
        document.body.classList.add('js-ready');

        initScrollProgress();
        initHeaderState();
        initMobileNav();
        initScrollSpy();
        initScrollReveal();
        initProjectFilter();
        initBackToTop();
    });

    /* --- 1. Progress bar scroll --- */
    function initScrollProgress() {
        const bar = document.createElement('div');
        bar.className = 'scroll-progress';
        bar.setAttribute('aria-hidden', 'true');
        document.body.prepend(bar);

        const update = () => {
            const doc = document.documentElement;
            const max = doc.scrollHeight - doc.clientHeight;
            bar.style.width = max > 0 ? `${(doc.scrollTop / max) * 100}%` : '0%';
        };
        window.addEventListener('scroll', update, { passive: true });
        update();
    }

    /* --- 2. Header mengecil saat scroll --- */
    function initHeaderState() {
        const header = document.querySelector('header');
        if (!header) return;
        const update = () => header.classList.toggle('scrolled', window.scrollY > 40);
        window.addEventListener('scroll', update, { passive: true });
        update();
    }

    /* --- 3. Hamburger menu mobile (nav sebelumnya hilang di <=968px) --- */
    function initMobileNav() {
        const header = document.querySelector('header');
        const nav = header && header.querySelector('nav');
        if (!header || !nav) return;

        const toggle = document.createElement('button');
        toggle.className = 'nav-toggle';
        toggle.setAttribute('aria-label', 'Buka menu navigasi');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.innerHTML = '<i class="fas fa-bars" aria-hidden="true"></i>';
        header.appendChild(toggle);

        const setOpen = (open) => {
            nav.classList.toggle('open', open);
            toggle.setAttribute('aria-expanded', String(open));
            toggle.innerHTML = open
                ? '<i class="fas fa-times" aria-hidden="true"></i>'
                : '<i class="fas fa-bars" aria-hidden="true"></i>';
        };

        toggle.addEventListener('click', () => setOpen(!nav.classList.contains('open')));
        nav.addEventListener('click', (e) => {
            if (e.target.closest('a')) setOpen(false); // tutup setelah memilih menu
        });
        window.addEventListener('resize', () => {
            if (window.innerWidth > 968) setOpen(false);
        });
    }

    /* --- 4. Scrollspy: tandai link nav sesuai section terlihat --- */
    function initScrollSpy() {
        const links = Array.from(document.querySelectorAll('nav ul li a[href^="#"]'));
        if (!links.length) return;

        const targets = links
            .map((link) => document.querySelector(link.getAttribute('href')))
            .filter(Boolean);

        const setActive = (id) => {
            links.forEach((l) =>
                l.classList.toggle('active', l.getAttribute('href') === `#${id}`)
            );
        };

        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) setActive(entry.target.id);
                });
            },
            { rootMargin: '-40% 0px -55% 0px' }
        );
        targets.forEach((t) => observer.observe(t));
    }

    /* --- 5. Scroll reveal: class disuntikkan runtime, markup utuh --- */
    function initScrollReveal() {
        if (prefersReducedMotion || !('IntersectionObserver' in window)) return;

        const groups = [
            { selector: '.section-padding > h2, .section-padding .section-header', stagger: 0 },
            { selector: '.about-grid > *', stagger: 120 },
            { selector: '.skill-card', stagger: 100 },
            { selector: '.edu-card', stagger: 120 },
            { selector: '.project-card', stagger: 90 },
            { selector: '.cert-card', stagger: 110 },
            { selector: '.contact-grid > *', stagger: 130 },
        ];

        groups.forEach(({ selector, stagger }) => {
            document.querySelectorAll(selector).forEach((el, i) => {
                el.classList.add('reveal');
                el.style.setProperty('--reveal-delay', `${(i % 4) * stagger}ms`);
            });
        });

        // Timeline pengalaman: masuk dari sisi kiri/kanan sesuai posisinya
        document.querySelectorAll('.timeline-item').forEach((el) => {
            el.classList.add('reveal', el.classList.contains('left') ? 'from-left' : 'from-right');
        });

        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('is-visible');
                        observer.unobserve(entry.target); // sekali tampil, selesai
                    }
                });
            },
            { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
        );
        document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));
    }

    /* --- 6. Filter proyek dengan transisi fade/scale (logika lama dipertahankan) --- */
    function initProjectFilter() {
        const filterBtns = document.querySelectorAll('.filter-btn');
        const projects = document.querySelectorAll('.project-card');
        if (!filterBtns.length || !projects.length) return;

        const HIDE_MS = prefersReducedMotion ? 0 : 350;

        filterBtns.forEach((btn) => {
            btn.addEventListener('click', () => {
                filterBtns.forEach((b) => b.classList.remove('active'));
                btn.classList.add('active');

                const filterValue = btn.getAttribute('data-filter');

                projects.forEach((project) => {
                    const match =
                        filterValue === 'all' ||
                        project.getAttribute('data-category') === filterValue;

                    if (match) {
                        project.classList.remove('filter-gone');
                        // paksa reflow agar transisi fade-in berjalan
                        void project.offsetWidth;
                        project.classList.remove('filter-hide');
                    } else {
                        project.classList.add('filter-hide');
                        setTimeout(() => {
                            if (project.classList.contains('filter-hide')) {
                                project.classList.add('filter-gone');
                            }
                        }, HIDE_MS);
                    }
                });
            });
        });
    }

    /* --- 7. Tombol kembali ke atas --- */
    function initBackToTop() {
        const btn = document.createElement('button');
        btn.className = 'back-to-top';
        btn.setAttribute('aria-label', 'Kembali ke atas');
        btn.innerHTML = '<i class="fas fa-arrow-up" aria-hidden="true"></i>';
        document.body.appendChild(btn);

        const update = () => btn.classList.toggle('visible', window.scrollY > 600);
        window.addEventListener('scroll', update, { passive: true });
        update();

        btn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: prefersReducedMotion ? 'auto' : 'smooth' });
        });
    }
})();
