# demo_outputs

## 1. 本地生成

在项目根目录执行：

```bash
python scripts/run_demo.py
```

产出写入 `demo_outputs/`（项目根目录），可复制到本目录作为参赛提交副本。

## 2. 从 GitHub Actions 下载（评委不跑代码时）

1. 打开仓库 GitHub 页面 → **Actions**
2. 选择最近一次成功的 workflow run（push 或 PR 触发）
3. 页面底部 **Artifacts** → 下载 `demo_outputs`
4. 解压后得到 `demo.log`、`graph.json`、`decisions.json`、`snapshots.json`
