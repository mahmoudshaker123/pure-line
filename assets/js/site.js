/* ================================================================
   مؤسسة الخط النقي للمقاولات والمصاعد | JavaScript
   ================================================================ */

// Theme toggle (Dark / Light mode)
const themeToggle = document.getElementById('theme-toggle');
const applyTheme = (theme) => {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('pl-theme', theme);
  if (themeToggle) {
    themeToggle.setAttribute('aria-label', theme === 'dark' ? 'تبديل إلى الوضع النهاري' : 'تبديل إلى الوضع الليلي');
    themeToggle.setAttribute('title', theme === 'dark' ? 'الوضع النهاري' : 'الوضع الليلي');
  }
};

themeToggle?.addEventListener('click', () => {
  const current = document.documentElement.getAttribute('data-theme') || 'dark';
  const target = current === 'dark' ? 'light' : 'dark';
  applyTheme(target);
});

// Mobile navigation
const toggle = document.querySelector('.nav-toggle');
const menu = document.querySelector('.nav-menu');
const header = document.querySelector('.site-header');
const backTop = document.querySelector('.back-top');

toggle?.addEventListener('click', () => {
  const open = toggle.getAttribute('aria-expanded') === 'true';
  toggle.setAttribute('aria-expanded', String(!open));
  menu.classList.toggle('is-open', !open);
  document.body.classList.toggle('menu-open', !open);
});

menu?.querySelectorAll('a').forEach((link) => link.addEventListener('click', () => {
  toggle?.setAttribute('aria-expanded', 'false');
  menu.classList.remove('is-open');
  document.body.classList.remove('menu-open');
}));

// Header & back-to-top on scroll
window.addEventListener('scroll', () => {
  const scrolled = window.scrollY > 24;
  header?.classList.toggle('is-scrolled', scrolled);
  backTop?.classList.toggle('is-visible', window.scrollY > 600);
}, { passive: true });

backTop?.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

// Reveal on scroll
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.reveal').forEach((element) => revealObserver.observe(element));

// Counters animation
const counterObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) return;
    const element = entry.target;
    const target = Number(element.dataset.count || 0);
    const started = performance.now();
    const duration = 1200;
    const draw = (now) => {
      const progress = Math.min((now - started) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      element.textContent = Math.round(target * eased);
      if (progress < 1) requestAnimationFrame(draw);
    };
    requestAnimationFrame(draw);
    counterObserver.unobserve(element);
  });
}, { threshold: 0.6 });

document.querySelectorAll('[data-count]').forEach((element) => counterObserver.observe(element));

// FAQ Accordion
document.querySelectorAll('.faq-item__header').forEach((btn) => {
  btn.addEventListener('click', () => {
    const item = btn.closest('.faq-item');
    const isOpen = item.classList.contains('is-open');

    // Close all other FAQs
    document.querySelectorAll('.faq-item.is-open').forEach((other) => {
      if (other !== item) {
        other.classList.remove('is-open');
        other.querySelector('.faq-item__header')?.setAttribute('aria-expanded', 'false');
      }
    });

    item.classList.toggle('is-open', !isOpen);
    btn.setAttribute('aria-expanded', String(!isOpen));
  });
});

// Contact Form -> WhatsApp
const contactForm = document.querySelector('#contact-form');
contactForm?.addEventListener('submit', (event) => {
  event.preventDefault();
  const value = (id) => document.getElementById(id)?.value.trim() || '';
  const name = value('id_name');
  const phone = value('id_phone');
  const email = value('id_email');
  const location = value('id_location');
  const serviceSelect = document.getElementById('id_service');
  const service = serviceSelect ? (serviceSelect.options[serviceSelect.selectedIndex]?.text || serviceSelect.value) : '';
  const message = value('id_message');

  if (!name || !phone || !message) {
    window.alert('من فضلك اكتب الاسم ورقم الجوال وتفاصيل المشروع.');
    return;
  }

  const text = encodeURIComponent(
    `السلام عليكم ورحمة الله وبركاته\n` +
    `طلب استشارة / معاينة من موقع مؤسسة الخط النقي:\n\n` +
    `👤 الاسم: ${name}\n` +
    `📱 رقم الجوال: ${phone}\n` +
    `🏢 الخدمة المطلوبة: ${service && service !== 'اختر الخدمة المطلوبة' ? service : 'غير محدد'}\n` +
    `📍 موقع المشروع: ${location || 'غير محدد'}\n` +
    (email ? `✉️ البريد الإلكتروني: ${email}\n` : '') +
    `📝 تفاصيل الاحتياج:\n${message}\n\n` +
    `شكراً جزيلاً.`
  );

  window.open(`https://wa.me/966506019745?text=${text}`, '_blank', 'noopener');
  contactForm.reset();
});
