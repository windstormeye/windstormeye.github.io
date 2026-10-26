-- 每天每个页面每个匿名浏览器一行，pv 为当天的加载次数：
--   文章 PV = SUM(pv)、文章 UV = COUNT(DISTINCT visitor_hash)（按 path 分组）
--   全站 PV / UV 同样从这张表按天汇总
-- visitor_hash 是浏览器本地随机 ID 的 HMAC，跨天稳定，区间 UV 可以跨天去重。
CREATE TABLE IF NOT EXISTS blog_page_visits (
  day TEXT NOT NULL CHECK (length(day) = 10),
  path TEXT NOT NULL CHECK (length(path) BETWEEN 1 AND 300),
  visitor_hash TEXT NOT NULL CHECK (length(visitor_hash) = 64),
  pv INTEGER NOT NULL DEFAULT 1 CHECK (pv >= 1),
  first_seen_at INTEGER NOT NULL,
  PRIMARY KEY (day, path, visitor_hash)
) WITHOUT ROWID;

-- 页面标题只用于看板展示，标题变化时才会写入
CREATE TABLE IF NOT EXISTS blog_pages (
  path TEXT PRIMARY KEY NOT NULL CHECK (length(path) BETWEEN 1 AND 300),
  title TEXT NOT NULL CHECK (length(title) BETWEEN 1 AND 200),
  updated_at INTEGER NOT NULL
) WITHOUT ROWID;

-- 每天最多新增 20000 行（页面 × 浏览器），防止被刷时 D1 写入失控；已有行的 PV 累加不受影响。
CREATE TABLE IF NOT EXISTS blog_daily_budget (
  day TEXT PRIMARY KEY NOT NULL CHECK (length(day) = 10),
  accepted INTEGER NOT NULL DEFAULT 0 CHECK (accepted BETWEEN 0 AND 20000)
) WITHOUT ROWID;

CREATE TRIGGER IF NOT EXISTS blog_page_visits_budget
BEFORE INSERT ON blog_page_visits
WHEN NOT EXISTS (
  SELECT 1 FROM blog_page_visits
  WHERE day = NEW.day AND path = NEW.path AND visitor_hash = NEW.visitor_hash
)
BEGIN
  INSERT INTO blog_daily_budget(day, accepted) VALUES (NEW.day, 0)
    ON CONFLICT(day) DO NOTHING;
  SELECT RAISE(IGNORE) FROM blog_daily_budget
    WHERE day = NEW.day AND accepted >= 20000;
  UPDATE blog_daily_budget SET accepted = accepted + 1 WHERE day = NEW.day;
END;
