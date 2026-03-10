/**
 * Portfolio Main JS — Dark Mode · Scroll Animations · Typing Effect
 * Counters · Skill Filters · Project Modal · Form Validation
 * ES6+ Vanilla JavaScript, no dependencies
 */

'use strict';

// ── DOM Ready ─────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initNavbar();
  initMobileMenu();
  initScrollAnimations();
  initTypingEffect();
  initCounters();
  initSkillFilters();
  initProjectFilters();
  initProjectModals();
  initContactForm();
  initBackToTop();
  autoCloseToasts();
  initMagneticLinks();
  initLenis();
  initCustomCursor();
  if (typeof lucide !== 'undefined') {
    lucide.createIcons();
  }
});


// ── 1. DARK / LIGHT MODE ──────────────────────────────────────
function initTheme() {
  const html = document.documentElement;
  const btn = document.getElementById('theme-toggle');
  const saved = localStorage.getItem('portfolio-theme') || 'dark';

  html.setAttribute('data-theme', saved);

  btn?.addEventListener('click', () => {
    const current = html.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', next);
    localStorage.setItem('portfolio-theme', next);
  });
}


// ── 2. NAVBAR SCROLL ──────────────────────────────────────────
function initNavbar() {
  const navbar = document.getElementById('navbar');
  const navLinks = document.querySelectorAll('.nav-link');
  const sections = document.querySelectorAll('section[id]');
  let lastScrollY = window.scrollY;

  window.addEventListener('scroll', () => {
    const currentScrollY = window.scrollY;
    
    // Scrolled class for shadow
    navbar?.classList.toggle('scrolled', currentScrollY > 50);

    // Auto-hide behavior
    if (currentScrollY > 100 && currentScrollY > lastScrollY) {
      if (!document.getElementById('nav-links')?.classList.contains('open')) {
        navbar?.classList.add('navbar-hidden');
      }
    } else {
      navbar?.classList.remove('navbar-hidden');
    }
    lastScrollY = currentScrollY;

    // Active link tracking
    let currentSection = '';
    sections.forEach(section => {
      const top = section.offsetTop - 100;
      if (currentScrollY >= top) {
        currentSection = section.getAttribute('id');
      }
    });

    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === `#${currentSection}`) {
        link.classList.add('active');
      }
    });
  }, { passive: true });

  // Smooth scroll for nav links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        // Close mobile menu if open
        closeMobileMenu();
      }
    });
  });
}


// ── 3. MOBILE HAMBURGER MENU ──────────────────────────────────
function initMobileMenu() {
  const hamburger = document.getElementById('hamburger');
  const navLinks = document.getElementById('nav-links');

  hamburger?.addEventListener('click', () => {
    const isOpen = navLinks.classList.contains('open');
    if (isOpen) {
      closeMobileMenu();
    } else {
      navLinks.classList.add('open');
      hamburger.classList.add('open');
      hamburger.setAttribute('aria-expanded', 'true');
    }
  });

  // Close on outside click
  document.addEventListener('click', (e) => {
    if (!hamburger?.contains(e.target) && !navLinks?.contains(e.target)) {
      closeMobileMenu();
    }
  });
}

function closeMobileMenu() {
  const hamburger = document.getElementById('hamburger');
  const navLinks = document.getElementById('nav-links');
  navLinks?.classList.remove('open');
  hamburger?.classList.remove('open');
  hamburger?.setAttribute('aria-expanded', 'false');
}


// ── 4. SCROLL REVEAL ANIMATIONS ───────────────────────────────
function initScrollAnimations() {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');

          // Animate skill bars when visible
          if (entry.target.classList.contains('skill-card')) {
            animateSkillBars(entry.target);
            animateSkillRadials(entry.target);
          }

          // Animate counters when stats come into view
          if (entry.target.classList.contains('stat-card')) {
            animateCounter(entry.target);
          }
        }
      });
    },
    { threshold: 0.15, rootMargin: '0px 0px -50px 0px' }
  );

  document.querySelectorAll('.reveal, .reveal-right, .skill-card, .stat-card').forEach(el => {
    observer.observe(el);
  });
}


// ── 5. TYPING EFFECT ──────────────────────────────────────────
function initTypingEffect() {
  const el = document.getElementById('typing-text');
  if (!el) return;

  const phrases = [
    'Développeur Python/Django',
    'Architecte API REST',
    'Expert Django REST Framework',
    'Développeur Flutter',
    'Builder EdTech',
  ];

  let phraseIndex = 0;
  let charIndex = 0;
  let isDeleting = false;
  let isPausing = false;

  function type() {
    if (isPausing) return;

    const currentPhrase = phrases[phraseIndex];

    if (isDeleting) {
      el.textContent = currentPhrase.substring(0, charIndex - 1);
      charIndex--;
    } else {
      el.textContent = currentPhrase.substring(0, charIndex + 1);
      charIndex++;
    }

    let delay = isDeleting ? 60 : 100;

    if (!isDeleting && charIndex === currentPhrase.length) {
      // Pause at end of phrase
      isPausing = true;
      setTimeout(() => {
        isPausing = false;
        isDeleting = true;
        type();
      }, 2000);
      return;
    }

    if (isDeleting && charIndex === 0) {
      isDeleting = false;
      phraseIndex = (phraseIndex + 1) % phrases.length;
      delay = 400;
    }

    setTimeout(type, delay);
  }

  setTimeout(type, 1000);
}


// ── 6. ANIMATED COUNTERS ──────────────────────────────────────
function animateCounter(card) {
  const numberEl = card.querySelector('.counter');
  if (!numberEl || numberEl.classList.contains('animated')) return;
  numberEl.classList.add('animated');

  const target = parseInt(numberEl.getAttribute('data-target'), 10);
  const duration = 2000;
  const start = performance.now();

  function update(currentTime) {
    const elapsed = currentTime - start;
    const progress = Math.min(elapsed / duration, 1);
    // Ease-out cubic
    const eased = 1 - Math.pow(1 - progress, 3);
    const value = Math.floor(eased * target);
    numberEl.textContent = value.toLocaleString('fr-FR');

    if (progress < 1) {
      requestAnimationFrame(update);
    } else {
      numberEl.textContent = target.toLocaleString('fr-FR');
    }
  }

  requestAnimationFrame(update);
}


// ── 7. SKILL BAR ANIMATIONS ───────────────────────────────────
function animateSkillBars(card) {
  const fill = card.querySelector('.skill-bar-fill');
  if (fill && !fill.classList.contains('animated')) {
    fill.classList.add('animated');
    const width = fill.style.getPropertyValue('--skill-width') || '0%';
    fill.style.width = width;
  }
}

function animateSkillRadials(card) {
  const circle = card.querySelector('.skill-progress-circle');
  if (circle && !circle.classList.contains('animated')) {
    circle.classList.add('animated');
    const percent = parseInt(circle.style.getPropertyValue('--skill-percent') || '0', 10);
    const circumference = 2 * Math.PI * 32; // radius=32
    const offset = circumference - (circumference * percent / 100);
    circle.style.strokeDashoffset = offset;
  }
}


// ── 8. SKILL FILTERS ──────────────────────────────────────────
function initSkillFilters() {
  const filterBtns = document.querySelectorAll('.skills-filters .filter-btn');
  const skillCards = document.querySelectorAll('#skills-grid .skill-card');

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      // Update active button
      filterBtns.forEach(b => {
        b.classList.remove('active');
        b.setAttribute('aria-selected', 'false');
      });
      btn.classList.add('active');
      btn.setAttribute('aria-selected', 'true');

      const filter = btn.getAttribute('data-filter');

      skillCards.forEach(card => {
        const category = card.getAttribute('data-category');
        const shouldShow = filter === 'all' || category === filter;
        card.classList.toggle('hidden', !shouldShow);
      });
    });
  });
}


// ── 9. PROJECT FILTERS ────────────────────────────────────────
function initProjectFilters() {
  const filterBtns = document.querySelectorAll('.projects-filters .filter-btn');
  const projectCards = document.querySelectorAll('#projects-grid .project-card');

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => {
        b.classList.remove('active');
        b.setAttribute('aria-selected', 'false');
      });
      btn.classList.add('active');
      btn.setAttribute('aria-selected', 'true');

      const filter = btn.getAttribute('data-filter');

      projectCards.forEach(card => {
        const category = card.getAttribute('data-category');
        const shouldShow = filter === 'all' || category === filter;

        if (shouldShow) {
          card.classList.remove('hidden');
          // Re-trigger reveal animation
          card.classList.remove('visible');
          setTimeout(() => card.classList.add('visible'), 50);
        } else {
          card.classList.add('hidden');
        }
      });
    });
  });
}


// ── 10. PROJECT MODAL ─────────────────────────────────────────
function initProjectModals() {
  const modal = document.getElementById('project-modal');
  const modalContent = document.getElementById('modal-content');
  const closeBtn = document.getElementById('modal-close-btn');

  // Open modal on button click
  document.querySelectorAll('.project-modal-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const data = {
        title: btn.getAttribute('data-title'),
        desc: btn.getAttribute('data-desc'),
        problem: btn.getAttribute('data-problem'),
        solution: btn.getAttribute('data-solution'),
        impact: btn.getAttribute('data-impact'),
        github: btn.getAttribute('data-github'),
        demo: btn.getAttribute('data-demo'),
      };
      openProjectModal(data, modal, modalContent);
    });
  });

  // Close modal
  closeBtn?.addEventListener('click', () => closeModal(modal));
  modal?.addEventListener('click', (e) => {
    if (e.target === modal) closeModal(modal);
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeModal(modal);
  });
}

function openProjectModal(data, modal, content) {
  content.innerHTML = `
    <div class="modal-header">
      <h2 class="modal-title" id="modal-title">${data.title}</h2>
      <p class="modal-desc">${data.desc}</p>
    </div>

    ${data.problem ? `
    <div class="modal-section">
      <h4><i data-lucide="target" class="inline-icon"></i> Problème résolu</h4>
      <p>${data.problem}</p>
    </div>` : ''}

    ${data.solution ? `
    <div class="modal-section">
      <h4><i data-lucide="zap" class="inline-icon"></i> Solution apportée</h4>
      <p>${data.solution}</p>
    </div>` : ''}

    ${data.impact ? `
    <div class="modal-section">
      <h4><i data-lucide="trending-up" class="inline-icon"></i> Impact & Résultats</h4>
      <p>${data.impact}</p>
    </div>` : ''}

    <div class="modal-links">
      ${data.github ? `
      <a href="${data.github}" target="_blank" rel="noopener noreferrer" class="btn btn-ghost">
        <svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/></svg>
        Voir le code
      </a>` : ''}
      ${data.demo ? `
      <a href="${data.demo}" target="_blank" rel="noopener noreferrer" class="btn btn-primary">
        <i data-lucide="external-link" class="inline-icon"></i> Voir la démo
      </a>` : ''}
    </div>
  `;

  modal.removeAttribute('hidden');
  document.body.style.overflow = 'hidden';
  closeBtn?.focus();
  if (typeof lucide !== 'undefined') {
    lucide.createIcons();
  }
}

function closeModal(modal) {
  modal?.setAttribute('hidden', '');
  document.body.style.overflow = '';
}


// ── 11. CONTACT FORM ──────────────────────────────────────────
function initContactForm() {
  const form = document.getElementById('contact-form');
  const submitBtn = document.getElementById('submit-btn');
  if (!form) return;

  form.addEventListener('submit', () => {
    // Show loading state
    const btnText = submitBtn?.querySelector('.btn-text');
    const btnLoading = submitBtn?.querySelector('.btn-loading');
    if (btnText && btnLoading) {
      btnText.setAttribute('hidden', '');
      btnLoading.removeAttribute('hidden');
      submitBtn.disabled = true;
    }
  });
}


// ── 12. BACK TO TOP ───────────────────────────────────────────
function initBackToTop() {
  const btn = document.getElementById('back-to-top');
  btn?.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}


// ── 13. AUTO-CLOSE TOASTS (PREMIUM) ───────────────────────────
function autoCloseToasts() {
  document.querySelectorAll('.premium-toast').forEach(toast => {
    // Auto remove after 5s (matches progress bar animation)
    setTimeout(() => {
      closePremiumToastEl(toast);
    }, 5000);
  });
}

function closePremiumToastEl(toast) {
  if (toast.classList.contains('closing')) return;
  toast.classList.add('closing');
  toast.addEventListener('animationend', () => {
    toast.remove();
  }, { once: true });
}

// Global exposure for the inline onclick handler in HTML
window.closePremiumToast = function(btn) {
  const toast = btn.closest('.premium-toast');
  if (toast) closePremiumToastEl(toast);
};

// ── 15. CUSTOM CURSOR ─────────────────────────────────────────
function initCustomCursor() {
  const cursor = document.querySelector('.custom-cursor');
  const follower = document.querySelector('.custom-cursor-follower');
  if (!cursor || !follower) return;

  if (window.innerWidth < 768) {
    document.body.style.cursor = 'auto'; // Revert on mobile
    return;
  }

  // Only hide default cursor when JS successfully initializes Custom Cursor
  document.body.classList.add('has-custom-cursor');

  let mouseX = 0, mouseY = 0;
  let followerX = 0, followerY = 0;

  document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
    
    // Immediate cursor update
    cursor.style.transform = `translate3d(${mouseX}px, ${mouseY}px, 0) translate(-50%, -50%)`;
  });

  // Smooth follower update
  function animateFollower() {
    followerX += (mouseX - followerX) * 0.10; // Softer spring
    followerY += (mouseY - followerY) * 0.10;
    follower.style.transform = `translate3d(${followerX}px, ${followerY}px, 0) translate(-50%, -50%)`;
    requestAnimationFrame(animateFollower);
  }
  animateFollower();

  // Hover states
  const hoverElements = document.querySelectorAll('a, button, .nav-link, .social-card, .btn');
  hoverElements.forEach(el => {
    el.addEventListener('mouseenter', () => {
      cursor.classList.add('hover');
      follower.classList.add('hover');
    });
    el.addEventListener('mouseleave', () => {
      cursor.classList.remove('hover');
      follower.classList.remove('hover');
    });
  });
}

// ── 16. LENIS SMOOTH SCROLL ───────────────────────────────────
function initLenis() {
  if (typeof Lenis !== 'undefined') {
    const lenis = new Lenis({
      duration: 1.6, // Longer duration for floaty feel
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)), // easeOutExpo
      direction: 'vertical',
      gestureDirection: 'vertical',
      smooth: true,
      mouseMultiplier: 1,
      smoothTouch: false,
      touchMultiplier: 2,
      infinite: false,
    });

    function raf(time) {
      lenis.raf(time);
      requestAnimationFrame(raf);
    }

    requestAnimationFrame(raf);

    // Update smooth scrolling for anchor links to use Lenis
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', (e) => {
        const targetId = anchor.getAttribute('href');
        const target = document.querySelector(targetId);
        if (target) {
          e.preventDefault();
          lenis.scrollTo(target);
          if(typeof closeMobileMenu === 'function') closeMobileMenu();
        }
      });
    });
  }
}

