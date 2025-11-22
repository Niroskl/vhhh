<!doctype html>
<html lang="he">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>משחק: חד-קרן תנוק חמוד</title>
  <style>
    html,body{height:100%;margin:0;font-family:system-ui,Segoe UI,Roboto,'Helvetica Neue',Arial}
    #gameWrap{display:flex;flex-direction:column;align-items:center;padding:12px;background:linear-gradient(180deg,#c8f1ff 0%,#ffe6fb 100%);min-height:100vh;box-sizing:border-box}
    canvas{background:transparent;border-radius:16px;box-shadow:0 10px 30px rgba(0,0,0,0.12)}
    .hud{display:flex;gap:12px;align-items:center;margin:10px 0}
    .panel{background:rgba(255,255,255,0.8);padding:8px 12px;border-radius:10px;backdrop-filter:blur(4px)}
    .big{font-size:18px;font-weight:700}
    .controls{margin-top:8px;display:flex;gap:8px}
    button{padding:8px 12px;border-radius:10px;border:0;background:#6c5ce7;color:white;font-weight:700}
    .touch-controls{display:none;margin-top:10px}
    .touch-controls button{width:64px;height:64px;border-radius:12px;font-size:18px}
    @media (max-width:800px){
      .touch-controls{display:flex}
      canvas{width:92vw;height:60vh}
    }
  </style>
</head>
<body>
  <div id="gameWrap">
    <h1>חד-קרן תנוק חמוד 🦄</h1>
    <div class="hud">
      <div class="panel big">ניקוד: <span id="score">0</span></div>
      <div class="panel">חיים: <span id="lives">3</span></div>
      <div class="panel">מהירות: <span id="level">1</span></div>
    </div>

    <canvas id="game" width="800" height="480"></canvas>

    <div class="controls">
      <button id="startBtn">התחל</button>
      <button id="pauseBtn">השהה</button>
      <button id="resetBtn">אתחל</button>
    </div>

    <div class="touch-controls">
      <button id="leftBtn">◀</button>
      <button id="upBtn">▲</button>
      <button id="rightBtn">▶</button>
    </div>

    <p style="max-width:800px;text-align:center">מנע מהמכשולים לפגוע בחד־קרן, אסוף כוכבים כדי להרוויח נקודות. שלוט עם החצים או הכפתורים למגע.</p>
  </div>

<script>
// --- הגדרות ומשתנים ---
const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');
let W = canvas.width, H = canvas.height;

let scoreEl = document.getElementById('score');
let livesEl = document.getElementById('lives');
let levelEl = document.getElementById('level');

let running = false;
let paused = false;

// משחקי ישויות
const unicorn = {
  x: 140, y: H/2, w: 80, h: 60,
  vy: 0, gravity: 0.6, jump: -11,
  speed: 3
};

let stars = []; // לאיסוף
let obstacles = []; // מכשולים

let score = 0;
let lives = 3;
let level = 1;
let spawnTimer = 0;

// תמיכה במגע
const leftBtn = document.getElementById('leftBtn');
const rightBtn = document.getElementById('rightBtn');
const upBtn = document.getElementById('upBtn');

let keys = {};

// --- פונקציות עזר ---
function rand(min,max){ return Math.random()*(max-min)+min }

function resetGame(){
  score = 0; lives = 3; level = 1; stars = []; obstacles = []; unicorn.x = 140; unicorn.y = H/2; unicorn.vy = 0; spawnTimer = 0; running = true; paused = false;
  updateHUD();
}

function updateHUD(){
  scoreEl.textContent = score;
  livesEl.textContent = lives;
  levelEl.textContent = level;
}

// --- יצירת ישויות ---
function spawnStar(){
  stars.push({x: W+40, y: rand(40,H-40), r: 12, vx: -3 - level*0.4});
}
function spawnObstacle(){
  const h = rand(24,80);
  obstacles.push({x: W+60, y: H - h - 20, w: 26, h: h, vx: -3 - level*0.5});
}

// --- לוגיקה ---
function update(dt){
  if(!running || paused) return;

  // תזוזת חד-קרן (כבידה + קפיצה)
  unicorn.vy += unicorn.gravity;
  unicorn.y += unicorn.vy;
  // bound
  if(unicorn.y + unicorn.h/2 > H - 20){ unicorn.y = H - 20 - unicorn.h/2; unicorn.vy = 0 }
  if(unicorn.y - unicorn.h/2 < 0){ unicorn.y = unicorn.h/2; unicorn.vy = 0 }

  // תזוזה שמאל/ימין
  if(keys['ArrowLeft'] || keys['a']) unicorn.x -= unicorn.speed + level*0.3;
  if(keys['ArrowRight'] || keys['d']) unicorn.x += unicorn.speed + level*0.3;
  unicorn.x = Math.max(20, Math.min(W-20-unicorn.w, unicorn.x));

  // ספאונינג
  spawnTimer += dt;
  if(spawnTimer > Math.max(400 - level*30, 160)){
    if(Math.random() < 0.6) spawnStar(); else spawnObstacle();
    spawnTimer = 0;
  }

  // עדכון כוכבים
  for(let i = stars.length-1; i >= 0; i--){
    const s = stars[i]; s.x += s.vx;
    if(s.x < -40) stars.splice(i,1);
    // בדיקת פגיעה
    if(collideRect(unicorn.x, unicorn.y- unicorn.h/2, unicorn.w, unicorn.h, s.x - s.r, s.y - s.r, s.r*2, s.r*2)){
      score += 10; stars.splice(i,1); if(score % 100 === 0) levelUp(); updateHUD();
    }
  }

  // עדכון מכשולים
  for(let i = obstacles.length-1; i >= 0; i--){
    const o = obstacles[i]; o.x += o.vx;
    if(o.x < -100) obstacles.splice(i,1);
    if(collideRect(unicorn.x, unicorn.y- unicorn.h/2, unicorn.w, unicorn.h, o.x, o.y, o.w, o.h)){
      // פגיעה
      obstacles.splice(i,1);
      lives -= 1; updateHUD();
      if(lives <= 0){ gameOver() }
      else { // קטן שבריטון קטן
        unicorn.x = 140; unicorn.y = H/2; unicorn.vy = 0;
      }
    }
  }
}

function levelUp(){
  level += 1; updateHUD();
}

function gameOver(){
  running = false; paused = false;
  setTimeout(()=>{
    if(confirm('Game Over! ניקוד: ' + score + '\nהאם תרצה לנסות שוב?')) resetGame();
  }, 100);
}

function collideRect(x1,y1,w1,h1,x2,y2,w2,h2){
  return !(x1+w1 < x2 || x1 > x2+w2 || y1+h1 < y2 || y1 > y2+h2);
}

// --- ציור ---
function draw(){
  // רקע עדין
  ctx.clearRect(0,0,W,H);
  drawClouds();

  // כוכבים
  for(const s of stars){ drawStar(s.x, s.y, s.r) }

  // מכשולים
  for(const o of obstacles){ drawObstacle(o) }

  // חד-קרן
  drawUnicorn(unicorn.x, unicorn.y);

  // תמיכה בפינה תחתונה
  ctx.fillStyle = 'rgba(255,255,255,0.06)';
  ctx.fillRect(0,H-18,W,18);
}

function drawClouds(){
  // כמה עננים פשוטים
  ctx.save();
  for(let i=0;i<5;i++){
    const x = (i*200 + (Date.now()/40 % 400))% (W+200) - 100;
    const y = 40 + (i%2)*20;
    roundCloud(x,y,60);
  }
  ctx.restore();
}

function roundCloud(x,y,r){
  ctx.beginPath();
  ctx.fillStyle = 'rgba(255,255,255,0.85)';
  ctx.arc(x,y, r*0.6,0,Math.PI*2);
  ctx.arc(x+40,y+8, r*0.5,0,Math.PI*2);
  ctx.arc(x-30,y+8, r*0.45,0,Math.PI*2);
  ctx.fill();
}

function drawStar(x,y,r){
  ctx.save();
  ctx.translate(x,y);
  ctx.beginPath();
  for(let i=0;i<5;i++){
    ctx.lineTo(Math.cos((18+i*72)/180*Math.PI)*r, -Math.sin((18+i*72)/180*Math.PI)*r);
    ctx.lineTo(Math.cos((54+i*72)/180*Math.PI)*r*0.5, -Math.sin((54+i*72)/180*Math.PI)*r*0.5);
  }
  ctx.closePath();
  ctx.fillStyle = '#ffd166';
  ctx.fill();
  ctx.restore();
}

function drawObstacle(o){
  ctx.save();
  ctx.fillStyle = '#7b3f00';
  ctx.fillRect(o.x, o.y, o.w, o.h);
  // עלים שמייצרים צורה
  ctx.fillStyle = 'rgba(0,0,0,0.05)';
  ctx.fillRect(o.x-6, o.y-8, o.w+12, 6);
  ctx.restore();
}

function drawUnicorn(cx, cy){
  ctx.save();
  // body shadow
  ctx.fillStyle = 'rgba(0,0,0,0.06)';
  ctx.beginPath(); ctx.ellipse(cx+24, cy+28, 40,16,0,0,Math.PI*2); ctx.fill();

  // body
  ctx.fillStyle = '#ffffff';
  roundRect(ctx, cx, cy-20, unicorn.w, unicorn.h, 14); ctx.fill();

  // head
  ctx.beginPath(); ctx.ellipse(cx+64, cy-8, 26,20,0,0,Math.PI*2); ctx.fill();

  // eye
  ctx.fillStyle = '#222'; ctx.beginPath(); ctx.arc(cx+72, cy-12, 3.5,0,Math.PI*2); ctx.fill();

  // horn
  ctx.fillStyle = '#ffd166'; ctx.beginPath(); ctx.moveTo(cx+82, cy-28); ctx.lineTo(cx+92, cy-6); ctx.lineTo(cx+72, cy-8); ctx.fill();

  // mane (rainbow)
  const maneColors = ['#ff6b6b','#ffd166','#6bcB77','#5ec6ff','#c084fc'];
  for(let i=0;i<maneColors.length;i++){
    ctx.fillStyle = maneColors[i];
    ctx.beginPath(); ctx.ellipse(cx+56 - i*6, cy-18 + i*2, 10,6, -0.4 + i*0.06,0,Math.PI*2); ctx.fill();
  }

  // tail
  for(let i=0;i<4;i++){
    ctx.fillStyle = maneColors[3-i]; ctx.beginPath(); ctx.ellipse(cx-10 - i*8, cy+2 + i*2, 10,6, 0.6 + i*0.1,0,Math.PI*2); ctx.fill();
  }

  ctx.restore();
}

function roundRect(ctx,x,y,w,h,r){
  ctx.beginPath();
  ctx.moveTo(x+r,y);
  ctx.arcTo(x+w,y,x+w,y+h,r);
  ctx.arcTo(x+w,y+h,x,y+h,r);
  ctx.arcTo(x,y+h,x,y,r);
  ctx.arcTo(x,y,x+w,y,r);
  ctx.closePath();
}

// --- פיקוח זמן / לופ ---
let last = performance.now();
function loop(now){
  const dt = now - last; last = now;
  update(dt);
  draw();
  requestAnimationFrame(loop);
}
requestAnimationFrame(loop);

// --- אירועים ---
window.addEventListener('keydown', e=>{ keys[e.key] = true; if(e.key === 'ArrowUp' || e.key === 'w' || e.key === ' ') { unicorn.vy = unicorn.jump } });
window.addEventListener('keyup', e=>{ keys[e.key] = false; });

document.getElementById('startBtn').addEventListener('click', ()=>{ if(!running) resetGame(); running = true; paused = false });
document.getElementById('pauseBtn').addEventListener('click', ()=>{ paused = !paused; document.getElementById('pauseBtn').textContent = paused? 'המשך' : 'השהה' });
document.getElementById('resetBtn').addEventListener('click', ()=>{ resetGame() });

leftBtn.addEventListener('touchstart', ()=> keys['ArrowLeft']=true); leftBtn.addEventListener('touchend', ()=> keys['ArrowLeft']=false);
rightBtn.addEventListener('touchstart', ()=> keys['ArrowRight']=true); rightBtn.addEventListener('touchend', ()=> keys['ArrowRight']=false);
upBtn.addEventListener('touchstart', ()=> unicorn.vy = unicorn.jump);

// עכבר/נגיעה על הקנבס לקפיצה
canvas.addEventListener('mousedown', ()=> unicorn.vy = unicorn.jump);
canvas.addEventListener('touchstart', (e)=>{ e.preventDefault(); unicorn.vy = unicorn.jump }, {passive:false});

// התאמת גודל
function resize(){
  // נשאיר רזולוציה קבועה פנימית, אך נשנה CSS לפי רוחב חלון
  const wrapW = Math.min(window.innerWidth - 40, 1000);
  canvas.style.width = wrapW + 'px';
  // לשמור על יחס
}
window.addEventListener('resize', resize); resize();

// אתחול ראשוני (מצב המתנה)
(function initial(){
  // הציגו הוראות התחלה
  ctx.font = '20px system-ui'; ctx.fillStyle = '#444'; ctx.textAlign = 'center';
  ctx.fillText('לחץ "התחל" כדי לשחק — מקשי חיצים או נגיעה לקפיצה', W/2, H/2);
})();

// נקודות משניות - נוסיף קצת ספאונינג אחורי
setInterval(()=>{ if(running && !paused){
  // כל X שניות אולי נוסיף אירוע
  if(Math.random()<0.5) spawnStar();
}}, 1200);

</script>
</body>
</html>
