#!/bin/bash

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "========================================"
echo "       视频播放器项目一键测试脚本"
echo "========================================"
echo ""

echo "🔍 检查 Python 环境..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ 未找到 Python 解释器"
    exit 1
fi
echo "✅ Python 可用: $($PYTHON_CMD --version)"
echo ""

echo "🧪 运行后端测试..."
echo "----------------------------------------"
cd "$PROJECT_ROOT/backend"

# 使用内存数据库运行测试，避免数据库锁定问题
export DATABASE_URL="sqlite:///:memory:"

$PYTHON_CMD -m pytest tests/ -v --tb=short -q -W ignore::DeprecationWarning 2>&1
TEST_RESULT=$?

echo ""
echo "========================================"
if [ $TEST_RESULT -eq 0 ]; then
    echo "✅ 所有测试通过！"
else
    echo "❌ 测试失败，退出码: $TEST_RESULT"
    exit $TEST_RESULT
fi
