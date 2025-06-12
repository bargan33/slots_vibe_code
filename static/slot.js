// static/slot.js
import { launchConfetti, screenFlash } from './confetti.js';

const SYMBOLS = ['🍒', '💎', '7️⃣', '🍋', '🔔'];

export function spin() {
  const bet = document.getElementById('bet').value;
  fetch('/slots/spin', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: `bet=${bet}`
  })
    .then(res => res.json())
    .then(data => {
      if (data.error) {
        document.getElementById('message').innerText = data.error;
        return;
      }

      const reels = document.getElementById('reels');
      reels.innerHTML = '';
      const stopSymbols = data.result;

      stopSymbols.forEach((symbol, i) => {
        const reel = document.createElement('div');
        reel.classList.add('reel');
        const inner = document.createElement('div');
        inner.classList.add('reel-inner');

        for (let j = 0; j < 30; j++) {
          const sym = SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)];
          const div = document.createElement('div');
          div.classList.add('symbol');
          div.innerText = sym;
          inner.appendChild(div);
        }

        const final = document.createElement('div');
        final.classList.add('symbol');
        final.innerText = symbol;
        inner.appendChild(final);
        reel.appendChild(inner);
        reels.appendChild(reel);

        setTimeout(() => {
          const offset = -((inner.childElementCount - 1) * 80);
          inner.style.transform = `translateY(${offset}px)`;
        }, i * 300);
      });

      setTimeout(() => {
        document.getElementById('message').innerText = `You won $${data.payout}! Balance: $${data.balance}`;
        if (data.payout >= 10 * parseInt(bet)) {
          screenFlash();
          launchConfetti();
        }
      }, stopSymbols.length * 300 + 800);
    });
};
