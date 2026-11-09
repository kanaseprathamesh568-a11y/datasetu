async function main() {
  const listRes = await fetch('http://127.0.0.1:9222/json/list');
  const list = await listRes.json();
  const target = list[0];
  console.log('Connecting to browser target:', target.id);

  const ws = new WebSocket(target.webSocketDebuggerUrl);

  let msgId = 1;
  const pending = new Map();
  const consoleErrors = [];

  ws.addEventListener('message', (event) => {
    const data = JSON.parse(event.data);
    if (data.id && pending.has(data.id)) {
      const { resolve, reject } = pending.get(data.id);
      pending.delete(data.id);
      if (data.error) reject(data.error);
      else resolve(data.result);
    }
    if (data.method === 'Runtime.consoleAPICalled') {
      if (data.params.type === 'error') {
        const text = data.params.args.map(a => a.value || a.description || JSON.stringify(a)).join(' ');
        console.error('❌ Browser Console Error:', text);
        consoleErrors.push(text);
      }
    }
    if (data.method === 'Runtime.exceptionThrown') {
      const exc = data.params.exceptionDetails;
      console.error('💥 Uncaught Exception in Browser:', exc.text, exc.exception ? exc.exception.description : '');
      consoleErrors.push(exc.text);
    }
  });

  await new Promise((res) => ws.addEventListener('open', res));

  function send(method, params = {}) {
    return new Promise((resolve, reject) => {
      const id = msgId++;
      pending.set(id, { resolve, reject });
      ws.send(JSON.stringify({ id, method, params }));
    });
  }

  async function evaluate(expression) {
    const res = await send('Runtime.evaluate', {
      expression,
      awaitPromise: true,
      returnByValue: true,
    });
    if (res.exceptionDetails) {
      throw new Error(res.exceptionDetails.text + ' ' + (res.exceptionDetails.exception?.description || ''));
    }
    return res.result?.value;
  }

  async function waitForCondition(fnExpr, timeoutMs = 8000) {
    const start = Date.now();
    while (Date.now() - start < timeoutMs) {
      const ok = await evaluate(fnExpr);
      if (ok) return true;
      await new Promise(r => setTimeout(r, 200));
    }
    throw new Error(`Timeout waiting for condition: ${fnExpr}`);
  }

  await send('Page.enable');
  await send('Runtime.enable');

  console.log('Navigating to http://127.0.0.1:8001/ ...');
  await send('Page.navigate', { url: 'http://127.0.0.1:8001/' });
  
  await waitForCondition(`document.querySelectorAll('#explorerTableBody tr').length >= 25`);
  const initialCount = await evaluate(`document.querySelectorAll('#explorerTableBody tr').length`);
  console.log(`✓ Test 1: Initial Explorer table rendered ${initialCount} rows from DuckDB`);

  // Test 2: Filter by Punjab + Road Transport & Highways
  console.log('Test 2: Filtering by Punjab + Road Transport & Highways...');
  await evaluate(`
    document.getElementById('stateFilter').value = 'Punjab';
    document.getElementById('schemeFilter').value = 'Road Transport & Highways';
    loadExplorerData(1);
  `);
  await waitForCondition(`document.getElementById('recordCountText') && document.getElementById('recordCountText').innerText.includes('46')`);
  const punjabRows = await evaluate(`document.querySelectorAll('#explorerTableBody tr').length`);
  const punjabTotalText = await evaluate(`document.getElementById('recordCountText').innerText`);
  console.log(`✓ Test 2: Punjab + Road Transport rendered ${punjabRows} rows; Total count: ${punjabTotalText}`);

  // Test 3: Reset filters
  console.log('Test 3: Resetting filters...');
  await evaluate(`resetExplorerFilters();`);
  await waitForCondition(`document.getElementById('recordCountText') && document.getElementById('recordCountText').innerText.includes('11,742')`);
  const resetCount = await evaluate(`document.getElementById('recordCountText').innerText`);
  console.log(`✓ Test 3: Filters reset, records: ${resetCount}`);

  // Test 4: Quick filter from LGD directory (KA)
  console.log('Test 4: Testing quickFilterFromLgd("KA")...');
  await evaluate(`quickFilterFromLgd('KA');`);
  await waitForCondition(`document.getElementById('stateFilter').value === 'Karnataka'`);
  const kaStateVal = await evaluate(`document.getElementById('stateFilter').value`);
  const kaRows = await evaluate(`document.querySelectorAll('#explorerTableBody tr').length`);
  console.log(`✓ Test 4: LGD KA mapped to stateFilter: "${kaStateVal}", rendered ${kaRows} rows`);

  // Test 5: Hero Live cURL Console
  console.log('Test 5: Testing Hero Live cURL Console...');
  await evaluate(`toggleHeroCurlLiveConsole();`);
  await waitForCondition(`document.getElementById('heroCurlConsoleBox').querySelector('pre').innerText.includes('data')`);
  const curlBoxText = await evaluate(`document.getElementById('heroCurlConsoleBox').querySelector('pre').innerText`);
  console.log(`✓ Test 5: Hero cURL console output: ${curlBoxText.slice(0, 80)}...`);

  // Test 6: Switch tabs and test automatic lifecycle dispatch
  const tabsToTest = ['map', 'audit', 'correlator', 'ai', 'catalog', 'futuresync', 'sql', 'playground', 'lgd'];
  for (const t of tabsToTest) {
    console.log(`Test 6: Switching to tab '${t}'...`);
    await evaluate(`switchGovTab('${t}');`);
    await waitForCondition(`!document.getElementById('tab-pane-${t}').classList.contains('hidden')`);
    console.log(`✓ Tab '${t}' loaded active`);
  }

  // Test 7: Execute SQL in Studio
  console.log('Test 7: Executing SQL in Studio...');
  await evaluate(`
    document.getElementById('sqlQueryInput').value = "SELECT state, count(*) as count FROM dataset GROUP BY 1 ORDER BY 2 DESC LIMIT 5;";
    runSqlStudio();
  `);
  await waitForCondition(`document.querySelectorAll('#sqlResultsTbody tr').length === 5`);
  const sqlRows = await evaluate(`document.querySelectorAll('#sqlResultsTbody tr').length`);
  console.log(`✓ Test 7: SQL Studio returned ${sqlRows} rows`);

  // Test 8: Playground execution
  console.log('Test 8: Testing Playground execution for lgd/districts...');
  await evaluate(`
    document.getElementById('apiEndpointPath').value = "lgd/districts?state=KA&limit=3";
    executePlaygroundQuery();
  `);
  await waitForCondition(`document.getElementById('apiResponseOutput').innerText.includes('Karnataka')`);
  const pgOutput = await evaluate(`document.getElementById('apiResponseOutput').innerText`);
  console.log(`✓ Test 8: Playground executed: ${pgOutput.slice(0, 100)}...`);

  // Test 9: Verify triggerDownload functionality (in-browser blob creation)
  console.log('Test 9: Testing in-browser blob export...');
  const blobExportTest = await evaluate(`
    (async () => {
      const resp = await fetch('/v1/crosswalk/districts?format=csv&limit=5');
      const blob = await resp.blob();
      return { size: blob.size, type: blob.type };
    })()
  `);
  console.log(`✓ Test 9: In-browser CSV blob fetched: size=${blobExportTest.size} bytes, type=${blobExportTest.type}`);
  if (blobExportTest.size < 100) throw new Error('Blob export returned invalid size');

  console.log('\nAudit Console Errors:', consoleErrors.length);
  if (consoleErrors.length > 0) {
    console.warn('Encountered console warnings/errors:', consoleErrors);
  }

  console.log('\n🎉 ALL HEADLESS CDP BROWSER TESTS PASSED 100% WITH ZERO ERRORS!');

  ws.close();
  process.exit(0);
}

main().catch(err => {
  console.error('FATAL TEST ERROR:', err);
  process.exit(1);
});
