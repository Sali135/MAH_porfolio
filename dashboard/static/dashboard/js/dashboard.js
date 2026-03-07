/**
 * Dashboard JS — Theme · Sidebar · AJAX toggles · Toasts · Custom Selects
 */
'use strict';

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initSidebar();
  initMobileMenu();
  initCustomSelects();
  initFeaturedToggles();
  initReadToggles();
  autoCloseToasts();
  initRecentProjectsTable();
});


// ── CUSTOM SELECT DROPDOWNS ───────────────────────────────────
function initCustomSelects() {
  // Only wrap selects inside .search-form (toolbars), not form selects
  document.querySelectorAll('.search-form select, .dash-select:not(select.dash-input)').forEach(select => {
    if (select.closest('.custom-select-wrapper')) return; // already wrapped

    // Build wrapper
    const wrapper = document.createElement('div');
    wrapper.className = 'custom-select-wrapper';

    // Get current selected option
    const currentOption = select.options[select.selectedIndex];

    // Trigger button
    const trigger = document.createElement('button');
    trigger.type = 'button';
    trigger.className = 'custom-select-trigger';
    trigger.setAttribute('aria-haspopup', 'listbox');
    trigger.setAttribute('aria-expanded', 'false');
    trigger.innerHTML = `
      <span class="trigger-label">${currentOption ? currentOption.text : 'Sélectionner'}</span>
      <svg class="chevron" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>
    `;

    // Dropdown menu
    const menu = document.createElement('div');
    menu.className = 'custom-select-menu';
    menu.setAttribute('role', 'listbox');

    Array.from(select.options).forEach((opt, i) => {
      const item = document.createElement('div');
      item.className = 'custom-select-option' + (opt.selected ? ' selected' : '');
      item.setAttribute('role', 'option');
      item.setAttribute('aria-selected', opt.selected);
      item.dataset.value = opt.value;
      item.textContent = opt.text;

      item.addEventListener('click', () => {
        // Update native select
        select.value = opt.value;
        // Update trigger label
        trigger.querySelector('.trigger-label').textContent = opt.text;
        // Update selected class
        menu.querySelectorAll('.custom-select-option').forEach(o => {
          o.classList.remove('selected');
          o.setAttribute('aria-selected', 'false');
        });
        item.classList.add('selected');
        item.setAttribute('aria-selected', 'true');
        // Close
        wrapper.classList.remove('open');
        trigger.setAttribute('aria-expanded', 'false');
        // Auto-submit the parent form
        const form = select.closest('form');
        if (form) form.submit();
      });

      menu.appendChild(item);
    });

    // Toggle open
    trigger.addEventListener('click', (e) => {
      e.stopPropagation();
      const isOpen = wrapper.classList.toggle('open');
      trigger.setAttribute('aria-expanded', isOpen);
      // Close other open dropdowns
      document.querySelectorAll('.custom-select-wrapper.open').forEach(w => {
        if (w !== wrapper) {
          w.classList.remove('open');
          w.querySelector('.custom-select-trigger')?.setAttribute('aria-expanded', 'false');
        }
      });
    });

    // Hide native select but keep it in DOM for form submission
    select.classList.add('custom-select-native');
    select.removeAttribute('class');
    select.className = 'custom-select-native';

    // Insert into DOM
    select.parentNode.insertBefore(wrapper, select);
    wrapper.appendChild(select);
    wrapper.appendChild(trigger);
    wrapper.appendChild(menu);
  });

  // Close on outside click
  document.addEventListener('click', () => {
    document.querySelectorAll('.custom-select-wrapper.open').forEach(w => {
      w.classList.remove('open');
      w.querySelector('.custom-select-trigger')?.setAttribute('aria-expanded', 'false');
    });
  });
}



function initTheme() {
  const html = document.documentElement;
  const btn = document.getElementById('theme-toggle-dash');
  const saved = localStorage.getItem('dashboard-theme') || 'dark';
  html.setAttribute('data-theme', saved);

  btn?.addEventListener('click', () => {
    const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', next);
    localStorage.setItem('dashboard-theme', next);
  });
}

// ── SIDEBAR COLLAPSIBLE ───────────────────────────────────────
function initSidebar() {
  const sidebar = document.getElementById('sidebar');
  const toggleBtn = document.getElementById('sidebar-toggle');
  const body = document.getElementById('dash-body');
  const saved = localStorage.getItem('sidebar-collapsed');

  if (saved === 'true') {
    sidebar?.classList.add('collapsed');
  }

  toggleBtn?.addEventListener('click', () => {
    const isCollapsed = sidebar.classList.toggle('collapsed');
    localStorage.setItem('sidebar-collapsed', isCollapsed);
  });
}

// ── MOBILE MENU ───────────────────────────────────────────────
function initMobileMenu() {
  const mobileBtn = document.getElementById('mobile-menu-btn');
  const sidebar = document.getElementById('sidebar');

  mobileBtn?.addEventListener('click', () => {
    sidebar?.classList.toggle('mobile-open');
  });

  // Close on outside click
  document.addEventListener('click', (e) => {
    if (!sidebar?.contains(e.target) && !mobileBtn?.contains(e.target)) {
      sidebar?.classList.remove('mobile-open');
    }
  });
}

// ── AJAX: TOGGLE PROJECT FEATURED ────────────────────────────
function initFeaturedToggles() {
  document.querySelectorAll('.toggle-featured-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
      const projectId = btn.getAttribute('data-project-id');
      try {
        const resp = await csrfFetch(`/dashboard/api/projet/${projectId}/featured/`, 'POST');
        const data = await resp.json();
        btn.classList.toggle('is-featured', data.featured);
        btn.title = data.featured ? 'Retirer vedette' : 'Mettre en vedette';
        if (btn.textContent.includes('Vedette') || btn.textContent.includes('vedette')) {
          btn.textContent = data.featured ? '⭐ Vedette' : '⭐ Mettre en vedette';
        }
        showToast(data.featured ? '⭐ Mis en vedette !' : '✅ Retiré des vedettes.', 'success');
      } catch (e) {
        showToast('❌ Erreur lors de la mise à jour.', 'error');
      }
    });
  });
}

// ── AJAX: TOGGLE MESSAGE READ ─────────────────────────────────
function initReadToggles() {
  document.querySelectorAll('.toggle-read-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
      const msgId = btn.getAttribute('data-msg-id');
      try {
        const resp = await csrfFetch(`/dashboard/api/message/${msgId}/read/`, 'POST');
        const data = await resp.json();
        const row = btn.closest('.msg-admin-row');
        row?.classList.toggle('msg-admin-unread', !data.is_read);
        btn.textContent = data.is_read ? '📧 Non lu' : '✅ Lu';
        const dot = row?.querySelector('.msg-unread-dot');
        if (dot) dot.style.display = data.is_read ? 'none' : 'block';
        showToast(data.is_read ? '✅ Marqué comme lu.' : '📧 Marqué comme non lu.', 'success');
      } catch (e) {
        showToast('❌ Erreur.', 'error');
      }
    });
  });
}

// ── RECENT PROJECTS TABLE (home dashboard) ────────────────────
function initRecentProjectsTable() {
  // This is handled inline in home.html for the featured toggle
  // Extra: highlight unread messages count in sidebar
  const unreadEl = document.querySelector('.nav-badge.unread');
  if (unreadEl && parseInt(unreadEl.textContent) > 0) {
    document.title = `(${unreadEl.textContent}) ${document.title}`;
  }
}

// ── CSRF FETCH HELPER ─────────────────────────────────────────
async function csrfFetch(url, method = 'POST') {
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value
    || getCookie('csrftoken');
  return fetch(url, {
    method,
    headers: {
      'X-CSRFToken': csrfToken,
      'Content-Type': 'application/json',
    },
    credentials: 'same-origin',
  });
}

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return '';
}

// ── TOAST HELPER ─────────────────────────────────────────────
function showToast(msg, type = 'success') {
  let container = document.querySelector('.dash-toasts');
  if (!container) {
    container = document.createElement('div');
    container.className = 'dash-toasts';
    document.body.appendChild(container);
  }
  const toast = document.createElement('div');
  toast.className = `dash-toast dash-toast-${type}`;
  toast.innerHTML = `${msg} <button class="toast-close" onclick="this.parentElement.remove()">×</button>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    toast.style.transition = 'all 0.4s ease';
    setTimeout(() => toast.remove(), 400);
  }, 3500);
}

// ── AUTO-CLOSE SERVER TOASTS ──────────────────────────────────
function autoCloseToasts() {
  document.querySelectorAll('.dash-toast').forEach(toast => {
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100%)';
      toast.style.transition = 'all 0.4s ease';
      setTimeout(() => toast.remove(), 400);
    }, 5000);
  });
}
