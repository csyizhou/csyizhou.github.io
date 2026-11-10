# 周毅 · 学术主页

中英双语静态网站，可直接用浏览器打开 `index.html`，也可以在此目录运行：

```sh
python3 -m http.server 8931 --bind 127.0.0.1
```

然后访问 http://127.0.0.1:8931/ 。

## 自己维护代表作

只需编辑仓库根目录的 **`publications.js`**。在 GitHub 打开文件，点击铅笔图标即可在线编辑；也可以在本地修改并提交。数组从上到下就是首页的展示顺序，想置顶就把那篇移到最前面。每篇由题名、作者、刊会、年份和链接组成：

```js
{
  "title": "论文题目",
  "authors": "A. Author, Y. Zhou, B. Author",
  "venue": "CVPR",
  "year": 2026,
  "links": [
    { "label": "Paper", "url": "https://example.org/paper" },
    { "label": "Code", "url": "https://example.org/code" }
  ]
}
```

新论文可以复制已有条目再改内容。条目间用逗号分隔，没有链接时用 `"links": []`。页面会自动加粗 `Y. Zhou` 或 `Yi Zhou`；`Paper`、`Code`、`Project` 和 `Dataset` 会随语言切换。

## 更新论文词云和其他内容

- 词云基于[东南大学个人主页](https://cs.seu.edu.cn/yizhou/main.htm)列出的 42 篇 2022–2026 年论文标题，每个词按包含它的标题数计算。会合并常见拼写变体，例如 `multi-modal` 和 `multimodal`。
- 更新 `scripts/paper-titles.tsv`（每行“年份、Tab、标题”），再运行 `python3 scripts/build_word_cloud.py`。生成的 `assets/word-cloud.svg` 和数据一起提交。若年份范围或论文数量改变，也同步更新 `index.html` 里的图注。
- `index.html`：简介、研究方向、近期成果与招生信息。
- `assets/portrait.jpg`：线上头像；本地原图 `profile.jpeg` 不提交。

## GitHub Pages

目标仓库：`csyizhou/csyizhou.github.io`。发布源选择 **Settings → Pages → Deploy from a branch → main → /(root)**。保留根目录的 `.nojekyll`。部署完成后，修改 `main` 分支里的文件会自动触发更新。

[GitHub Pages 官方指南](https://docs.github.com/en/pages/quickstart)
