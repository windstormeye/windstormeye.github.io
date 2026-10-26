// pjhubs.com 博客的访问统计。没有公网域名，只经 app.pj.studio 网关的 service binding 访问：
//   POST https://app.pj.studio/api/blog/analytics/visit  ->  /v1/visit
//   GET  https://app.pj.studio/api/blog/analytics/health ->  /health
// 每次页面加载上报一次 {"visitorID": "<浏览器本地随机 UUID>", "path": "/2026/10/07/talk28/", "title": "第二次创业"}，
// 按北京时间自然日记每个页面和全站的 PV / UV。
const encoder = new TextEncoder();
const uuid = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const bot = /\b(?:Googlebot|GoogleOther|Google-InspectionTool|bingbot|msnbot|GPTBot|ChatGPT-User|OAI-SearchBot|ClaudeBot|Claude-SearchBot|Claude-User|PerplexityBot|Perplexity-User|CCBot|Slackbot|Twitterbot|Discordbot|TelegramBot|LinkedInBot|DuckDuckBot|YandexBot|Baiduspider|Bytespider|Applebot|PetalBot|AhrefsBot|SemrushBot|MJ12bot|DotBot|facebookexternalhit|Facebot|meta-externalagent|meta-externalfetcher|HeadlessChrome|HeadlessFirefox|HeadlessSafari|PhantomJS|bot|spider|crawler)\b/i;
const headers = { 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff', 'X-Robots-Tag': 'noindex' };
const reply = (status = 204) => new Response(null, { status, headers });
// 同一浏览器同一页面一天最多记 200 次 PV，防止单个 ID 被刷
export const MAX_DAILY_PV = 200;
// location.pathname 已经是百分号编码的，只允许 URL 路径字符
const pathPattern = /^\/[A-Za-z0-9\-._~%!$&'()*+,;=:@/]{0,299}$/;
export const beijingDay = now => new Date(now + 8 * 3600000).toISOString().slice(0, 10);
let savedSecret, savedKey, cleanedDay;
// isolate 内记住已写过的标题，避免每次 PV 都多一条 SQL
const savedTitles = new Map();

export async function hashVisitor(id, secret) {
  if (typeof secret !== 'string' || encoder.encode(secret).byteLength < 32) throw new Error('blog_analytics_unconfigured');
  if (secret !== savedSecret) {
    savedSecret = secret;
    savedKey = crypto.subtle.importKey('raw', encoder.encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  }
  const bytes = new Uint8Array(await crypto.subtle.sign('HMAC', await savedKey,
    encoder.encode('pjhubs.com:blog:v1:' + id.toLowerCase())));
  return Array.from(bytes, byte => byte.toString(16).padStart(2, '0')).join('');
}

// sendBeacon / fetch(no-cors) 跨域只能发 text/plain，JSON 也接受
async function visitorBody(request) {
  const type = request.headers.get('Content-Type')?.split(';', 1)[0].trim().toLowerCase();
  if (type !== 'text/plain' && type !== 'application/json') throw new Error('invalid_body');
  const reader = request.body?.getReader();
  if (!reader) throw new Error('invalid_body');
  const chunks = []; let length = 0;
  try {
    for (;;) {
      const { done, value } = await reader.read(); if (done) break;
      length += value.length; if (length > 2048) throw new Error('invalid_body');
      chunks.push(value);
    }
  } finally { await reader.cancel().catch(() => {}); }
  const bytes = new Uint8Array(length); let offset = 0;
  for (const value of chunks) { bytes.set(value, offset); offset += value.length; }
  const body = JSON.parse(new TextDecoder().decode(bytes));
  if (!body || Array.isArray(body) || typeof body.visitorID !== 'string' || !uuid.test(body.visitorID)
      || typeof body.path !== 'string' || !pathPattern.test(body.path)
      || Object.keys(body).some(key => !['visitorID', 'path', 'title'].includes(key))) throw new Error('invalid_body');
  let title = null;
  if (body.title !== undefined) {
    if (typeof body.title !== 'string') throw new Error('invalid_body');
    title = body.title.replace(/[\u0000-\u001f\u007f]/g, ' ').replace(/\s+/g, ' ').trim().slice(0, 200) || null;
  }
  return { visitor: body.visitorID, path: body.path.replace(/\/index\.html$/, '/'), title };
}

export const recordSQL = `INSERT INTO blog_page_visits (day,path,visitor_hash,pv,first_seen_at) VALUES (?,?,?,1,?)
  ON CONFLICT(day,path,visitor_hash) DO UPDATE SET pv = pv + 1 WHERE pv < ${MAX_DAILY_PV}`;
// 标题没变时不产生写入
export const titleSQL = `INSERT INTO blog_pages (path,title,updated_at) VALUES (?,?,?)
  ON CONFLICT(path) DO UPDATE SET title = excluded.title, updated_at = excluded.updated_at WHERE title IS NOT excluded.title`;

// 只保留最近 90 天，和看板最长的查询范围一致
export async function cleanup(db, now = Date.now()) {
  const cutoff = beijingDay(now - 89 * 86400000);
  for (let batch = 0; batch < 12; batch++) {
    const result = await db.prepare(`DELETE FROM blog_page_visits WHERE (day,path,visitor_hash) IN
      (SELECT day,path,visitor_hash FROM blog_page_visits WHERE day < ? LIMIT 1000)`).bind(cutoff).run();
    if ((result.meta?.changes ?? 0) < 1000) break;
  }
  await db.prepare('DELETE FROM blog_daily_budget WHERE day < ?').bind(cutoff).run();
}

export async function recordVisit(request, env, context, now = Date.now()) {
  if (env.BLOG_ANALYTICS_ENABLED === 'false') return reply();
  if (request.method !== 'POST') return reply(405);
  const origins = (env.ALLOWED_ORIGINS || '').split(',').map(value => value.trim()).filter(Boolean);
  if (!origins.includes(request.headers.get('Origin'))) return reply(403);
  // 尊重浏览器的隐私设置，尽量排除爬虫。不保存 IP 和 UA，IP 只用于 Cloudflare 的短期限流。
  if (request.headers.get('DNT') === '1' || request.headers.get('Sec-GPC') === '1'
      || bot.test(request.headers.get('User-Agent') || '')) return reply();
  if (!env.DB || !env.BLOG_HASH_KEY || !env.VISIT_LIMIT || !env.VISIT_LOCATION_LIMIT) return reply(503);
  try {
    if (!(await env.VISIT_LIMIT.limit({ key: 'ip:' + (request.headers.get('CF-Connecting-IP') || 'unknown') })).success) return reply(429);
    // 按 Cloudflare 节点共享的刹车，在读请求体和写 D1 之前生效
    if (!(await env.VISIT_LOCATION_LIMIT.limit({ key: 'blog-ingestion' })).success) return reply(429);
  } catch { return reply(503); }
  let visit;
  try { visit = await visitorBody(request); } catch { return reply(400); }
  try {
    const hash = await hashVisitor(visit.visitor, env.BLOG_HASH_KEY);
    const today = beijingDay(now), seconds = Math.floor(now / 1000);
    const statements = [env.DB.prepare(recordSQL).bind(today, visit.path, hash, seconds)];
    if (visit.title && savedTitles.get(visit.path) !== visit.title) statements.push(env.DB.prepare(titleSQL).bind(visit.path, visit.title, seconds));
    await env.DB.batch(statements);
    if (visit.title) {
      if (savedTitles.size >= 512) savedTitles.delete(savedTitles.keys().next().value);
      savedTitles.set(visit.path, visit.title);
    }
    // 不额外占用账号的 cron：每个 isolate 每天顺带清理一次过期数据
    if (cleanedDay !== today) {
      cleanedDay = today;
      context?.waitUntil(cleanup(env.DB, now).catch(() => console.error('blog_analytics_cleanup_failed')));
    }
    return reply();
  } catch { console.error('blog_analytics_failed'); return reply(503); }
}
