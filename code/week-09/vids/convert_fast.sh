#!/bin/bash

# 快速视频到GIF转换脚本（批量并行）
# 使用更优化的参数快速转换

cd "$(dirname "$0")"

echo "快速批量转换视频为高清GIF..."
echo ""

find . -name "*.mp4" | sort | while read video; do
    dir=$(dirname "$video")
    name=$(basename "$video" .mp4)
    output="$dir/$name.gif"
    
    [ -f "$output" ] && echo "跳过 $name (已存在)" && continue
    
    echo "转换: $name..."
    
    ffmpeg -i "$video" \
        -vf "fps=10,scale=min(1200\, iw):-1:flags=lanczos" \
        -c:v pam -f image2pipe - 2>/dev/null | \
    convert -delay 10 -loop 0 -colorspace sRGB - "$output" 2>/dev/null
    
    if [ -f "$output" ]; then
        size=$(du -h "$output" | cut -f1)
        echo "  完成 -> $output ($size)"
    fi
done

echo ""
echo "所有转换完成！"
find . -name "*.gif" -exec ls -lh {} \; | awk '{print $5, $NF}' | column -t
