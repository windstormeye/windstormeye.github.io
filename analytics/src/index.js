// Worker 入口只能导出处理函数，采集逻辑在 visit.js
import { recordVisit } from './visit.js';

const headers = { 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff', 'X-Robots-Tag': 'noindex' };

export default {
  async fetch(request, env, context) {
    const path = new URL(request.url).pathname;
    if (path === '/health' && request.method === 'GET') return Response.json({ service: 'blog-analytics', schema_version: 1 }, { headers });
    if (path === '/v1/visit') return recordVisit(request, env, context);
    return new Response(null, { status: 404, headers });
  },
};
