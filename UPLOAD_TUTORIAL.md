# 从零开始：如何把项目上传到 GitHub（含 Git 安装教程）

这份教程是为了帮助你从一台全新的电脑开始，把你的代码项目上传到 GitHub。我们将分为三个步骤：**安装工具**、**配置身份**、**上传项目**。

---

## 🛠️ 第一步：安装 Git（只需做一次）

如果你换了新电脑，或者电脑里没有 Git，需要先安装它。

1.  **下载**
    *   访问官网：[https://git-scm.com/download/win](https://git-scm.com/download/win)
    *   点击 "Click here to download" 下载最新版安装包。

2.  **安装**
    *   双击下载好的 `.exe` 文件。
    *   **无脑点击 "Next"**：安装向导会有很多选项，对于初学者，**一路点击 "Next" (下一步)** 直到点击 "Install" (安装) 即可。默认设置已经非常完美。
    *   等待安装进度条走完。

3.  **验证**
    *   打开你的终端（在桌面右键 -> Open Git Bash here，或者直接用 IDE 的终端）。
    *   输入：`git --version`
    *   如果出现类似 `git version 2.xx.x` 的字样，说明安装成功！

---

## 👤 第二步：告诉 Git 你是谁（只需做一次）

Git 需要知道是谁在写代码。打开终端，输入以下两行命令（记得把引号里的内容换成你的）：

```bash
# 设置你的用户名（建议用英文）
git config --global user.name "你的GitHub用户名"

# 设置你的邮箱（建议用注册GitHub的邮箱）
git config --global user.email "你的邮箱@example.com"
```

---

## 🚀 第三步：上传你的项目（每个新项目做一次）

假设你现在有一个写好的代码文件夹，想把它上传到 GitHub。

### 1. 准备工作
*   在 GitHub 网站右上角点击 `+` -> **New repository** (新建仓库)。
*   给仓库起个名字（Repository name），比如 `my-awesome-project`。
*   点击 **Create repository** (创建仓库)。
*   **复制仓库地址**：你会看到一个 HTTPS 地址，类似 `https://github.com/你的名字/仓库名.git`，复制它。

### 2. 在 IDE 中操作
打开你的 IDE（比如 Trae 或 VS Code），打开你的项目文件夹，然后打开终端（Terminal），依次输入以下命令：

#### (1) 初始化仓库
让 Git 接管这个文件夹：
```bash
git init
```

#### (2) 忽略不需要的文件（非常重要！）
**在上传前**，一定要检查根目录下有没有一个叫 `.gitignore` 的文件。如果没有，新建一个，并写入以下内容（防止上传垃圾文件或敏感信息）：
```text
venv/
__pycache__/
*.log
.env
.DS_Store
```

#### (3) 暂存所有文件
把所有代码放入“待上传区”：
```bash
git add .
```

#### (4) 提交存档
保存到本地：
```bash
git commit -m "第一次提交我的项目"
```

#### (5) 关联远程仓库
把本地仓库和刚才在 GitHub 上创建的仓库连起来（把 `<你的仓库地址>` 换成刚才复制的链接）：
```bash
git remote add origin <你的仓库地址>
```

#### (6) 推送代码
把代码上传到 GitHub：
```bash
git push -u origin main
```

---

## 🔄 第四步：以后如何更新代码？

以后你修改了代码，只需要做“日常三部曲”：

1.  `git add .` （保存修改）
2.  `git commit -m "写点你改了什么"` （确认存档）
3.  `git push` （上传云端）

---

### ❓ 常见问题

*   **Q: 提示 "fatal: remote origin already exists"?**
    *   A: 说明你已经关联过仓库了。如果想换一个，运行 `git remote remove origin`，然后重新关联。
*   **Q: 提示 "Access denied" 或需要密码？**
    *   A: GitHub 现在不再支持直接输入密码。当你第一次 Push 时，Windows 通常会弹出一个窗口让你登录 GitHub 账号，在浏览器里授权即可。

祝你的开源之旅愉快！🚀
