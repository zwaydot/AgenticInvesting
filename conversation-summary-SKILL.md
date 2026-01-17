---
name: conversation-summary
description: Generate a structured summary of the conversation, including problems solved, capabilities demonstrated, and tools used. Use this skill when the user asks to summarize the conversation or says "总结对话".
license: Complete terms in LICENSE.txt
---

This skill generates a structured, comprehensive summary of the conversation session.

## When to Use

Trigger this skill when the user:
- Says "总结对话" (Chinese for "summarize conversation")
- Says "总结对话"
- Asks to summarize the conversation
- Requests a recap of what was discussed

## Summary Structure

Generate a summary with the following sections:

### 1. 对话概览 (Conversation Overview)
- **主题**: Main topic(s) discussed
- **时间**: Date and duration context
- **参与者**: User and Agent roles

### 2. 解决的问题 (Problems Solved)
List each problem the user presented and how it was resolved:
- **问题描述**: What the user asked for or needed
- **解决方案**: What the Agent did to help
- **结果**: Outcome or deliverable

### 3. 表现出的能力 (Capabilities Demonstrated)
Analyze and list the capabilities the Agent demonstrated:
- **分析能力**: Understanding user needs, analyzing code/data
- **技术能力**: Programming, API integration, data processing
- **问题解决**: Debugging, troubleshooting, optimization
- **沟通能力**: Explanation, documentation, user guidance
- **工具使用**: Effective use of available tools and APIs

### 4. 调用的工具 (Tools Used)
List all tools/MCPs called during the conversation:
- **工具名称**: Name of each tool/MCP used
- **调用目的**: Why it was used
- **调用次数**: Number of times called (if applicable)

### 5. 关键产出 (Key Deliverables)
List any tangible outputs:
- Code written or modified
- Files created or edited
- Data retrieved or processed
- Documentation generated
- Actions completed

### 6. 对话亮点 (Highlights)
Note any particularly interesting or valuable aspects of the conversation:
- Innovative solutions
- Learning moments
- Complex challenges overcome
- Best practices demonstrated

## Execution Steps

### Step 1: Generate Summary Text
Call the Skill tool to generate a structured summary of the conversation:
- Use the Skill tool with `skill: "conversation-summary"`
- The skill will return a comprehensive text summary

### Step 2: Append to Notion (MANDATORY - DO NOT SKIP)
**Immediately after receiving the summary, you must persist it to Notion.**

Call `mcp__notion__API-patch-block-children` with:
- **block_id**: `2e850145-005b-80ca-8e23fbcbb1257239`
- **children**: An array starting with a divider, followed by the summary content

**⚠️ CRITICAL**: This step is NOT optional. Failure to execute this step means the summary will only exist in the conversation and won't be persisted for future reference.

### Step 3: Verify Storage
After calling the MCP:
- Check the response to ensure no errors occurred
- Inform the user that the summary has been saved to Notion
- Provide the URL to the Notion page for their reference

## Format Guidelines

- Use clear, professional language
- Be concise but comprehensive
- Use Chinese for section headers and content (unless user prefers English)
- Include specific details where relevant (file paths, function names, etc.)
- Format with markdown for readability (headers, lists, code blocks where appropriate)

## Example Output

```markdown
# 对话总结

## 对话概览
- **主题**: Alpaca 账户查看与记录存储
- **时间**: 2025-01-14
- **参与者**: 用户（查询账户）、Agent（执行查询和存储）

## 解决的问题
1. **查看 Alpaca 账户信息**
   - 问题描述: 用户想了解当前账户状态
   - 解决方案: 使用 Alpaca MCP 的 `get_account_info` 工具
   - 结果: 成功获取并展示了完整的账户信息

2. **存储对话记录到 Notion**
   - 问题描述: 用户希望将本次对话保存到 Notion
   - 解决方案: 尝试使用 Notion MCP 创建新页面，遇到 API bug 后改为追加到现有页面
   - 结果: 成功将内容存储到 "Agent Investing" 页面

## 表现出的能力
- **API 集成**: Alpaca 和 Notion MCP 的调用
- **问题诊断**: 识别 Notion MCP post-page API 的参数序列化问题
- **灵活适应**: 当创建新页面失败时，采用替代方案
- **用户沟通**: 清晰解释技术限制和解决方案

## 调用的工具
| 工具 | 目的 | 次数 |
|------|------|------|
| mcp__alpaca__get_account_info | 获取账户信息 | 1 |
| mcp__notion__API-post-search | 搜索 Notion 页面 | 3 |
| mcp__notion__API-patch-block-children | 添加内容到页面 | 2 |
| mcp__notion__API-delete-a-block | 删除内容块 | 17 |
| mcp__notion__API-post-page | 尝试创建页面（失败） | 4 |

## 关键产出
- Alpaca 账户信息报告
- Notion 页面更新（两条记录已撤回）
- 对话记录成功保存到 "Agent Investing" 页面

## 对话亮点
- 发现并诊断了 Notion MCP 的 API bug
- 展示了处理技术限制的灵活性
- 成功实现了用户的核心需求
```

## Configuration

**Notion Storage:**
- Target page: `https://www.notion.so/alivedesign/Agent-Investing-2e850145005b80ca8e23fbcbb1257239`
- Page ID: `2e850145-005b-80ca-8e23fbcbb1257239` (use this in API calls)
- **IMPORTANT**: Notion MCP requires UUID without hyphens in API calls:
  - ✅ Correct format: `2e850145005b80ca8e23fbcbb1257239`
  - ❌ Incorrect format: `2e850145-005b-80ca-8e23fbcbb1257239`
- Method: Append to existing page (do NOT create new pages)
- Required MCP: `mcp__notion__API-patch-block-children`

**Important**: The skill only generates the summary text. It is the Agent's responsibility to call the MCP and persist the data. Always follow the Execution Steps in order.
