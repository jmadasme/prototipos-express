/**
 * PrototiposExpress — Main JavaScript
 * Handles navigation, scroll animations, form submission
 */

'use strict';

// ============================================================
// DOM Ready
// ============================================================
document.addEventListener('DOMContentLoaded', () => {
  initNavbar();
  initScrollAnimations();
  initContactForm();
  initSmoothScroll();
});

// ============================================================
// Navbar — Toggle & Scroll Effect
// ============================================================
function initNavbar() {
  const navbar = document.getElementById('navbar');
  const navToggle = document.getElementById('navToggle');
  const navMenu = document.getElementById('navMenu');
  const navLinks = document.querySelectorAll('.nav-link');

  // Toggle mobile menu
  navToggle.addEventListener('click', () => {
    navMenu.classList.toggle('active');
    const icon = navToggle.querySelector('i');
    icon.classList.toggle('fa-bars');
    icon.classList.toggle('fa-times');
  });

  // Close menu on link click (mobile)
  navLinks.forEach((link) => {
    link.addEventListener('click', () => {
      navMenu.classList.remove('active');
      const icon = navToggle.querySelector('i');
      icon.classList.add('fa-bars');
      icon.classList.remove('fa-times');
    });
  });

  // Navbar background on scroll
  const handleScroll = () => {
    if (window.scrollY > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  };

  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll(); // initial check
}

// ============================================================
// Intersection Observer — Scroll Animations
// ============================================================
function initScrollAnimations() {
  const animatedElements = document.querySelectorAll('.animate-on-scroll');

  if (!('IntersectionObserver' in window)) {
    // Fallback: show all elements immediately
    animatedElements.forEach((el) => el.classList.add('visible'));
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          // Optionally keep observing to re-trigger? No, we only animate once.
          observer.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.15,
      rootMargin: '0px 0px -60px 0px',
    }
  );

  animatedElements.forEach((el) => observer.observe(el));

  // Also handle hero fade-up elements (they may need visibility too)
  const heroElements = document.querySelectorAll('.animate-fade-up');
  heroElements.forEach((el) => el.classList.add('visible'));
}

// ============================================================
// Smooth Scroll for anchor links (fallback)
// ============================================================
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', (e) => {
      const targetId = anchor.getAttribute('href');
      if (targetId === '#') return;
      const target = document.querySelector(targetId);
      if (!target) return;

      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });
}

// ============================================================
// Contact Form — Validation & Submission
// ============================================================
function initContactForm() {
  const form = document.getElementById('contactForm');
  const submitBtn = document.getElementById('submitBtn');
  const formMessage = document.getElementById('formMessage');

  if (!form) return;

  // Real-time validation on blur for better UX
  const inputs = form.querySelectorAll('input, textarea');
  inputs.forEach((input) => {
    input.addEventListener('blur', () => validateField(input));
    input.addEventListener('input', () => {
      // Clear error while typing
      const errorEl = document.getElementById(`error-${input.name}`);
      if (errorEl) {
        errorEl.textContent = '';
      }
      input.classList.remove('error');
    });
  });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Reset message
    formMessage.className = 'form-message';
    formMessage.textContent = '';
    formMessage.style.display = 'none';

    // Validate all fields
    let isValid = true;
    const fields = [
      { id: 'nombre' },
      { id: 'email' },
      { id: 'telefono' },
      { id: 'empresa' },
      { id: 'necesidad' },
      { id: 'plazo' },
    ];

    fields.forEach((field) => {
      const input = document.getElementById(field.id);
      if (!validateField(input)) {
        isValid = false;
      }
    });

    if (!isValid) {
      // Scroll to first error
      const firstError = form.querySelector('.error');
      if (firstError) {
        firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        firstError.focus();
      }
      return;
    }

    // Build FormData for Netlify Forms
    const formData = new FormData(form);

    // Show loading state
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Enviando...';
    formMessage.className = 'form-message loading';
    formMessage.textContent = 'Enviando tu solicitud...';
    formMessage.style.display = 'block';

    try {
      // Enviar a Netlify Forms (AJAX)
      const response = await fetch('/', {
        method: 'POST',
        body: new URLSearchParams(formData).toString(),
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      });

      if (response.ok) {
        formMessage.className = 'form-message success';
        formMessage.textContent =
          '¡Solicitud enviada con éxito! Te contactaremos en un máximo de 24 horas para agendar tu reunión sin costo.';
        form.reset();
      } else {
        throw new Error('Error al enviar la solicitud');
      }
    } catch (err) {
      formMessage.className = 'form-message error';
      formMessage.textContent =
        err.message === 'Failed to fetch'
          ? 'No se pudo conectar con el servidor. Por favor, intenta nuevamente.'
          : err.message || 'Ocurrió un error al enviar tu solicitud. Por favor, intenta nuevamente.';
    } finally {
      submitBtn.disabled = false;
      submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Enviar solicitud';
      formMessage.style.display = 'block';
    }
  });
}

// ============================================================
// Field Validation
// ============================================================
function validateField(input) {
  const value = input.value.trim();
  const errorEl = document.getElementById(`error-${input.name}`);
  let errorMsg = '';

  // Reset
  input.classList.remove('error');
  if (errorEl) errorEl.textContent = '';

  if (input.hasAttribute('required') && !value) {
    errorMsg = 'Este campo es obligatorio';
  } else if (value) {
    switch (input.name) {
      case 'email':
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
          errorMsg = 'Ingresa un correo electrónico válido';
        }
        break;
      case 'telefono':
        if (!/^[\d\s+()-]{7,20}$/.test(value)) {
          errorMsg = 'Ingresa un teléfono válido (mín. 7 dígitos)';
        }
        break;
      case 'plazo':
        {
          const selectedDate = new Date(value);
          const today = new Date();
          today.setHours(0, 0, 0, 0);
          if (selectedDate <= today) {
            errorMsg = 'La fecha debe ser posterior a hoy';
          }
        }
        break;
    }
  }

  if (errorMsg) {
    input.classList.add('error');
    if (errorEl) errorEl.textContent = errorMsg;
    return false;
  }

  return true;
}
