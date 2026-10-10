const revealItems = document.querySelectorAll('.reveal-up');
const navLinks = document.querySelectorAll('.nav-link');
const sections = document.querySelectorAll('section[id], header[id]');
const counters = document.querySelectorAll('[data-counter]');
const form = document.getElementById('contactForm');
const formMessage = document.getElementById('formMessage');

const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.18 });

revealItems.forEach((item) => revealObserver.observe(item));

const activateNav = () => {
  let currentId = '';

  sections.forEach((section) => {
    const top = window.scrollY;
    const offsetTop = section.offsetTop - 140;
    const height = section.offsetHeight;

    if (top >= offsetTop && top < offsetTop + height) {
      currentId = section.id;
    }
  });

  navLinks.forEach((link) => {
    link.classList.toggle('active', link.getAttribute('href') === `#${currentId}`);
  });
};

window.addEventListener('scroll', activateNav);
window.addEventListener('load', activateNav);

const counterObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) {
      return;
    }

    const target = entry.target;
    const endValue = Number(target.dataset.counter);
    let current = 0;
    const step = Math.max(1, Math.ceil(endValue / 40));

    const timer = window.setInterval(() => {
      current += step;
      if (current >= endValue) {
        current = endValue;
        window.clearInterval(timer);
      }
      target.textContent = `${current}%`;
    }, 30);

    counterObserver.unobserve(target);
  });
}, { threshold: 0.5 });

counters.forEach((counter) => counterObserver.observe(counter));

if (form) {
  form.addEventListener('submit', (event) => {
    event.preventDefault();

    const name = document.getElementById('name').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const service = document.getElementById('service').value.trim();
    const message = document.getElementById('message').value.trim();

    if (!name || !phone || !service || !message) {
      formMessage.textContent = 'من فضلك أكمل كل البيانات المطلوبة.';
      return;
    }

    const whatsappText = encodeURIComponent(
      `السلام عليكم، اسمي ${name}\nرقم الجوال: ${phone}\nالخدمة المطلوبة: ${service}\nتفاصيل الطلب: ${message}`
    );

    formMessage.textContent = 'تم تجهيز الطلب، وسيتم تحويلك إلى واتساب.';
    window.open(`https://wa.me/966506019745?text=${whatsappText}`, '_blank', 'noopener');
    form.reset();
  });
}
