import { after, before, beforeEach, test } from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { randomUUID } from 'node:crypto';
import { build } from 'esbuild';
import { Miniflare, convertV4MiniflareOptions } from 'miniflare';
import { beijingDay, cleanup, hashVisitor, MAX_DAILY_PV, recordVisit } from '../src/visit.js';

const secret = 'local-test-secret-not-for-deployment-0123456789';
const origin = 'https://pjhubs.com';
const allow = { limit: async () => ({ success: true }) };
let runtime, db, env;
const waits = [];
const context = { waitUntil: promise => waits.push(promise) };
const post = '/2026/10/07/talk28/';
const visit = (visitorID, { headers = {}, body, path = post, title = '第二次创业' } = {}) => new Request('https://app.pj.studio/v1/visit', {
  method: 'POST',
  headers: { Origin: origin, 'Content-Type': 'text/plain;charset=UTF-8', 'User-Agent': 'Mozilla/5.0 (Macintosh) Safari/605.1.15', 'CF-Connecting-IP': '192.0.2.1', ...headers },
  body: body ?? JSON.stringify({ visitorID, path, title }),
});
const send = (request, overrides = {}, now) => recordVisit(request, { ...env, ...overrides }, context, now);
const rows = () => db.prepare('SELECT day, path, visitor_hash, pv FROM blog_page_visits ORDER BY day, path, pv').all().then(result => result.results);
const titles = () => db.prepare('SELECT path, title FROM blog_pages ORDER BY path').all().then(result => result.results);

before(async () => {
  // 整个 Worker 经 Miniflare 跑一遍，确认打包后的入口和 workerd 一致
  const bundle = await build({ stdin: { contents: `import worker from './src/index.js';
    const allow = { limit: async () => ({ success: true }) };
    export default { fetch(request, env, context) { return worker.fetch(request, { ...env, VISIT_LIMIT: allow, VISIT_LOCATION_LIMIT: allow }, context); } };`,
    resolveDir: new URL('../', import.meta.url).pathname }, bundle: true, format: 'esm', write: false, platform: 'browser' });
  runtime = new Miniflare(convertV4MiniflareOptions({ name: 'blog-analytics-test', modules: true,
    script: bundle.outputFiles[0].text, compatibilityDate: '2026-09-01', cf: false,
    d1Databases: ['DB'], bindings: { BLOG_HASH_KEY: secret, ALLOWED_ORIGINS: 'https://pjhubs.com,https://www.pjhubs.com' } }));
  db = await runtime.getD1Database('DB');
  const sql = await readFile(new URL('../migrations/0001_blog_visits.sql', import.meta.url), 'utf8');
  for (const statement of sql.replace(/--[^\n]*/g, '').match(/CREATE TRIGGER\b[\s\S]+?\bEND;|CREATE TABLE[^;]+;/g)) await db.prepare(statement).run();
  env = { DB: db, BLOG_HASH_KEY: secret, ALLOWED_ORIGINS: 'https://pjhubs.com,https://www.pjhubs.com', VISIT_LIMIT: allow, VISIT_LOCATION_LIMIT: allow };
});
beforeEach(async () => {
  await Promise.all(waits.splice(0));
  await db.prepare('DELETE FROM blog_page_visits').run();
  await db.prepare('DELETE FROM blog_pages').run();
  await db.prepare('DELETE FROM blog_daily_budget').run();
});
after(async () => { await Promise.all(waits.splice(0)); await runtime?.dispose(); });

test('page views add up per page, browser and day', async () => {
  const reader = randomUUID(), other = randomUUID();
  for (let i = 0; i < 3; i++) assert.equal((await send(visit(reader))).status, 204);
  await send(visit(reader, { path: '/', title: 'PJHubs | 也就骑个车' }));
  assert.equal((await send(visit(other.toUpperCase(), { headers: { Origin: 'https://www.pjhubs.com', 'Content-Type': 'application/json' } }))).status, 204);
  const stored = await rows();
  assert.deepEqual(stored.map(row => [row.path, row.pv]), [['/', 1], [post, 1], [post, 3]]);
  assert.equal(stored[2].visitor_hash, await hashVisitor(reader, secret));
  assert.equal(stored[1].visitor_hash, await hashVisitor(other, secret));
  assert.equal(JSON.stringify(stored).includes(reader), false);
  assert.ok(stored.every(row => row.day === beijingDay(Date.now())));
  assert.deepEqual(await titles(), [{ path: '/', title: 'PJHubs | 也就骑个车' }, { path: post, title: '第二次创业' }]);
});

test('paths are normalized and titles follow the latest page', async () => {
  const id = randomUUID();
  await send(visit(id, { path: '/about/index.html', title: '关于' }));
  await send(visit(id, { path: '/about/', title: '  关于\n我 ' }));
  await send(visit(id, { body: JSON.stringify({ visitorID: id, path: '/2018/01/20/2017%E6%80%BB%E7%BB%93/' }) }));
  assert.deepEqual((await rows()).map(row => [row.path, row.pv]), [['/2018/01/20/2017%E6%80%BB%E7%BB%93/', 1], ['/about/', 2]]);
  assert.deepEqual(await titles(), [{ path: '/about/', title: '关于 我' }]);
});

test('the bundled Worker accepts beacons and exposes health only', async () => {
  const response = await runtime.dispatchFetch('https://app.pj.studio/v1/visit', visit(randomUUID()));
  assert.equal(response.status, 204);
  assert.equal((await rows()).length, 1);
  const health = await runtime.dispatchFetch('https://app.pj.studio/health');
  assert.deepEqual(await health.json(), { service: 'blog-analytics', schema_version: 1 });
  assert.equal((await runtime.dispatchFetch('https://app.pj.studio/v1/other')).status, 404);
});

test('other sites, bots and privacy preferences are never recorded', async () => {
  const id = randomUUID();
  assert.equal((await send(visit(id, { headers: { Origin: 'https://evil.example' } }))).status, 403);
  assert.equal((await send(visit(id, { headers: { Origin: '' } }))).status, 403);
  assert.equal((await send(visit(id, { headers: { 'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1)' } }))).status, 204);
  assert.equal((await send(visit(id, { headers: { DNT: '1' } }))).status, 204);
  assert.equal((await send(visit(id, { headers: { 'Sec-GPC': '1' } }))).status, 204);
  assert.equal((await send(new Request('https://app.pj.studio/v1/visit', { headers: { Origin: origin } }))).status, 405);
  assert.equal((await rows()).length, 0);
});

test('malformed bodies are rejected before touching D1', async () => {
  for (const body of ['not json', '[]', JSON.stringify({ visitorID: 'abc', path: '/' }), JSON.stringify({ visitorID: randomUUID() }),
    JSON.stringify({ visitorID: randomUUID(), path: 'https://evil.example/' }), JSON.stringify({ visitorID: randomUUID(), path: '/a b' }),
    JSON.stringify({ visitorID: randomUUID(), path: '/' + 'x'.repeat(300) }), JSON.stringify({ visitorID: randomUUID(), path: '/', title: 1 }),
    JSON.stringify({ visitorID: randomUUID(), path: '/', referrer: 'x' }), JSON.stringify({ visitorID: randomUUID(), path: '/', title: 'x'.repeat(2100) })])
    assert.equal((await send(visit(null, { body }))).status, 400, body);
  assert.equal((await send(visit(randomUUID(), { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }))).status, 400);
  assert.equal((await rows()).length, 0);
});

test('rate limits and missing configuration fail closed', async () => {
  const deny = { limit: async () => ({ success: false }) };
  assert.equal((await send(visit(randomUUID()), { VISIT_LIMIT: deny })).status, 429);
  assert.equal((await send(visit(randomUUID()), { VISIT_LOCATION_LIMIT: deny })).status, 429);
  assert.equal((await send(visit(randomUUID()), { BLOG_HASH_KEY: 'short' })).status, 503);
  assert.equal((await send(visit(randomUUID()), { BLOG_ANALYTICS_ENABLED: 'false' })).status, 204);
  assert.equal((await rows()).length, 0);
});

test('daily new-row budget and per-page PV cap bound writes', async () => {
  const known = randomUUID();
  await send(visit(known));
  await db.prepare('UPDATE blog_daily_budget SET accepted = 20000').run();
  assert.equal((await send(visit(randomUUID()))).status, 204);
  await send(visit(known));
  assert.deepEqual((await rows()).map(row => row.pv), [2]);
  await send(visit(known, { path: '/about/' }));
  assert.deepEqual((await rows()).map(row => row.pv), [2]);
  await db.prepare('UPDATE blog_page_visits SET pv = ?').bind(MAX_DAILY_PV).run();
  await send(visit(known));
  assert.deepEqual((await rows()).map(row => row.pv), [MAX_DAILY_PV]);
});

test('cleanup keeps the last 90 Beijing days only', async () => {
  const now = Date.now(), hash = await hashVisitor(randomUUID(), secret);
  for (const days of [0, 89, 90, 120]) {
    const day = beijingDay(now - days * 86400000);
    await db.prepare('INSERT INTO blog_page_visits VALUES (?,?,?,1,0)').bind(day, post, hash).run();
  }
  await cleanup(db, now);
  assert.deepEqual((await rows()).map(row => row.day).sort(), [beijingDay(now - 89 * 86400000), beijingDay(now)]);
  assert.equal(await db.prepare('SELECT count(*) count FROM blog_daily_budget WHERE day < ?').bind(beijingDay(now - 89 * 86400000)).first('count'), 0);
});

test('the real entry module loads in workerd and fails closed without rate limiters', async () => {
  const bundle = await build({ entryPoints: [new URL('../src/index.js', import.meta.url).pathname], bundle: true, format: 'esm', write: false, platform: 'browser' });
  const entry = new Miniflare(convertV4MiniflareOptions({ name: 'blog-analytics-entry', modules: true, script: bundle.outputFiles[0].text,
    compatibilityDate: '2026-09-01', cf: false, d1Databases: ['DB'], bindings: { BLOG_HASH_KEY: secret, ALLOWED_ORIGINS: origin } }));
  try {
    assert.equal((await entry.dispatchFetch('https://app.pj.studio/health')).status, 200);
    assert.equal((await entry.dispatchFetch('https://app.pj.studio/v1/visit', visit(randomUUID()))).status, 503);
  } finally { await entry.dispose(); }
});
