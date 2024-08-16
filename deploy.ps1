# auto_git_push.ps1
# 检查 Git 状态
git status

# 添加所有更改的文件到暂存区
git add .

# 提示用户输入提交信息
$commitMessage = Read-Host "git info"

# 提交更改
git commit -m "$commitMessage"

# 推送到远程仓库
git push

# 提示完成
Write-Host "done."

# 延时3秒
Start-Sleep -Seconds 3