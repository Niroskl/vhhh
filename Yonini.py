<!doctype html>
<html lang="he">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>משחק ציור — draw game</title>
  <style>
    :root{--bg:#0f1724;--card:#0b1220;--accent:#7dd3fc;--muted:#94a3b8}
    html,body{height:100%;margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,"Helvetica Neue",Arial}
    body{background:linear-gradient(180deg,#04132a 0%, #081826 100%);color:#eef2ff;display:flex;align-items:center;justify-content:center;padding:20px}
    .app{width:100%;max-width:1000px;background:linear-gradient(180deg, rgba(255,255,255,0.02), rgba(0,0,0,0.06));border-radius:16px;padding:18px;box-shadow:0 8px 30px rgba(0,0,0,0.6)}
    header{display:flex;align-items:center;gap:12px;margin-bottom:12px}
    h1{margin:0;font-size:20px}
    .controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
    .panel{display:flex;gap:8px;align-items:center}
    button{background:transparent;border:1px solid rgba(255,255,255,0.08);padding:8px 12px;border-radius:8px;color:inherit;cursor:pointer}
    button.primary{background:var(--accent);color:#042029;border:none}
    .board{display:grid;grid-template-columns:1fr 320px;gap:12px}

    .canvas-wrap{background:#021424;border-radius:12px;padding:12px;display:flex;flex-direction:column;gap:10px}
    canvas{background:#fff;border-radius:8px;touch-action:none}
    .tools{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
    .sidebar{background:linear-gradient(180deg,#031726, #041826);padding:12px;border-radius:12px;min-height:300px}
    label{font-size:13px;color:var(--muted)}
    .prompt{background:rgba(255,255,255,0.03);padding:8px;border-radius:8px;margin-bottom:8px}
    .stat{font-size:16px;margin-top:8px}
    .footer{margin-top:12px;font-size:13px;color:var(--muted)}
    input[type=range]{width:120px}
    .hidden{display:none}
    .big{font-size:18px}
  </style>
</head>
<body>
  <div class="app">
    <header>
      <h1>משחק ציור — אתגר בזמן</h1>
      <div style="flex:1"></div>
      <div class="controls">
        <div class="panel">
          <label class="big">בחר צבע</label>
          <input id="color" type="color" value="#000000" />
          <label>גודל מברשת</label>
          <input id="size" type="range" min="1" max="40" value="6" />
        </div>
        <button id="clear">נקה</button>
        <button id="undo">בטל</button>
        <button id="download">הורד תמונה</button>
      </div>
    </header>

    <div class="board">
      <div class="canvas-wrap">
        <div style="display:flex;gap:8px;align-items:center;justify-content:space-between">
          <div class="tools">
            <button id="pencil" class="primary">צייר</button>
            <button id="eraser">מחק</button>
            <button id="fill">מלא (מלא בדוגמה)</button>
          </div>
          <div style="text-align:right">
            <div id="timer" class="stat">זמן: 00:00</div>
            <div id="score" class="stat">ניקוד: 0</div>
          </div>
        </div>

        <canvas id="canvas" width="800" height="500"></canvas>
        <div style="display:flex;gap:8px;align-items:center;justify-content:space-between">
          <div>
            <button id="startGame" class="primary">התחל אתגר (60s)</button>
            <button id="submit">סיים והגדר ניקוד</button>
          </div>
          <div style="color:var(--muted)">טיפים: השתמש בעכבר או במסך מגע כדי לצייר. ניתן לבטל פעולות עם 'בטל'.</div>
        </div>
      </div>

      <aside class="sidebar">
        <div class="prompt">
          <div style="font-size:14px;color:var(--muted)">אתגר עכשיו:</div>
          <div id="currentPrompt" style="font-weight:700;font-size:18px">-</div>
        </div>

        <div>
          <label>רשימת אתגרים אפשריים</label>
          <ul id="promptsList"></ul>
        </div>

        <div class="stat" id="strokes">שרטוטים: 0</div>
        <div class="stat" id="timeUsed">זמן בשימוש: 0s</div>

        <div style="margin-top:12px">
          <label>כללים פשוטים</label>
          <ol style="color:var(--muted)">
            <li>בחר פרומפט ולחץ 'התחל'.</li>
            <li>צייר בתוך הזמן.</li>
            <li>לחץ 'סיים' כדי לקבל ניקוד מבוסס זמן ומספר מהלכים.</li>
          </ol>
        </div>

        <div class="footer">רצית להוסיף אופציית שיתוף או בדיקת דמיון לתמונה? תגיד ואוסיף!</div>
      </aside>
    </div>
  </div>

  <script>
    // אלמנטים
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    const colorPicker = document.getElementById('color');
    const sizeRange = document.getElementById('size');
    const clearBtn = document.getElementById('clear');
    const undoBtn = document.getElementById('undo');
    const downloadBtn = document.getElementById('download');
    const pencilBtn = document.getElementById('pencil');
    const eraserBtn = document.getElementById('eraser');
    const fillBtn = document.getElementById('fill');
    const startBtn = document.getElementById('startGame');
    const submitBtn = document.getElementById('submit');
    const timerEl = document.getElementById('timer');
    const scoreEl = document.getElementById('score');
    const currentPromptEl = document.getElementById('currentPrompt');
    const promptsListEl = document.getElementById('promptsList');
    const strokesEl = document.getElementById('strokes');
    const timeUsedEl = document.getElementById('timeUsed');

    // משחק
    const prompts = [
      'חתול', 'כלב', 'אוטו', 'בית', 'עץ', 'שמש', 'כוכב', 'איש שלג', 'דג', 'פרח', 'לחם', 'כדור', 'שמלה', 'תות'
    ];

    // הצגת רשימת הפרומפטים
    prompts.forEach(p => {
      const li = document.createElement('li'); li.textContent = p; promptsListEl.appendChild(li);
    });

    let drawing = false;
    let erasing = false;
    let last = {x:0,y:0};
    let history = []; // snapshots for undo
    let strokes = 0;

    // הגדרות התחלתיות
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.lineWidth = sizeRange.value;
    ctx.strokeStyle = colorPicker.value;

    // אירועים
    function saveSnapshot(){
      try{
        history.push(canvas.toDataURL());
        if(history.length>30) history.shift();
      }catch(e){/*ignore*/}
    }

    function restoreSnapshot(){
      if(!history.length) return;
      const url = history.pop();
      const img = new Image();
      img.onload = ()=>{
        ctx.clearRect(0,0,canvas.width,canvas.height);
        ctx.drawImage(img,0,0);
      };
      img.src = url;
    }

    function getPos(e){
      const rect = canvas.getBoundingClientRect();
      const isTouch = e.touches && e.touches[0];
      const clientX = isTouch ? e.touches[0].clientX : e.clientX;
      const clientY = isTouch ? e.touches[0].clientY : e.clientY;
      return {x: clientX - rect.left, y: clientY - rect.top};
    }

    function startDraw(e){
      e.preventDefault();
      drawing = true;
      last = getPos(e);
      ctx.beginPath();
      ctx.moveTo(last.x,last.y);
      saveSnapshot();
      strokes++;
      updateStats();
    }
    function moveDraw(e){
      if(!drawing) return;
      const p = getPos(e);
      if(erasing){
        ctx.clearRect(p.x-ctx.lineWidth/2, p.y-ctx.lineWidth/2, ctx.lineWidth, ctx.lineWidth);
      } else {
        ctx.lineTo(p.x,p.y);
        ctx.stroke();
      }
      last = p;
    }
    function endDraw(e){
      if(!drawing) return;
      drawing = false;
      ctx.closePath();
      updateStats();
    }

    // חיבור אירועים למגע ועכבר
    canvas.addEventListener('mousedown', startDraw);
    canvas.addEventListener('mousemove', moveDraw);
    window.addEventListener('mouseup', endDraw);

    canvas.addEventListener('touchstart', startDraw, {passive:false});
    canvas.addEventListener('touchmove', moveDraw, {passive:false});
    window.addEventListener('touchend', endDraw);

    // בקרים
    colorPicker.addEventListener('input',(e)=>{ctx.strokeStyle=e.target.value;});
    sizeRange.addEventListener('input',(e)=>{ctx.lineWidth=e.target.value;});
    clearBtn.addEventListener('click', ()=>{saveSnapshot(); ctx.clearRect(0,0,canvas.width,canvas.height);});
    undoBtn.addEventListener('click', ()=>{restoreSnapshot();});
    downloadBtn.addEventListener('click', ()=>{
      const link = document.createElement('a');
      link.download = 'my-drawing.png';
      link.href = canvas.toDataURL();
      link.click();
    });

    pencilBtn.addEventListener('click', ()=>{erasing=false; pencilBtn.classList.add('primary'); eraserBtn.classList.remove('primary');});
    eraserBtn.addEventListener('click', ()=>{erasing=true; eraserBtn.classList.add('primary'); pencilBtn.classList.remove('primary');});

    // מילוי דוגמה: לצורך הדגמה ממלא בצורת פשוטה
    fillBtn.addEventListener('click', ()=>{
      saveSnapshot();
      ctx.fillStyle = '#fde68a';
      ctx.fillRect(50,50,200,150);
    });

    // סטטיסטיקה ומשחק
    let gameTimer = null;
    let secondsLeft = 0;
    let gameStartedAt = null;
    let gameTimeTotal = 60; // seconds default

    function updateTimerDisplay(){
      const mm = String(Math.floor(secondsLeft/60)).padStart(2,'0');
      const ss = String(secondsLeft%60).padStart(2,'0');
      timerEl.textContent = `זמן: ${mm}:${ss}`;
    }

    function updateStats(){
      strokesEl.textContent = 'שרטוטים: ' + strokes;
      const used = gameStartedAt ? Math.floor((Date.now()-gameStartedAt)/1000) : 0;
      timeUsedEl.textContent = 'זמן בשימוש: ' + used + 's';
    }

    function pickRandomPrompt(){
      return prompts[Math.floor(Math.random()*prompts.length)];
    }

    startBtn.addEventListener('click', ()=>{
      // איפוס קנבס
      ctx.clearRect(0,0,canvas.width,canvas.height);
      history = [];
      strokes = 0; updateStats();
      secondsLeft = gameTimeTotal;
      updateTimerDisplay();
      currentPromptEl.textContent = pickRandomPrompt();
      if(gameTimer) clearInterval(gameTimer);
      gameStartedAt = Date.now();
      gameTimer = setInterval(()=>{
        secondsLeft--;
        updateTimerDisplay();
        if(secondsLeft<=0){
          clearInterval(gameTimer);
          endGame();
        }
      },1000);
    });

    function endGame(){
      // תזמון סיום
      alert('הזמן נגמר! לחץ סיים כדי לקבל ניקוד או התחל שוב.');
    }

    // חישוב ניקוד פשוט — דגם: יותר שנותרו יותר ניקוד, פחות שרטוטים יותר ניקוד
    function computeScore(){
      const usedSec = gameStartedAt ? Math.floor((Date.now()-gameStartedAt)/1000) : 0;
      const timeScore = Math.max(0, Math.round((Math.max(0, gameTimeTotal - usedSec) / gameTimeTotal) * 100));
      const strokeScore = Math.max(0, 100 - (strokes*6));
      const final = Math.round((timeScore*0.6) + (strokeScore*0.4));
      return {final, timeScore, strokeScore, usedSec};
    }

    submitBtn.addEventListener('click', ()=>{
      const s = computeScore();
      scoreEl.textContent = 'ניקוד: ' + s.final;
      alert(`ניקוד סופי: ${s.final}\nזמן בשימוש: ${s.usedSec}s\nנקודות זמן: ${s.timeScore}\nנקודות מתאר: ${s.strokeScore}`);
    });

    // אתחול תצוגה ראשונית
    currentPromptEl.textContent = 'לחץ התחלה';
    updateTimerDisplay();
    updateStats();

    // התאמת גודל קנבס למכשיר (אופציונלי)
    function fitCanvas(){
      // שמור תוכן
      const img = new Image(); img.src = canvas.toDataURL();
      const w = Math.min(1000, window.innerWidth-120);
      const h = Math.min(600, window.innerHeight-220);
      canvas.width = Math.max(600, w);
      canvas.height = Math.max(320, h);
      img.onload = ()=>{ ctx.drawImage(img,0,0,canvas.width,canvas.height); };
    }
    window.addEventListener('resize', fitCanvas);
    fitCanvas();
  </script>
</body>
</html>
