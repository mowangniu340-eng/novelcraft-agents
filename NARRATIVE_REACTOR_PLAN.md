# Narrative Reactor Architecture 规划蓝图（V1）

## 1. 目标重述与设计原则

你要构建的不是传统写作工具，而是一个**叙事涌现系统（Narrative Emergence System）**：
- 输入：世界规则、角色目标、环境扰动。
- 运行：多 Agent 在稀缺资源和信息不完全条件下持续博弈。
- 输出：从高张力状态中“收割”文学片段，而非线性剧情脚本。

### 核心原则
1. **规则先于故事**：剧情是动力系统演化结果。
2. **状态先于文本**：先保证模拟可解释，再做文风渲染。
3. **冲突驱动采样**：只有高信息增益时刻才触发文学生成。
4. **可观测可回放**：每段文本必须可追溯到状态快照与事件链。

---

## 2. 四层拓扑架构（解耦 + 互动）

## Layer A：世界公理层（Ontological Layer）

**职责**：定义“上帝物理学”，不处理叙事语言。

### A1. 资源图谱（Resource Graph）
- 节点：角色、组织、地点、物资、信息。
- 边：拥有、欠债、控制、依赖、掩盖、交换。
- 关键稀缺资源建议统一抽象为：
  - `material`（物质资源）
  - `authority`（权力合法性）
  - `knowledge`（信息优势）
  - `affect`（情感资本）

### A2. 社会熵增模型（Societal Drift）
- 定义无干预趋势函数 `drift(state, dt)`。
- 示例：
  - 财富向高节点集中。
  - 谣言在低信任网络传播速度增加。
  - 压力累积导致角色激进行为阈值下降。

### A3. 世界硬约束（Physical Constants）
- 技术上限、时空限制、魔法守恒、死亡不可逆等。
- 作为校验器：任何 Agent 行动提议必须通过 `constraint_check`。

---

## Layer B：代理意识层（Agentic Soul Layer）

**职责**：将每个角色实现为局部视角、有限理性的自主 Agent。

### B1. 记忆晶格（Memory Lattice）
- 分层记忆：
  - `episodic`（经历）
  - `semantic`（常识与关系）
  - `rumor`（来源不明信息）
- 每条记忆包含：
  - 置信度 `confidence`
  - 情绪权重 `valence`
  - 衰减函数 `decay(t)`
  - 认知偏差标签（确认偏误、投射、防御机制等）

### B2. 欲望矢量（Desire Vector）
- 角色状态向量建议：
  - 生存 `survival`
  - 控制 `control`
  - 归属 `belonging`
  - 自我价值 `self_actualization`
- 每步根据缺口 `need_gap` 计算行动动机：
  - `intent_score = f(need_gap, threat, opportunity, memory_bias)`

### B3. 隐藏面具（Shadow Model）
- 每角色配置：
  - 秘密（可被揭露）
  - 禁忌（触发失控）
  - 恐惧（在压力下改变策略）
- 触发后可暂时覆盖理性策略，生成“非最优但戏剧性高”的行为。

---

## Layer C：叙事探测层（Narrative Extraction Layer）

**职责**：实时检测“值得写”的时刻。

### C1. 冲突侦测器（Conflict Detector）
- 对每个时刻计算：
  - 欲望对冲分 `goal_opposition`
  - 资源重叠分 `resource_collision`
  - 信息不对称分 `info_asymmetry`
  - 关系脆弱分 `relational_fragility`
- 汇总得到张力分：
  - `tension = w1*goal_opposition + w2*resource_collision + w3*info_asymmetry + w4*relational_fragility`

### C2. 命运锚点（Fate Anchor）
- 当 `tension > threshold_high`：
  - 冻结低相关实体更新频率。
  - 提升冲突子图仿真步进精度。
  - 记录高分辨率事件日志用于后续渲染。

### C3. 文学性评估（Literariness Filter）
- 过滤“日常噪声”，保留有轨迹改变的事件：
  - 身份揭露
  - 联盟破裂
  - 关键资源易主
  - 道德底线突破

---

## Layer D：文学呈现层（Stylistic Rendering Layer）

**职责**：把状态轨迹映射为可读、可控文体输出。

### D1. 视角渲染引擎
- 输入：同一事件图 + 视角模板。
- 输出模式：
  - 冷叙事实录（Hemingway-like）
  - 高感知内流（Proust-like）
  - 多角色对照（Rashomon-like）

### D2. 多维输出
- 短对白片段
- 时间轴式冲突报告
- 角色书信体
- 可视化关系动图数据（供前端渲染）

---

## 3. 技术落地建议（按可实现优先）

## 后端/模拟核心
- **Python + LangGraph（MVP）**：快速验证 Agent 编排。
- **Rust（性能阶段）**：把冲突检测与状态推进核心下沉。

## 数据层
- **Neo4j**：关系图、依赖图、联盟结构。
- **向量库（Pinecone 或 pgvector）**：长程记忆召回。
- 建议新增事件日志表：支持时刻回放与“文本可追溯”。

## 前端操作台
- **React + GSAP**：先做 2D 张力仪表盘。
- **Three.js（后续）**：做时空缩放与网络拓扑漫游。

## 文学生成
- LLM 只做“后处理渲染”：
  - 严禁 LLM 直接决定世界状态。
  - LLM 输入必须绑定状态快照 ID 和事件链。

---

## 4. 三阶段执行路线图（可直接开工）

## Step 1：三人密室模拟器（2~4 周）

### 范围
- 3 名 Agent、1 个密闭场景、3 类稀缺资源、每人 1 个秘密。
- 文本界面输出：每回合行为 + 张力指数 + 关键日志。

### 必做能力
1. 回合推进器（tick-based）。
2. 局部记忆与误传机制。
3. 冲突评分函数。
4. 高张力阈值触发的叙事片段生成。

### 验收指标
- 连续 50 回合内至少出现 3 次非模板化冲突。
- 同一初始种子可复现事件骨架。
- 更换随机种子可产生显著差异路径。

## Step 2：视觉化操作台（2~3 周）

### 范围
- 关系网络、情绪热力、欲望雷达图、冲突时间线。
- 支持投放“神谕变量”（天气、信件、意外事故）。

### 验收指标
- 用户可在 30 秒内识别谁在主导冲突。
- 注入变量后 10 回合内张力曲线出现可感知变化。

## Step 3：文学炼金（3~4 周）

### 范围
- 设计 Prompt 矩阵：
  - 文体维度
  - 视角维度
  - 叙事距离维度
- 支持“一事件，多文风”并列输出。

### 验收指标
- 同一事件生成 3 种风格，核心事实一致率 > 95%。
- 读者盲测可区分风格差异。

---

## 5. 关键风险与防崩策略

1. **LLM 抢控制权**：
   - 策略：状态机决定事实，LLM 仅负责表达。
2. **叙事噪声过多**：
   - 策略：提高文学性筛选阈值，按信息增益采样。
3. **Agent 同质化**：
   - 策略：强化 Shadow 参数与认知偏差差异。
4. **可解释性不足**：
   - 策略：每段文本附 `event_trace_id` 与因果链摘要。

---

## 6. 推荐最小数据结构（草案）

```json
{
  "world_state": {
    "tick": 128,
    "resources": {"water": 4, "authority": 7, "secret_docs": 1},
    "constraints": {"tech_level": 2, "magic_budget": 0}
  },
  "agents": [
    {
      "id": "A",
      "desire_vector": {"survival": 0.8, "belonging": 0.2, "control": 0.7},
      "shadow": {"secret": "patricide", "fear": "public_shame"},
      "memory_refs": ["m_102", "m_451"]
    }
  ],
  "detector": {
    "tension": 0.87,
    "anchor": true,
    "event_trace_id": "E-128-04"
  }
}
```

---

## 7. 立刻执行：第一周任务清单（按天排程）

> 目标：在 7 天内交付一个可跑通的「三人密室」MVP，具备**可复现模拟 + 高张力触发叙事**的最小闭环。

### Day 1（模型定义日）
- 产出文件：`schemas/world_state.json`、`schemas/agent_state.json`、`schemas/event_log.json`。
- 明确字段：
  - `world_state`: tick、全局资源池、硬约束。
  - `agent_state`: desire_vector、memory_refs、shadow。
  - `event_log`: actor、target、action、resource_delta、trace_id。
- 任务分解（建议按时段推进）：
  - 09:00-10:30：先定义统一命名与 ID 规范（如 `agent_id`、`event_trace_id`、`snapshot_id`）。
  - 10:30-12:00：完成 `world_state` schema（资源池、时钟、约束、环境变量）。
  - 14:00-15:30：完成 `agent_state` schema（欲望向量、记忆引用、shadow、关系权重）。
  - 15:30-17:00：完成 `event_log` schema（行为类型、参与方、资源变化、因果链指针）。
  - 17:00-18:00：补全示例数据与字段注释，形成 `schemas/examples/*.json`。
- 当日设计约束（必须落实）：
  - 所有状态对象必须带 `version`，保证后续 schema 演进兼容。
  - 所有“可计算字段”要标明来源（原始输入 / 运行时派生），避免歧义。
  - `event_log` 必须能反向追踪到触发它的上游状态（`cause_refs`）。
- 快速验收命令（Day 1 结束前必须可跑）：
  - `python -m jsonschema -i schemas/examples/world_state.sample.json schemas/world_state.json`
  - `python -m jsonschema -i schemas/examples/agent_state.sample.json schemas/agent_state.json`
  - `python -m jsonschema -i schemas/examples/event_log.sample.json schemas/event_log.json`
- 完成 DoD（Definition of Done）：
  - 三个 schema 可通过 JSON Schema 校验。
  - 每个字段有注释说明与示例。
  - 任取一条 `event_log` 都能追溯到至少一个 `agent_state`/`world_state` 快照。

### Day 2（回合引擎日）
- 实现 `simulate.py` 最小循环：
  - 输入随机种子。
  - 运行 30 tick。
  - 每 tick 输出结构化事件日志。
- 关键函数：`step_world()`、`step_agent()`、`apply_constraints()`。
- 引擎实现建议（继续设计）：
  - 调度顺序：`world_drift -> agent_update -> action_select -> apply_delta -> score_tension -> emit_event`。
  - 每 tick 最少产出 1 条 `event_log`，并附带 `metrics`（四项分量 + 总张力）。
  - 当 `tension > 0.78` 时写入 `fate_anchor=true`，用于后续 Day 6 文学渲染触发。
  - 输出文件使用 JSONL，便于流式回放与后处理。
- CLI 约定：
  - `python3 scripts/simulate.py --seed 42 --ticks 30 --out runs/run_42.jsonl`
  - 输出中必须包含 `event_trace_id` + `cause_refs`（满足可追溯）。
- DoD：
  - 命令行可执行：`python simulate.py --seed 42 --ticks 30`。
  - 运行结束可导出 `run_*.jsonl`。
  - 可统计到至少一个张力峰值（例如 `tension > 0.75`）。

### Day 3（记忆与误传日）
- 增加记忆写入与召回：`episodic / semantic / rumor`。
- 加入“误传概率”机制（rumor distortion）。
- 机制细化（继续设计）：
  - 行为发生后，Actor 写入 `episodic memory`（高置信）。
  - Target 写入 `rumor memory`（中置信 + 扭曲衰减）。
  - 每 tick 对历史记忆执行 `confidence_decay`，并保留 `source_event_id` 追因。
  - 当动作为 `lie / threaten / withhold` 时，提高误传扭曲系数。
- 建议观测指标：
  - `memory_divergence`: 同一 `source_event_id` 在不同角色记忆中的置信度差。
  - `rumor_distortion`: 当 tick 的平均误传扭曲值。
- DoD：
  - 同一事件在不同角色记忆中出现可追踪偏差。
  - 日志可看到记忆衰减与置信度变化。
  - 每 tick 日志包含 `memory_update`（新增/衰减结果）。

### Day 4（冲突评分日）
- 实现第一版 `tension_score()`：
  - `goal_opposition`
  - `resource_collision`
  - `info_asymmetry`
  - `relational_fragility`
- 输出张力曲线 `tension_timeline`。
- DoD：
  - 每 tick 有可解释的分项得分。
  - 至少能识别 2 类典型冲突（资源争夺/身份冲突）。

### Day 5（命运锚点日）
- 实现阈值触发：`if tension > threshold_high -> fate_anchor`。
- 锚点时刻记录高分辨率快照：`state_snapshot_id`、`event_trace_id`。
- DoD：
  - 一次 30 tick 运行中可触发并保存至少 1 个锚点。
  - 锚点事件可从日志回放。

### Day 6（文学渲染接入日）
- 接入 LLM 渲染模板（仅后处理）：
  - 输入：`state_snapshot + event_trace + pov + style`。
  - 输出：200~400 字冲突片段。
- 加入事实约束检查，确保“文风变化不改变事件事实”。
- DoD：
  - 同一锚点可输出 2 种风格文本。
  - 关键事实一致率达到预设阈值（建议 >95%）。

### Day 7（测试验收日）
- 建立回归测试：
  - 固定种子快照比对。
  - 随机种子差异度检测。
  - 张力峰值存在性测试。
- 输出周报：
  - 成功样例 3 条。
  - 失败样例与修复优先级。
  - 下周迭代 backlog。
- DoD：
  - `seed=42` 结果可复现。
  - `seed=43/44` 结果存在显著路径差异。
  - 至少 3 段可读冲突文本可追溯到事件链。

### 本周交付物（Checklist）
- [ ] 可运行 CLI 模拟器（30 tick）。
- [ ] 三层核心数据结构（world/agent/event）。
- [ ] 张力曲线与命运锚点检测。
- [ ] 最小文学渲染链路（基于锚点触发）。
- [ ] 可复现测试与回放日志。

### 最低成功标准（周末验收口径）
1. 你可以“投一个初始种子”，得到一条完整事件链。
2. 系统能自动指出“最高张力时刻”并解释为什么。
3. 点击该时刻，可生成一段可读、可追溯的文学片段。
4. 换随机种子后，故事轨迹会明显变化，但规则保持一致。

> 结论：你的方向非常前沿。最重要的是先做“可运行的动力核心”，而不是先追求华丽文本。只要底层冲突机制成立，文学性可以被持续放大。
