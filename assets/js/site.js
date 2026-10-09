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

window.addEventListener('scroll', () => {
  header?.classList.toggle('is-scrolled', window.scrollY > 24);
  backTop?.classList.toggle('is-visible', window.scrollY > 600);
}, { passive: true });

backTop?.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.reveal').forEach((element) => revealObserver.observe(element));

const counterObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) return;
    const element = entry.target;
    const target = Number(element.dataset.count || 0);
    const started = performance.now();
    const duration = 1100;
    const draw = (now) => {
      const progress = Math.min((now - started) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      element.textContent = Math.round(target * eased);
      if (progress < 1) requestAnimationFrame(draw);
    };
    requestAnimationFrame(draw);
    counterObserver.unobserve(element);
  });
}, { threshold: 0.7 });

document.querySelectorAll('[data-count]').forEach((element) => counterObserver.observe(element));

const contactForm = document.querySelector('#contact-form');
contactForm?.addEventListener('submit', (event) => {
  event.preventDefault();
  const value = (id) => document.getElementById(id)?.value.trim() || '';
  const name = value('id_name');
  const phone = value('id_phone');
  const email = value('id_email');
  const location = value('id_location');
  const service = value('id_service');
  const message = value('id_message');

  if (!name || !phone || !message) {
    window.alert('من فضلك اكتب الاسم ورقم الجوال وتفاصيل المشروع.');
    return;
  }

  const text = encodeURIComponent(
    `طلب جديد من الموقع\nالاسم: ${name}\nالجوال: ${phone}\nالبريد: ${email || '-'}\n` +
    `الخدمة: ${service || '-'}\nالموقع: ${location || '-'}\nالتفاصيل: ${message}`
  );
  window.open(`https://wa.me/966534201283?text=${text}`, '_blank', 'noopener');
  contactForm.reset();
});
