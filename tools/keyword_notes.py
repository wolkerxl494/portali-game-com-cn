from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Optional

# 示例数据中使用的关键词和关联URL
SAMPLE_KEYWORD = "爱游戏"
SAMPLE_URL = "https://portali-game.com.cn"

@dataclass
class KeywordNote:
    """
    表示一条关键词笔记的数据类。
    
    属性：
        keyword: 核心关键词
        url: 关联的链接（可选）
        content: 笔记正文
        tags: 标签列表
        created_at: 创建时间
    """
    keyword: str
    content: str
    url: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def formatted_entry(self, with_timestamp: bool = True) -> str:
        """生成格式化的单条笔记字符串"""
        lines = [
            f"关键词: {self.keyword}",
            f"内容: {self.content}",
        ]
        if self.url:
            lines.append(f"链接: {self.url}")
        if self.tags:
            tags_str = ", ".join(self.tags)
            lines.append(f"标签: [{tags_str}]")
        if with_timestamp:
            lines.append(f"时间: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        return "\n".join(lines)

    def short_summary(self) -> str:
        """返回简短的摘要"""
        url_part = f" | {self.url}" if self.url else ""
        return f"[{self.keyword}]{url_part} | {self.content[:30]}..."


def format_notes_list(notes: List[KeywordNote], title: str = "关键词笔记列表") -> str:
    """将笔记列表格式化为带标题的文本块"""
    parts = [f"===== {title} ====="]
    for idx, note in enumerate(notes, 1):
        parts.append(f"--- 第{idx}条 ---")
        parts.append(note.formatted_entry())
    parts.append("=" * 20)
    return "\n\n".join(parts)


def export_to_json(notes: List[KeywordNote]) -> str:
    """将笔记列表导出为JSON字符串（原生字典转换）"""
    import json
    dict_list = []
    for note in notes:
        d = asdict(note)
        d["created_at"] = d["created_at"].isoformat()
        dict_list.append(d)
    return json.dumps(dict_list, ensure_ascii=False, indent=2)


def filter_by_keyword(notes: List[KeywordNote], keyword: str) -> List[KeywordNote]:
    """根据关键词过滤笔记（不区分大小写）"""
    return [n for n in notes if keyword.lower() in n.keyword.lower()]


def filter_by_tag(notes: List[KeywordNote], tag: str) -> List[KeywordNote]:
    """根据标签过滤笔记"""
    return [n for n in notes if tag in n.tags]


# 示例数据使用指定的关键词和URL
DEMO_NOTES = [
    KeywordNote(
        keyword=SAMPLE_KEYWORD,
        content="爱游戏是一个专注于游戏资讯和社区的平台。",
        url=SAMPLE_URL,
        tags=["游戏", "社区"],
        created_at=datetime(2024, 10, 15, 14, 30, 0)
    ),
    KeywordNote(
        keyword="爱游戏攻略",
        content="这里收录了各类热门游戏的详细攻略。",
        url=SAMPLE_URL + "/guides",
        tags=["攻略", "热门"]
    ),
    KeywordNote(
        keyword="爱游戏新闻",
        content="每日更新游戏行业最新动态与资讯。",
        url=SAMPLE_URL + "/news",
        tags=["新闻", "动态"],
        created_at=datetime(2024, 10, 16, 9, 0, 0)
    ),
]


def demo_run():
    """演示函数：展示各个功能的使用"""
    print("=== 初始化演示数据 ===")
    notes = DEMO_NOTES

    print("\n>>> 格式化输出全部笔记:")
    print(format_notes_list(notes))

    print("\n>>> 按关键词 '爱游戏' 过滤:")
    filtered = filter_by_keyword(notes, "爱游戏")
    for n in filtered:
        print(n.short_summary())

    print("\n>>> 按标签 '攻略' 过滤:")
    tagged = filter_by_tag(notes, "攻略")
    for n in tagged:
        print(n.short_summary())

    print("\n>>> JSON 导出:")
    print(export_to_json(notes))

    print("\n>>> 单条笔记格式化:")
    single = notes[0]
    print(single.formatted_entry(with_timestamp=False))


if __name__ == "__main__":
    demo_run()