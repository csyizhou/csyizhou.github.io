const button = document.querySelector('.language');
const navigation = document.querySelector('nav');
function setLanguage(language) {
  const chinese = language === 'zh-CN';
  document.documentElement.lang = language;
  navigation.setAttribute('aria-label', chinese ? '主导航' : 'Main navigation');
  button.setAttribute('aria-label', chinese ? 'Switch to English' : '切换到中文');
  try { localStorage.setItem('yi-zhou-language', language); } catch {}
}
let language = 'en';
try { if (localStorage.getItem('yi-zhou-language') === 'zh-CN') language = 'zh-CN'; } catch {}
setLanguage(language);
button.hidden = false;
button.addEventListener('click', () => setLanguage(document.documentElement.lang === 'en' ? 'zh-CN' : 'en'));

const paperList = document.querySelector('#selected-papers');
const translatedLabels = { Paper: '论文', Code: '代码', Project: '项目', Dataset: '数据集' };
function make(tag, value, className) {
  const element = document.createElement(tag);
  if (value) element.textContent = value;
  if (className) element.className = className;
  return element;
}
for (const entry of window.selectedPublications || []) {
  const paper = make('article', null, 'paper');
  const venue = make('div', entry.venue, 'venue');
  venue.append(make('small', entry.year));
  const details = make('div');
  const authors = make('p');
  for (const part of entry.authors.split(/(Y\. Zhou\b|\bYi Zhou\b)/)) {
    authors.append(/^(Y\. Zhou|Yi Zhou)$/.test(part) ? make('strong', part) : part);
  }
  details.append(make('h3', entry.title), authors);
  const links = make('div', null, 'paper-links');
  for (const item of entry.links || []) {
    const a = make('a');
    try {
      const url = new URL(item.url);
      if (url.protocol !== 'https:') continue;
      a.href = url.href;
    } catch { continue; }
    if (Object.hasOwn(translatedLabels, item.label)) {
      const en = make('span', item.label);
      const zh = make('span', translatedLabels[item.label]);
      en.lang = 'en'; zh.lang = 'zh-CN';
      a.append(en, zh);
    } else a.textContent = item.label;
    a.append(' ↗');
    links.append(a);
  }
  if (links.childElementCount) details.append(links);
  paper.append(venue, details);
  paperList.append(paper);
}
