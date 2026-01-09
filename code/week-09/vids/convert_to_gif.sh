#!/bin/bash

# 批量转换视频为高清GIF脚本
# 使用 ffmpeg 将 mp4 视频转换为优化的高清GIF
# 输出 GIF 保存在同目录，命名为 [视频名].gif

set -e

echo "开始批量转换视频为高清GIF..."
echo ""

# 统计
total=0
success=0
failed=0

# 遍历所有 mp4 文件
find . -type f -name "*.mp4" | sort | while read video; do
    dir=$(dirname "$video")
    filename=$(basename "$video" .mp4)
    output_gif="$dir/$filename.gif"
    
    ((total++))
    
    if [ -f "$output_gif" ]; then
        echo "[跳过] $filename.gif 已存在"
        continue
    fi
    
    echo "[转换] $filename..."
    
    ffmpeg -i "$video" \
        -vf "fps=10,scale=min(800\, iw):-1:flags=lanczos" \
        -c:v pam -f image2pipe \
        - | convert -delay 10 -loop 0 - "$output_gif" 2>/dev/null
    
    if [ -f "$output_gif" ]; then
        size=$(du -h "$output_gif" | cut -f1)
        echo "  成功 -> $output_gif ($size)"
        ((success++))
    else
        echo "  失败 -> $output_gif"
        ((failed++))
    fi
    echo ""
done

echo ""
echo "转换完成!"
echo "总数: $total | 成功: $success | 失败: $failed"
