/* ============================================================
   Alpha Tech — Carrito v1
   - localStorage persistente
   - Badge auto-montado en navbars (Solutions + Simulations)
   - Toast de confirmación
   - Hook universal: [data-add-to-cart="SKU"]
   ============================================================ */
(function () {
  'use strict';

  const STORAGE_KEY = 'atech-cart-v1';

  // ============================================================
  // CART MODEL
  // ============================================================
  const Cart = {
    items() {
      try {
        return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
      } catch (e) { return []; }
    },
    save(arr) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(arr));
      this._emit();
    },
    add(p) {
      if (!p || !p.sku) return;
      const arr = this.items();
      const existing = arr.find(i => i.sku === p.sku);
      if (existing) {
        existing.qty += 1;
      } else {
        arr.push({
          sku: p.sku,
          nombre: p.nombre,
          marca: p.marca || '',
          categoria: p.categoria || '',
          precio: Number(p.precio) || 0,
          moneda: p.moneda || 'S/.',
          recurrence: p.recurrence || null,
          modelo: p.modelo || 'Directo',
          img: p.img || null,
          qty: 1
        });
      }
      this.save(arr);
    },
    update(sku, qty) {
      const arr = this.items();
      const item = arr.find(i => i.sku === sku);
      if (!item) return;
      const n = Math.max(0, Math.floor(Number(qty)));
      if (n === 0) {
        this.save(arr.filter(i => i.sku !== sku));
      } else {
        item.qty = n;
        this.save(arr);
      }
    },
    remove(sku) {
      this.save(this.items().filter(i => i.sku !== sku));
    },
    clear() { this.save([]); },
    count() {
      return this.items().reduce((s, i) => s + i.qty, 0);
    },
    total() {
      return this.items().reduce((s, i) => s + (i.precio * i.qty), 0);
    },
    totalRecurring() {
      return this.items()
        .filter(i => i.recurrence)
        .reduce((s, i) => s + (i.precio * i.qty), 0);
    },
    totalOneOff() {
      return this.items()
        .filter(i => !i.recurrence)
        .reduce((s, i) => s + (i.precio * i.qty), 0);
    },
    _listeners: [],
    subscribe(fn) { this._listeners.push(fn); fn(); },
    _emit() { this._listeners.forEach(fn => { try { fn(); } catch (e) {} }); }
  };

  // Sync across tabs
  window.addEventListener('storage', e => {
    if (e.key === STORAGE_KEY) Cart._emit();
  });

  // ============================================================
  // TOAST
  // ============================================================
  function toast(msg, kind) {
    let t = document.getElementById('atech-toast');
    if (!t) {
      t = document.createElement('div');
      t.id = 'atech-toast';
      t.style.cssText = [
        'position:fixed', 'bottom:32px', 'right:32px',
        'background:rgba(0,21,64,.96)', 'color:#FFF',
        'padding:14px 22px', 'border-radius:8px',
        "font-family:'Inter',sans-serif",
        'font-size:13px', 'font-weight:600', 'letter-spacing:.3px',
        'border:1px solid rgba(0,142,170,.4)',
        'box-shadow:0 12px 32px rgba(0,0,0,.45)',
        'z-index:2000', 'opacity:0', 'pointer-events:none',
        'transition:opacity .25s ease, transform .25s ease',
        'transform:translateY(8px)',
        'backdrop-filter:blur(8px)',
        '-webkit-backdrop-filter:blur(8px)',
        'max-width:340px'
      ].join(';');
      document.body.appendChild(t);
    }
    t.textContent = msg;
    if (kind === 'error') {
      t.style.borderColor = 'rgba(254,80,0,.6)';
    } else {
      t.style.borderColor = 'rgba(0,142,170,.4)';
    }
    t.style.opacity = '1';
    t.style.transform = 'translateY(0)';
    clearTimeout(t._timer);
    t._timer = setTimeout(() => {
      t.style.opacity = '0';
      t.style.transform = 'translateY(8px)';
    }, 2400);
  }
  Cart.toast = toast;

  // ============================================================
  // BADGE — auto-mount on any navbar
  // ============================================================
  const BADGE_HTML =
    '<a href="carrito.html" class="cart-badge is-empty" aria-label="Carrito de compras">' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
        '<circle cx="9" cy="21" r="1"/>' +
        '<circle cx="20" cy="21" r="1"/>' +
        '<path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/>' +
      '</svg>' +
      '<span class="cart-badge-count">0</span>' +
    '</a>';

  const BADGE_CSS = `
    .cart-badge {
      position: relative; display: inline-flex;
      align-items: center; justify-content: center;
      width: 38px; height: 38px;
      border: 1px solid rgba(255,255,255,.15);
      border-radius: 8px;
      color: rgba(255,255,255,.8);
      text-decoration: none;
      transition: all .2s ease;
      flex-shrink: 0;
    }
    .cart-badge:hover {
      background: rgba(0,142,170,.12);
      border-color: #008EAA;
      color: #FFF;
    }
    .cart-badge svg { width: 16px; height: 16px; }
    .cart-badge-count {
      position: absolute;
      top: -6px; right: -6px;
      min-width: 18px; height: 18px;
      padding: 0 5px;
      background: #FE5000;
      color: #FFF;
      font-family: 'Rajdhani','Inter',sans-serif;
      font-size: 11px; font-weight: 700;
      border-radius: 100px;
      display: flex; align-items: center; justify-content: center;
      line-height: 1;
    }
    .cart-badge.is-empty .cart-badge-count { display: none; }
    @media (max-width: 900px) {
      .cart-badge { width: 36px; height: 36px; }
    }
  `;

  function injectBadgeStyles() {
    if (document.getElementById('cart-badge-styles')) return;
    const s = document.createElement('style');
    s.id = 'cart-badge-styles';
    s.textContent = BADGE_CSS;
    document.head.appendChild(s);
  }

  function mountBadge() {
    injectBadgeStyles();

    // Solutions navbar — has .nav-right
    const navRight = document.querySelector('nav .nav-right');
    if (navRight && !navRight.querySelector('.cart-badge')) {
      const wrap = document.createElement('div');
      wrap.innerHTML = BADGE_HTML.trim();
      const badge = wrap.firstElementChild;
      const ctaBtn = navRight.querySelector('.nav-cta-btn');
      if (ctaBtn) navRight.insertBefore(badge, ctaBtn);
      else navRight.appendChild(badge);
    }

    // Simulations navbar — has .nav__links (BEM)
    const simNav = document.querySelector('.nav__links');
    if (simNav && !simNav.querySelector('.cart-badge')) {
      const li = document.createElement('li');
      li.style.cssText = 'display:flex;align-items:center';
      li.innerHTML = BADGE_HTML.trim();
      // Insertar antes de .nav-fly o .nav-cta
      const flyA = simNav.querySelector('.nav-fly');
      const ctaA = simNav.querySelector('.nav-cta');
      const target = flyA || ctaA;
      if (target && target.parentElement) {
        simNav.insertBefore(li, target.parentElement);
      } else {
        simNav.appendChild(li);
      }
    }

    // Update on Cart changes
    Cart.subscribe(() => {
      const count = Cart.count();
      document.querySelectorAll('.cart-badge').forEach(b => {
        const span = b.querySelector('.cart-badge-count');
        if (span) span.textContent = count;
        b.classList.toggle('is-empty', count === 0);
      });
    });
  }

  // ============================================================
  // CLICK HOOK — [data-add-to-cart="SKU"]
  // ============================================================
  function handleAddClick(e) {
    const btn = e.target.closest('[data-add-to-cart]');
    if (!btn) return;
    e.preventDefault();

    const sku = btn.dataset.addToCart;
    let p = null;

    // 1) Buscar en window.PRODUCTS si existe (catálogos)
    if (window.PRODUCTS && Array.isArray(window.PRODUCTS)) {
      p = window.PRODUCTS.find(x => x.sku === sku);
    }
    // 2) Fallback: leer del propio botón
    if (!p) {
      p = {
        sku: sku,
        nombre: btn.dataset.nombre || sku,
        marca: btn.dataset.marca || '',
        categoria: btn.dataset.categoria || '',
        precio: parseFloat(btn.dataset.precio || '0'),
        moneda: btn.dataset.moneda || 'S/.',
        recurrence: btn.dataset.recurrence || null,
        modelo: btn.dataset.modelo || 'Directo',
        img: btn.dataset.img || null
      };
    }

    Cart.add(p);
    Cart.toast('✓ ' + p.nombre + ' agregado al carrito');
  }

  // ============================================================
  // INIT
  // ============================================================
  function init() {
    mountBadge();
    document.addEventListener('click', handleAddClick);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Expose
  window.Cart = Cart;
})();
