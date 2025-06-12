// static/confetti.js

export function launchConfetti() {
  const canvas = document.getElementById('confetti-canvas');
  const ctx = canvas.getContext('2d');
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  canvas.style.opacity = 1;

  const pieces = Array.from({ length: 100 }, () => ({
    x: Math.random() * canvas.width,
    y: Math.random() * -canvas.height,
    r: Math.random() * 6 + 4,
    d: Math.random() * 10 + 2,
    color: `hsl(${Math.random() * 360}, 100%, 50%)`,
    tilt: Math.random() * 10 - 5
  }));

  let frame = 0;
  let running = true;

  function draw() {
    if (!running) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let p of pieces) {
      ctx.beginPath();
      ctx.fillStyle = p.color;
      ctx.ellipse(p.x + p.tilt, p.y, p.r, p.r * 0.4, 0, 0, 2 * Math.PI);
      ctx.fill();
      p.y += p.d;
      p.tilt += Math.random() - 0.5;
    }

    if (++frame < 150) requestAnimationFrame(draw);
  }

  draw();

  setTimeout(() => {
    canvas.style.opacity = 0;
    running = false;
    setTimeout(() => ctx.clearRect(0, 0, canvas.width, canvas.height), 500);
  }, 2000);
}

export function screenFlash() {
  const flash = document.getElementById('flash');
  flash.style.opacity = 1;
  setTimeout(() => {
    flash.style.opacity = 0;
  }, 150);
}