/* global hexo */
'use strict';

// SEO / 爬虫 / Agent 相关的模板 helper 与生成器：
// - helper：页面标题兜底、摘要、canonical、JSON-LD、Markdown 副本地址
// - 生成器：每篇文章与页面的 Markdown 副本、sitemap.xml、robots.txt、llms.txt

const { stripHTML, unescapeHTML, prettyUrls } = require('hexo-util');

const DESCRIPTION_LENGTH = 120;

function plainText(html) {
  // 块级标签换成空格，避免标题和正文粘在一起
  const spaced = (html || '').replace(/<\/?(?:h[1-6]|p|li|ul|ol|br|div|tr|td|th|blockquote|pre|figure|figcaption)\b[^>]*>/gi, ' ');
  return unescapeHTML(stripHTML(spaced)).replace(/\s+/g, ' ').trim();
}

function truncate(text, length) {
  return text.length > length ? text.slice(0, length) + '…' : text;
}

function canonicalUrl(url) {
  return prettyUrls(url, { trailing_index: false, trailing_html: true });
}

// 没写 title 的独立页面（如 about、photograph），用导航菜单里的名字兜底
function pageTitle(page, theme) {
  if (page.title) return page.title;
  if (!page.path) return '';
  const dir = page.path.replace(/index\.html$/, '');
  const menu = (theme.menu || []).find(item => item.directory === dir);
  return menu ? menu.page : '';
}

function pageDescription(page, config) {
  if (page.tag) return `${config.title} 中标签「${page.tag}」下的文章`;
  if (page.category) return `${config.title} 中分类「${page.category}」下的文章`;
  if (page.archive) return `${config.title} 的全部文章归档`;
  const text = plainText(page.description || page.excerpt || page.content);
  return text ? truncate(text, DESCRIPTION_LENGTH) : config.description;
}

function firstImage(html, base) {
  const match = /<img [^>]*src=['"]([^'"]+)['"]/i.exec(html || '');
  if (!match || match[1].startsWith('data:')) return '';
  try {
    return new URL(match[1], base).toString();
  } catch (err) {
    return '';
  }
}

// 'a/b/' 或 'about/index.html' -> 'a/b/index.md' / 'about/index.md'
function markdownPath(path) {
  if (/(^|\/)index\.html$/.test(path)) return path.replace(/index\.html$/, 'index.md');
  if (path.endsWith('.html')) return path.replace(/\.html$/, '.md');
  return path.replace(/\/?$/, '/') + 'index.md';
}

// 站内链接 / 图片改成绝对地址，和站点渲染（../images -> /images）保持一致，方便 Agent 直接使用
function absolutizeLinks(markdown, root) {
  const absolutize = target => {
    if (/^([a-z][a-z0-9+.-]*:|#|\/\/)/i.test(target)) return target;
    return root + target.replace(/^(\.{1,2}\/)+/, '').replace(/^\/+/, '');
  };
  return markdown
    .replace(/(\]\(\s*)([^)\s]+)/g, (_, prefix, target) => prefix + absolutize(target))
    .replace(/((?:src|href)=["'])([^"']+)/g, (_, prefix, target) => prefix + absolutize(target));
}

function siteRoot(config) {
  return config.url.replace(/\/?$/, '/');
}

function postTags(post) {
  return post.tags ? post.tags.map(tag => tag.name) : [];
}

function xmlEscape(text) {
  return String(text).replace(/[<>&'"]/g, char => ({
    '<': '&lt;', '>': '&gt;', '&': '&amp;', '\'': '&apos;', '"': '&quot;'
  })[char]);
}

function publishedPosts(locals) {
  return locals.posts.filter(post => post.published !== false).sort('-date').toArray();
}

hexo.extend.helper.register('seo_title', function() {
  return pageTitle(this.page, this.theme);
});

hexo.extend.helper.register('seo_description', function() {
  return pageDescription(this.page, this.config);
});

hexo.extend.helper.register('seo_canonical', function() {
  return canonicalUrl(this.url);
});

// 只取正文第一张图作为分享图，open_graph 默认会把所有图片都输出一遍
hexo.extend.helper.register('seo_image', function() {
  return firstImage(this.page.content, canonicalUrl(this.url));
});

hexo.extend.helper.register('seo_markdown_url', function() {
  if (!this.is_post() && !this.page.__page) return '';
  return this.url_for(markdownPath(this.page.path));
});

hexo.extend.helper.register('seo_json_ld', function() {
  const { config, page } = this;
  const url = canonicalUrl(this.url);
  const author = { '@type': 'Person', name: config.author, url: siteRoot(config) };
  let data;

  if (this.is_post()) {
    const tags = postTags(page);
    const image = firstImage(page.content, url);
    data = {
      '@context': 'https://schema.org',
      '@type': 'BlogPosting',
      headline: page.title,
      description: pageDescription(page, config),
      url,
      mainEntityOfPage: url,
      datePublished: page.date.toISOString(),
      dateModified: (page.updated || page.date).toISOString(),
      inLanguage: 'zh-CN',
      author,
      publisher: author
    };
    if (image) data.image = image;
    if (tags.length) data.keywords = tags.join(', ');
  } else if (this.is_home() && !(page.current > 1)) {
    data = {
      '@context': 'https://schema.org',
      '@type': 'WebSite',
      name: config.title,
      description: config.description,
      url: siteRoot(config),
      inLanguage: 'zh-CN',
      author
    };
  } else {
    return '';
  }

  // 防止内容里的 </script> 提前闭合标签
  return `<script type="application/ld+json">${JSON.stringify(data).replace(/</g, '\\u003c')}</script>`;
});

// 每篇文章 / 页面额外输出一份 Markdown（在文章地址后加 index.md），供 Agent 读取
hexo.extend.generator.register('seo_markdown', function(locals) {
  const { config } = this;
  const root = siteRoot(config);
  const items = publishedPosts(locals).concat(locals.pages.toArray());

  return items.map(item => {
    const isPost = item.layout === 'post';
    const title = pageTitle(item, this.theme.config);
    const meta = [`> 原文：${canonicalUrl(item.permalink)}`];
    if (isPost) {
      const tags = postTags(item);
      meta.push(`> 作者：${config.author} · 发布于 ${item.date.format('YYYY-MM-DD')}${tags.length ? ` · 标签：${tags.join('、')}` : ''}`);
    }
    const header = (item.title ? `# ${title}\n\n` : '') + meta.join('\n>\n') + '\n\n';

    return {
      path: markdownPath(item.path),
      data: header + absolutizeLinks((item._content || '').trim(), root) + '\n'
    };
  });
});

hexo.extend.generator.register('seo_sitemap', function(locals) {
  const { config } = this;
  const posts = publishedPosts(locals).filter(post => post.sitemap !== false);
  const pages = locals.pages.filter(page => page.sitemap !== false).toArray();
  const lastmod = date => date.toISOString();
  const latest = posts.length ? posts.reduce((a, b) => (a.updated > b.updated ? a : b)).updated : null;

  const urls = [{ loc: siteRoot(config), lastmod: latest }]
    .concat(posts.map(post => ({ loc: canonicalUrl(post.permalink), lastmod: post.updated })))
    .concat(pages.map(page => ({ loc: canonicalUrl(page.permalink), lastmod: page.updated })));

  const body = urls.map(({ loc, lastmod: date }) => {
    const mod = date ? `<lastmod>${lastmod(date)}</lastmod>` : '';
    return `  <url><loc>${xmlEscape(loc)}</loc>${mod}</url>`;
  }).join('\n');

  return {
    path: 'sitemap.xml',
    data: `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${body}\n</urlset>\n`
  };
});

hexo.extend.generator.register('seo_robots', function() {
  return {
    path: 'robots.txt',
    data: `User-agent: *\nAllow: /\n\nSitemap: ${siteRoot(this.config)}sitemap.xml\n`
  };
});

// https://llmstxt.org/
hexo.extend.generator.register('seo_llms', function(locals) {
  const { config } = this;
  const root = siteRoot(config);
  const posts = publishedPosts(locals);
  const pages = locals.pages.toArray();
  const topTags = locals.tags.sort('-length').limit(12).map(tag => tag.name);
  const link = path => root + markdownPath(path);

  const lines = [
    `# ${config.title}`,
    '',
    `> ${config.description}`,
    '',
    `${config.author} 的个人中文博客，共 ${posts.length} 篇文章，常见话题：${topTags.join('、')}。`,
    '每篇文章和页面都有 Markdown 版本（在页面地址后加 `index.md`），下面的链接均指向 Markdown 版本。',
    '',
    '## 页面',
    '',
    ...pages.map(page => `- [${pageTitle(page, this.theme.config) || page.path}](${link(page.path)})`),
    `- [文章归档](${root}archives/)`,
    '',
    '## 文章',
    '',
    ...posts.map(post => {
      const tags = postTags(post);
      const info = [post.date.format('YYYY-MM-DD')].concat(tags.length ? [tags.join('、')] : []).join(' · ');
      return `- [${post.title}](${link(post.path)}): ${info}。${truncate(plainText(post.content), 60)}`;
    }),
    '',
    '## Optional',
    '',
    `- [RSS 订阅（Atom）](${root}${config.feed ? config.feed.path : 'atom.xml'})`,
    `- [Sitemap](${root}sitemap.xml)`,
    ''
  ];

  return { path: 'llms.txt', data: lines.join('\n') };
});
