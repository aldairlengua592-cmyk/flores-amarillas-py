"""Regalo de flores amarillas. Ejecutar: python -m streamlit run app.py."""
from pathlib import Path
import base64
import json
import re

import streamlit as st

# PERSONALIZA TU REGALO AQUI
NOMBRE = "Ari"
MENSAJE = "Estas flores amarillas son para ti, porque quería regalarte algo que pudiera transmitir un poquito de lo especial que eres para mí. 💛"
NOMBRE_CANCION = "Una canción para ti"
FRASE_INICIAL = "🌻 Tengo un pequeño regalo para ti..."
COLOR_PRINCIPAL = "#f3cd63"
VOLUMEN = 0.05  # De 0 (silencio) a 1 (máximo).
ARCHIVO_AUDIO = "cancion.mp3"  # Archivo junto a app.py; None desactiva la música.
BASE_DIR = Path(__file__).resolve().parent

# La interfaz del navegador está integrada en Python para conservar sus animaciones.
HTML = r"""<!doctype html>
<html lang="es">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#101f1b">
  <meta name="description" content="Un pequeño regalo de flores amarillas, hecho con mucho cariño.">
  <title>Flores para ti · Un regalo especial</title>
</head>

<body>
  <div class="ambient" aria-hidden="true"></div>
  <div id="particles" aria-hidden="true"></div>
  <header class="masthead"><span class="brand">✳ &nbsp; FLORES PARA TI</span><span class="header-note">un detalle, con
      mucho
      cariño</span></header>

  <main>
    <section id="intro" class="intro" aria-labelledby="intro-title">
      <div class="gift-seal" aria-hidden="true">✿</div>
      <p class="eyebrow">HAY COSAS QUE SE DICEN CON FLORES</p>
      <h1 id="intro-title">🌻 Tengo un pequeño regalo para ti...</h1>
      <p class="intro-copy">Un poquito de sol.<br>Y todo el cariño que cabe en un detalle.</p>
      <button id="discover" class="primary" type="button">Descubrir mi regalo</button>
      <p class="small-note">Hecho para sacarte una sonrisa</p>
    </section>

    <section id="gift" class="gift" aria-labelledby="gift-title" hidden>
      <div class="gift-heading">
        <p class="eyebrow">UN PEDACITO DE SOL, SOLO PARA TI</p>
        <h2 id="gift-title" tabindex="-1">Para ti, <span id="recipient"></span></h2>
      </div>

      <div class="gift-layout">
        <div class="bouquet-column">
          <p class="bouquet-label">que estas flores te regalen una sonrisa</p>
        <div class="bouquet-area">
          <span class="orbit orbit-one" aria-hidden="true"></span>
          <span class="orbit orbit-two" aria-hidden="true"></span>
          <button id="bouquet" class="bouquet" type="button"
            aria-label="Arreglo de nueve flores amarillas. Pulsa para enviar corazones.">
            <!-- Flores, pétalos, hojas y tallos creados con elementos HTML en script.js. -->
            <span class="ribbon" aria-hidden="true"><i></i><b>con mucho cariño</b></span>
          </button>
          <p class="touch-hint">✧ &nbsp; Toca las flores, tienen un poquito de magia</p>
        </div>
        </div>

        <div class="letter-column">
          <article class="letter">
            <span class="letter-mark" aria-hidden="true">❝</span>
            <p class="eyebrow">ALGO QUE QUERÍA DECIRTE</p>
            <p id="message" class="message"></p>
            <div class="signature"><span>Con mucho cariño</span><span aria-hidden="true">♡</span></div>
          </article>

          <section class="music" aria-label="Canción del regalo">
            <div class="music-heading"><span class="record" aria-hidden="true">♫</span>
              <div>
                <h3 id="song-title"></h3>
              </div>
            </div>
            <!-- Sin src: no se solicita ni se reproduce ningún archivo hasta configurarlo. -->
            <audio id="audio" preload="none" loop></audio>
            <div class="player-controls"><button id="play" type="button" disabled>▶ Reproducir</button><span
                id="time">0:00 / 0:00</span></div>
            <label class="sr-only" for="progress">Progreso de la canción</label>
            <input id="progress" type="range" min="0" max="100" value="0" step="0.1" disabled>
            <p id="music-status" class="music-status" role="status">Tu canción está lista para acompañar este regalo.
            </p>
          </section>
        </div>
      </div>
      <footer>Estas flores no se marchitan. <span>Porque algunos detalles merecen durar.</span> <b>💛</b></footer>
    </section>
  </main>
  <noscript>
    <p class="no-script">Activa JavaScript para abrir tu regalo y ver florecer este ramo.</p>
  </noscript>
</body>

</html>"""

CSS = r"""  /* PERSONALIZACIÓN: cambia este color por tu tono favorito. */
:root { --primary: #f3cd63; --background: #101f1b; --cream: #f8f0da; --muted: #a9b5a6; }
* { box-sizing: border-box; }
html { overflow-x: clip; overscroll-behavior-x: none; -webkit-text-size-adjust: 100%; text-size-adjust: 100%; }
body { margin: 0; width: 100%; min-height: 100svh; overflow-x: clip; background: var(--background); color: var(--cream); font-family: 'Segoe UI', sans-serif; }
main, .gift-layout > *, .music-heading > div { min-width: 0; }
h1, h2, h3, .message, .music-status { overflow-wrap: anywhere; }
button { touch-action: manipulation; }
button, input { font: inherit; }
button { cursor: pointer; }
button:disabled { cursor: default; opacity: .5; }
button:focus-visible, input:focus-visible { outline: 2px solid var(--primary); outline-offset: 7px; }
[hidden] { display: none !important; }
.ambient { position: fixed; inset: 0; z-index: -1; background: radial-gradient(ellipse at 29% 60%, #38503955, transparent 48%), radial-gradient(ellipse at 85% 0%, #85702f18, transparent 50%); }
.masthead { max-width: 1300px; margin: auto; padding: 30px 6%; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #ffffff0b; }
.brand { color: var(--primary); font-size: 12px; letter-spacing: 3px; }
.header-note { color: var(--muted); font: italic 15px Georgia, serif; }
.eyebrow { font-size: 10px; font-weight: 500; letter-spacing: 2.5px; line-height: 1.8; color: var(--primary); }
.intro { min-height: calc(100svh - 90px); padding: 55px 24px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }
.gift-seal { width: 98px; height: 98px; border: 1px solid #f3cd6344; border-radius: 50%; display: grid; place-items: center; color: var(--primary); font-size: 65px; margin-bottom: 30px; box-shadow: 0 0 90px #f3cd6314; animation: seal 6s ease-in-out infinite; }
h1, h2 { font-family: Georgia, 'Times New Roman', serif; font-weight: 400; }
h1 { max-width: 680px; font-size: clamp(36px, 5vw, 64px); line-height: 1.13; margin: 16px 0; }
.intro-copy { color: var(--muted); line-height: 1.9; margin: 10px 0 32px; }
.primary { background: var(--primary); color: #233025; border: 0; border-radius: 50px; padding: 19px 29px; font-weight: 600; box-shadow: 0 8px 35px #e7bd3820; transition: transform .3s, box-shadow .3s; }
.primary span { margin-left: 20px; }
.primary:hover { transform: translateY(-3px); box-shadow: 0 10px 45px #e7bd3840; }
.small-note { margin-top: 22px; color: var(--muted); font-size: 11px; letter-spacing: 1px; }
.intro.leaving { animation: disappear .6s ease forwards; pointer-events: none; }
.gift { max-width: 1160px; margin: auto; padding: 30px 45px 0; animation: appear 1.2s both; }
.gift-heading { text-align: center; }
h2 { font-size: clamp(36px, 4.5vw, 59px); margin: 12px 0; }
h2 span { color: var(--primary); font-style: italic; }
.gift-heading > p:last-child { color: var(--muted); font-size: 14px; }
.gift-layout { display: grid; grid-template-columns: minmax(0, 1.15fr) minmax(0, 1fr); gap: 52px; align-items: center; }
.bouquet-area { position: relative; min-width: 0; height: 575px; }
.bouquet { position: absolute; width: 440px; height: 490px; left: 50%; top: 55px; transform: translateX(-50%); border: 0; background: transparent; -webkit-tap-highlight-color: transparent; }
.bouquet::before { content: ''; position: absolute; width: 300px; height: 330px; left: 70px; top: 45px; background: radial-gradient(ellipse, #dfbc3420, transparent 68%); filter: blur(15px); }
.bouquet-label { margin: 20px 0 12px; padding: 0 12px; text-align: center; color: #9da78a; font: italic 13px/1.6 Georgia, serif; overflow-wrap: anywhere; }
.orbit { position: absolute; border: 1px solid #d6c97814; border-radius: 50%; width: 390px; height: 390px; left: 50%; top: 38px; transform: translateX(-50%) rotate(-20deg); pointer-events: none; }
.orbit-two { width: 440px; height: 310px; top: 100px; transform: translateX(-50%) rotate(-40deg); }
/* Cada flor tiene su ángulo y retraso; los tallos se unen bajo el lazo. */
.flower { position: absolute; left: 50%; bottom: 65px; width: 0; height: var(--height); transform-origin: bottom; transform: rotate(var(--angle)); animation: grow 1.5s var(--delay) both; }
.flower-sway { position: absolute; inset: 0; transform-origin: bottom; animation: sway var(--speed) ease-in-out infinite alternate; }
.stem { position: absolute; width: 5px; height: 100%; left: -2px; background: linear-gradient(90deg, #344d28, #8caa55, #405e32); border-radius: 90% 10% 0 0; }
.leaf { position: absolute; width: 52px; height: 23px; top: 55%; left: 0; border-radius: 0 90% 0 90%; background: linear-gradient(160deg, #8aab55, #3e643b 60%, #24492f); transform: rotate(-29deg); transform-origin: left; }
.leaf::after { content: ''; position: absolute; width: 90%; height: 1px; background: #a2bd6655; left: 4%; top: 50%; transform: rotate(16deg); }
.leaf.second { top: 72%; transform: rotate(204deg); width: 43px; }
.blossom { position: absolute; top: -5px; left: 0; width: 0; height: 0; transform: scale(var(--size)); transition: filter .4s; }
.petal { position: absolute; width: 25px; height: 57px; left: -12.5px; top: -53px; border-radius: 58% 58% 43% 43%; transform-origin: 50% 53px; background: linear-gradient(0deg, #b78320, var(--primary) 48%, #ffe998); box-shadow: inset 2px 0 4px #fff5b455, 0 2px 5px #1c271c22; transform: rotate(var(--rotation)); animation: flutter 4s ease-in-out infinite alternate; animation-delay: var(--delay); }
.petal.inner { height: 42px; top: -38px; transform-origin: 50% 38px; width: 20px; left: -10px; background: linear-gradient(0deg, #c99326, #f8d951 65%, #ffe888); }
.flower-center { position: absolute; width: 34px; height: 34px; left: -17px; top: -17px; border-radius: 50%; background: radial-gradient(circle at 38% 32%, #ae8134, #684d21 67%, #40331b); box-shadow: 0 2px 5px #58410a70, inset 0 0 0 3px #e6ac3933; }
.flower-center::after { content: ''; position: absolute; inset: 4px; border-radius: 50%; background-image: radial-gradient(#e2b558 1px, transparent 1px); background-size: 4px 4px; opacity: .5; }
.bouquet:hover .blossom, .bouquet.touched .blossom { filter: brightness(1.13) drop-shadow(0 0 10px #f4d65b50); }
.ribbon { position: absolute; z-index: 20; bottom: 52px; left: 198px; width: 45px; height: 26px; background: linear-gradient(110deg, #b59149, #ebd195, #bc9853); transform: rotate(-8deg); border-radius: 4px; box-shadow: 0 2px 10px #0004; }
.ribbon::before, .ribbon::after { content: ''; position: absolute; width: 52px; height: 30px; border: 8px solid #d6b878; top: -11px; border-radius: 60% 55% 20% 50%; }
.ribbon::before { right: 26px; transform: rotate(20deg); }
.ribbon::after { left: 25px; transform: rotate(-25deg); }
.ribbon i { position: absolute; top: 20px; left: 8px; width: 19px; height: 52px; background: #d4b473; transform: rotate(20deg); clip-path: polygon(0 0, 100% 0, 100% 100%, 50% 80%, 0 100%); }
.ribbon b { position: absolute; top: 35px; left: 39px; padding: 8px 12px; white-space: nowrap; background: #eee2c6; color: #665939; font: italic 12px Georgia, serif; transform: rotate(20deg); }
.touch-hint { position: absolute; bottom: 0; width: 100%; text-align: center; color: var(--muted); font-size: 11px; }
.letter-column { padding-top: 15px; }
.letter { background: linear-gradient(135deg, #ffffff07, #ffffff02); border: 1px solid #e6d99b23; border-radius: 4px 30px 4px 4px; padding: 28px 32px; position: relative; }
.letter-mark { font: 54px Georgia, serif; color: var(--primary); line-height: .8; opacity: .75; }
.message { font: 23px/1.65 Georgia, serif; margin: 22px 0 28px; }
.gift .message { animation: appear 1.8s .8s both; }
.signature { border-top: 1px solid #ffffff13; padding-top: 20px; display: flex; justify-content: space-between; align-items: center; font: italic 16px Georgia, serif; color: var(--muted); }
.signature span:last-child { font-size: 30px; color: var(--primary); }
.music { margin-top: 24px; padding: 0 5px; }
.music-heading { display: flex; gap: 15px; align-items: center; }
.record { display: grid; place-items: center; width: 44px; height: 44px; flex-shrink: 0; border-radius: 50%; background: repeating-radial-gradient(#26382c 0 2px, #1b2b22 3px 5px); color: var(--primary); border: 1px solid #e6d99b20; }
.music .eyebrow { font-size: 8px; letter-spacing: 1.6px; margin: 0 0 4px; }
h3 { font-size: 14px; font-weight: 400; margin: 0; }
.player-controls { display: flex; justify-content: space-between; align-items: center; margin-top: 17px; gap: 8px; }
#play { border: 0; background: transparent; color: var(--primary); padding: 7px 0; font-size: 12px; min-height: 36px; }
#time { font-size: 10px; color: var(--muted); font-variant-numeric: tabular-nums; }
#progress { width: 100%; accent-color: var(--primary); margin: 0; height: 24px; cursor: pointer; }
.music-status { font-size: 11px; line-height: 1.6; color: var(--muted); margin-top: 5px; }
footer { border-top: 1px solid #ffffff0e; padding: 24px 0; margin-top: 28px; text-align: center; color: var(--muted); font: italic 13px/1.8 Georgia, serif; }
footer b { margin-left: 10px; }
#particles { position: fixed; inset: 0; overflow: hidden; pointer-events: none; z-index: 30; }
.falling { position: absolute; top: -35px; width: 10px; height: 17px; border-radius: 80% 0 80% 10%; background: var(--primary); animation: fall var(--duration) linear forwards; opacity: 0; }
.heart, .sparkle { position: absolute; color: var(--primary); animation: float-up 2.5s ease-out forwards; font-size: 18px; }
.sparkle { font-size: 15px; }
/* Estrellas adicionales: caen entre los pétalos sin bloquear los controles. */
.falling-star { position: absolute; top: -35px; color: #ffffff; line-height: 1; text-shadow: 0 0 6px #ffffffcc, 0 0 14px #dceeff88; animation: star-fall var(--duration) linear forwards; opacity: 0; }
@keyframes star-fall {
  0% { opacity: 0; transform: translate(0, 0) rotate(0); }
  15%, 55% { opacity: 1; }
  35%, 75% { opacity: .65; }
  90% { opacity: .85; }
  100% { opacity: 0; transform: translate(var(--drift), 110vh) rotate(180deg); }
}
.sr-only { position: absolute; width: 1px; height: 1px; padding: 0; overflow: hidden; clip-path: inset(50%); white-space: nowrap; }
.no-script { text-align: center; padding: 20px; }
@keyframes appear { from { opacity: 0; transform: translateY(18px); } to { opacity: 1; transform: translateY(0); } }
@keyframes disappear { to { opacity: 0; transform: translateY(-20px); } }
@keyframes grow { from { opacity: 0; transform: rotate(var(--angle)) scale(.3); } to { opacity: 1; transform: rotate(var(--angle)) scale(1); } }
@keyframes sway { from { transform: rotate(-1.7deg); } to { transform: rotate(1.7deg); } }
@keyframes flutter { from { transform: rotate(var(--rotation)) scaleX(.96); } to { transform: rotate(var(--rotation)) scaleX(1.04); } }
@keyframes seal { 50% { transform: translateY(-7px) rotate(8deg); } }
@keyframes fall { 10% { opacity: .65; } 90% { opacity: .5; } to { transform: translate(var(--drift), 110vh) rotate(520deg); opacity: 0; } }
@keyframes float-up { 0% { opacity: 0; transform: translateY(0) scale(.5); } 25% { opacity: .9; } to { opacity: 0; transform: translateY(-100px) rotate(20deg) scale(1.2); } }
@media (max-width: 800px) {
  .gift { padding: 28px 24px 0; max-width: 560px; }
  .gift-layout { grid-template-columns: 1fr; gap: 15px; }
  /* El escenario mantiene sus proporciones y no ensancha la página. */
  /* Los pétalos sobresalen del botón: reservar 55px evita cortar la flor superior. */
  .bouquet-area { height: calc(490px * var(--bouquet-scale, .65) + 85px); overflow: hidden; overflow: clip; }
  .bouquet { top: 55px; transform: translateX(-50%) scale(var(--bouquet-scale, .65)); transform-origin: top center; }
  .orbit { width: 80%; height: 70%; top: 35px; }
  .orbit-two { width: 85%; height: 55%; top: 70px; }
  .bouquet-label { font-size: 12px; }
  .touch-hint { padding: 0 8px; line-height: 1.5; }
  .letter-column { padding-top: 0; }
  .header-note { font-size: 12px; }
  .brand { font-size: 10px; letter-spacing: 1.5px; }
  .masthead { padding: 23px 6%; }
  .intro { padding: 30px 20px; min-height: calc(100svh - 65px); }
  .gift-seal { margin-bottom: 20px; }
  .primary { min-height: 48px; max-width: 100%; }
  #play { min-height: 44px; }
  #progress { height: 44px; }
  .gift { padding-bottom: env(safe-area-inset-bottom, 0px); }
}
@media (max-width: 430px) {
  .gift { padding-left: 16px; padding-right: 16px; }
  .letter { padding: 22px; }
  .message { font-size: 21px; }
  .header-note { display: none; }
  footer span { display: block; }
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; transition: none !important; }
  #particles { display: none; }
}
"""

JAVASCRIPT = r"""const $ = (id) => document.getElementById(id);
const audio = $('audio');
audio.volume = CONFIG.volumenCancion;
const play = $('play');
const progress = $('progress');
const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
// Solo el ancho modifica el tamaño del ramo; hacer scroll no cambia su escala.
const bouquetArea = document.querySelector('.bouquet-area');
const bouquetObserver = new ResizeObserver(([entry]) => {
  if (!entry.contentRect.width) return;
  const scale = Math.min(1, Math.max(0, (entry.contentRect.width - 12) / 440));
  bouquetArea.style.setProperty('--bouquet-scale', scale.toFixed(4));
});
bouquetObserver.observe(bouquetArea);
let opened = false;
let effectTimer;
let touchTimer;

$('recipient').textContent = CONFIG.nombre;
$('message').textContent = CONFIG.mensaje;
$('song-title').textContent = CONFIG.nombreCancion;
$('intro-title').textContent = CONFIG.fraseInicial;

// Ángulo, longitud del tallo y tamaño: nueve flores forman el ramo.
const arrangement = [
  [-30, 290, .82], [28, 303, .86], [-17, 351, .93],
  [12, 367, .9], [0, 407, .95], [-36, 230, .86],
  [35, 232, .86], [-13, 269, 1.03], [14, 278, 1.02]
];

function createBouquet() {
  arrangement.forEach(([angle, height, size], index) => {
    const flower = document.createElement('span');
    flower.className = 'flower';
    flower.setAttribute('aria-hidden', 'true');
    flower.style.cssText = `--angle:${angle}deg;--height:${height}px;--size:${size};--delay:${index * .12}s;--speed:${3.5 + index * .23}s;z-index:${index + 1}`;
    const sway = document.createElement('span');
    sway.className = 'flower-sway';
    for (const className of ['stem', 'leaf', 'leaf second']) {
      const part = document.createElement('span');
      part.className = className;
      sway.append(part);
    }
    const blossom = document.createElement('span');
    blossom.className = 'blossom';
    for (let p = 0; p < 24; p++) {
      const petal = document.createElement('span');
      petal.className = p < 12 ? 'petal' : 'petal inner';
      petal.style.setProperty('--rotation', `${(p % 12) * 30 + (p >= 12 ? 15 : 0)}deg`);
      blossom.append(petal);
    }
    const center = document.createElement('span');
    center.className = 'flower-center';
    blossom.append(center);
    sway.append(blossom);
    flower.append(sway);
    $('bouquet').append(flower);
  });
}

// Efectos limitados y retirados del DOM al terminar su animación.
function particle(type, x, y) {
  if (motion.matches || document.hidden || $('particles').childElementCount >= 45) return;
  const item = document.createElement('span');
  item.className = type;
  if (type === 'falling' || type === 'falling-star') {
    item.style.left = `${Math.random() * 100}%`;
    item.style.setProperty('--duration', `${7 + Math.random() * 6}s`);
    item.style.setProperty('--drift', `${Math.random() * 180 - 90}px`);
    if (type === 'falling-star') {
      // Estrellas de distintos tamaños con un brillo discreto.
      item.textContent = Math.random() < .5 ? '✦' : '★';
      item.style.fontSize = `${10 + Math.random() * 9}px`;
    }
  } else {
    item.textContent = type === 'heart' ? '♡' : '✧';
    item.style.left = `${x}px`;
    item.style.top = `${y}px`;
  }
  item.addEventListener('animationend', () => item.remove(), { once: true });
  $('particles').append(item);
}

function ambientEffects() {
  clearInterval(effectTimer);
  if (!opened || motion.matches || document.hidden) return;
  effectTimer = setInterval(() => {
    particle('falling');
    if (Math.random() < .65) particle('falling-star');
    const rect = $('bouquet').getBoundingClientRect();
    const x = rect.left + rect.width * (.15 + Math.random() * .7);
    const y = rect.top + rect.height * (.1 + Math.random() * .5);
    particle(Math.random() < .18 ? 'heart' : 'sparkle', x, y);
  }, 650);
}

function syncPlayback() {
  play.textContent = audio.paused ? '▶ Reproducir' : '⏸ Pausar';
}

async function startMusic() {
  try {
    await audio.play();
    $('music-status').textContent = 'Una melodía para acompañar tus flores.';
  } catch {
    $('music-status').textContent = audio.error
      ? 'No se pudo cargar la canción. Comprueba el archivo de audio.'
      : 'Pulsa Reproducir para comenzar la canción.';
  }
  syncPlayback();
}

$('discover').addEventListener('click', () => {
  if (opened) return;
  opened = true;
  $('discover').disabled = true;
  // Se llama desde el clic para conservar el permiso de audio del navegador.
  if (CONFIG.archivoCancion) {
    audio.src = CONFIG.archivoCancion;
    play.disabled = false;
    startMusic();
  }
  $('intro').classList.add('leaving');
  setTimeout(() => {
    $('intro').hidden = true;
    $('gift').hidden = false;
    createBouquet();
    $('gift-title').focus({ preventScroll: true });
    for (let i = 0; i < 10; i++) particle('falling');
    for (let i = 0; i < 5; i++) particle('falling-star');
    ambientEffects();
  }, motion.matches ? 0 : 600);
});

// Click también funciona con el dedo, Enter y la barra espaciadora.
$('bouquet').addEventListener('click', () => {
  const rect = $('bouquet').getBoundingClientRect();
  $('bouquet').classList.add('touched');
  clearTimeout(touchTimer);
  touchTimer = setTimeout(() => $('bouquet').classList.remove('touched'), 900);
  for (let i = 0; i < 8; i++) {
    particle('heart', rect.left + rect.width * (.2 + Math.random() * .6), rect.top + rect.height * (.2 + Math.random() * .4));
  }
});

play.addEventListener('click', () => {
  if (audio.paused) startMusic();
  else audio.pause();
});

function formatTime(seconds) {
  if (!Number.isFinite(seconds)) return '0:00';
  return `${Math.floor(seconds / 60)}:${String(Math.floor(seconds % 60)).padStart(2, '0')}`;
}

function updateProgress() {
  const valid = Number.isFinite(audio.duration) && audio.duration > 0;
  progress.disabled = !valid;
  progress.value = valid ? audio.currentTime / audio.duration * 100 : 0;
  $('time').textContent = `${formatTime(audio.currentTime)} / ${formatTime(audio.duration)}`;
  progress.setAttribute('aria-valuetext', $('time').textContent);
}

progress.addEventListener('input', () => {
  if (Number.isFinite(audio.duration) && audio.duration > 0) {
    audio.currentTime = Number(progress.value) / 100 * audio.duration;
    updateProgress();
  }
});
['loadedmetadata', 'durationchange', 'timeupdate', 'ended'].forEach(event => audio.addEventListener(event, updateProgress));
['play', 'pause', 'ended'].forEach(event => audio.addEventListener(event, syncPlayback));
audio.addEventListener('error', () => {
  $('music-status').textContent = 'No se pudo cargar la canción. Comprueba el nombre y formato del archivo.';
  progress.disabled = true;
  syncPlayback();
});

document.addEventListener('visibilitychange', ambientEffects);
motion.addEventListener('change', () => {
  $('particles').replaceChildren();
  ambientEffects();
});
"""


def construir_pagina():
    """Genera una página autónoma con el audio local incrustado."""
    audio_uri = None
    if ARCHIVO_AUDIO:
        ruta = BASE_DIR / ARCHIVO_AUDIO
        if ruta.is_file():
            audio_uri = "data:audio/mpeg;base64," + base64.b64encode(ruta.read_bytes()).decode("ascii")

    config = {
        "nombre": NOMBRE,
        "mensaje": MENSAJE,
        "nombreCancion": NOMBRE_CANCION,
        "fraseInicial": FRASE_INICIAL,
        "archivoCancion": audio_uri,
        "volumenCancion": max(0.0, min(1.0, VOLUMEN)),
    }
    # Serializar como JSON conserva comillas y caracteres especiales del mensaje.
    config_json = json.dumps(config, ensure_ascii=True).replace("<", "\\u003c")
    color = COLOR_PRINCIPAL if re.fullmatch(r"#[0-9a-fA-F]{6}", COLOR_PRINCIPAL) else "#f3cd63"
    estilos = CSS + "\n:root { --primary: " + color + "; }"
    pagina = HTML.replace("</head>", "<style>" + estilos + "</style></head>")
    script = "(() => {\n'use strict';\nconst CONFIG = " + config_json + ";\n" + JAVASCRIPT + "\n})();"
    pagina = pagina.replace("</body>", "<script>" + script + "</script></body>")
    if not audio_uri:
        pagina = pagina.replace("Tu canción está lista para acompañar este regalo.", "Añade cancion.mp3 junto a app.py para escuchar tu canción.")
    return pagina


def main():
    st.set_page_config(page_title="Flores para ti", page_icon="🌻", layout="wide", initial_sidebar_state="collapsed")
    # Marco de Streamlit a pantalla completa; la página conserva su propio CSS.
    st.html("""<style>
        html, body { overflow: hidden; overscroll-behavior: none; }
        .stApp { background: #101f1b; overflow: hidden; }
        [data-testid="stHeader"] { display: none; }
        [data-testid="stMainBlockContainer"] { padding: 0; width: 100%; max-width: 100%; min-width: 0; }
        [data-testid="stMain"] { overflow: hidden; }
        [data-testid="stVerticalBlock"] { gap: 0; }
        /* Una sola zona de scroll, dentro del iframe; altura móvil estable. */
        #regalo-streamlit { width: 100%; max-width: 100%; min-width: 0; height: 100vh; height: 100svh; overflow: hidden; }
    </style>""")
    # Un iframe aísla los estilos y mantiene la reproducción al interactuar.
    # srcdoc contiene únicamente el código local y la configuración anterior.
    documento = json.dumps(construir_pagina(), ensure_ascii=True).replace("<", "\\u003c")
    st.html(
        '<div id="regalo-streamlit"></div><script>(() => {'
        'const host = document.getElementById("regalo-streamlit");'
        'if (!host || host.childElementCount) return;'
        'const frame = document.createElement("iframe");'
        'frame.title = "Regalo de flores amarillas";'
        'frame.style.cssText = "display:block;width:100%;height:100%;border:0;background:#101f1b";'
        'frame.setAttribute("allow", "autoplay");'
        'frame.srcdoc = ' + documento + ';'
        'host.append(frame);'
        '})();</script>',
        unsafe_allow_javascript=True,
    )


if __name__ == "__main__":
    main()
