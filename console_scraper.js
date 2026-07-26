
(async function continuousStreamWithAutoSave() {
    console.log("🚀 Starting Continuous Extractor with Auto-Save (Every 1 Minute)...");
    console.log("💡 You can type `stopAndDownload()` in the console at any time to save immediately and stop.");
  
    const collectedTurns = [];
    const seenKeys = new Set();
    let keepRunning = true;
    let saveCounter = 1;
  
    // Function to save the currently accumulated turns to disk
    function saveCurrentBatch() {
      if (collectedTurns.length === 0) {
        console.log("⚠️ No turns to save yet.");
        return;
      }
      const blob = new Blob([JSON.stringify(collectedTurns, null, 2)], { type: 'application/json' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = `gemini_chat_backup_part${saveCounter}_(${collectedTurns.length}_items).json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      console.log(`💾 [Auto-Save #${saveCounter}] Downloaded backup with ${collectedTurns.length} total parts!`);
      saveCounter++;
    }
  
    // Global handle to trigger manual stop/save at any time
    window.stopAndDownload = function() {
      keepRunning = false;
      console.log(`🛑 Stopping extraction loop...`);
      saveCurrentBatch();
    };
  
    function getScrollTargets() {
      const targets = [
        document.querySelector('infinite-scroller'),
        document.querySelector('#chat-history'),
        document.querySelector('main'),
        document.documentElement,
        document.body
      ];
      return targets.filter(Boolean);
    }
  
    function captureTurns() {
      const userNodes = document.querySelectorAll('user-query, .user-query, .query-text');
      const modelNodes = document.querySelectorAll('model-response, .model-response, message-content');
      const maxCount = Math.max(userNodes.length, modelNodes.length);
  
      let newCount = 0;
      for (let i = 0; i < maxCount; i++) {
        const uText = userNodes[i] ? userNodes[i].textContent.trim() : "";
        const mText = modelNodes[i] ? modelNodes[i].textContent.trim() : "";
  
        const key = `${uText.slice(0, 50)}|${mText.slice(0, 50)}`;
        if ((uText || mText) && !seenKeys.has(key)) {
          seenKeys.add(key);
          if (uText) collectedTurns.push({ role: "user", parts: [{ text: uText }] });
          if (mText) collectedTurns.push({ role: "model", parts: [{ text: mText }] });
          newCount++;
        }
      }
      return newCount;
    }
  
    let loopCount = 0;
    let idleCount = 0;
    const SAVE_INTERVAL_MS = 60000; // 60 seconds
    let lastSaveTime = Date.now();
  
    while (keepRunning) {
      loopCount++;
      const added = captureTurns();
      
      if (added > 0) {
        idleCount = 0;
        console.log(`[Loop #${loopCount}] 🟢 +${added} new parts! Total captured: ${collectedTurns.length}`);
      } else {
        idleCount++;
        console.log(`[Loop #${loopCount}] ⏳ Waiting for render/fetch... (Idle pass #${idleCount})`);
      }
  
      // Scroll all container candidates down
      const targets = getScrollTargets();
      targets.forEach(t => {
        t.scrollTop = t.scrollHeight;
      });
      window.scrollTo(0, document.body.scrollHeight || document.documentElement.scrollHeight);
  
      // Trigger scroll events to signal background fetches
      window.dispatchEvent(new Event('scroll'));
      targets.forEach(t => t.dispatchEvent(new Event('scroll')));
  
      // Auto-save check (trigged every 60 seconds)
      if (Date.now() - lastSaveTime >= SAVE_INTERVAL_MS) {
        saveCurrentBatch();
        lastSaveTime = Date.now();
      }
  
      // Pause 2 seconds between scroll passes
      await new Promise(resolve => setTimeout(resolve, 2000));
  
      // If no new turns render for 3 full minutes (90 idle checks), finalize and stop
      if (idleCount >= 90) {
        console.log("🏁 Reached the end of the conversation (no new data for 3 minutes).");
        window.stopAndDownload();
        break;
      }
    }
  })();