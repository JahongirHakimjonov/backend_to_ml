# AI Agents

## 🎯 Maqsad

Bu bobni o'qib bo'lgach:
- AI Agent nima va oddiy LLM call'dan farqini bilasiz
- Tool use / Function calling bilan agent yarata olasiz
- Multi-agent sistemalar (CrewAI, AutoGen, LangGraph) bilan ishlay olasiz
- Production-ready agent backend qura olasiz
- Agent xavfsizligi va monitoring'ni bilasiz

## 📖 Nimani o'rganish kerak

- **Agent nima** — LLM + tools + memory + planning
- **ReAct pattern** — Reasoning + Acting
- **Tool use / Function calling**
- **Memory** — short-term va long-term
- **Multi-agent** — CrewAI, AutoGen, LangGraph
- **Agentic workflows** — sequential, parallel, conditional
- **MCP (Model Context Protocol)** — Anthropic'ning yangi standarti
- **Agent xavfsizligi** — sandbox, permissions
- **Observability** — Langfuse, agent traces

## 🧠 Agent nima?

```
Simple LLM call:
  Input → LLM → Output

Agent:
  Goal → Plan → Action → Observation → ... → Final answer
                    ↓
              Tools (search, code, DB, API)
                    ↓
              Memory (history, context)
```

**Agent = LLM + Loop + Tools + Memory**

### Agent levels (sodda → murakkab)

1. **Simple chatbot** — bitta savolga bitta javob
2. **Tool-using agent** — calculator, search, weather API
3. **ReAct agent** — Thought → Action → Observation cycle
4. **Multi-agent** — bir necha specialized agent hamkorlikda
5. **Autonomous agent** — uzoq goal'larni mustaqil yechadi (eksperiment)

## 💻 Kod misollari

### Simple agent — Pydantic AI

```python
from pydantic_ai import Agent
from pydantic_ai.tools import RunContext

agent = Agent(
    model="openai:gpt-4o-mini",
    system_prompt="Sen yordamchi assistantsan. Tool'lardan foydalan.",
)

@agent.tool
def get_weather(ctx: RunContext, city: str) -> str:
    """Berilgan shahar uchun ob-havoni qaytaradi."""
    # Real API call
    return f"{city}: 22°C, quyoshli"

@agent.tool
def calculator(ctx: RunContext, expression: str) -> float:
    """Matematik ifoda hisoblaydi."""
    # Diqqat: eval xavfli, sandbox kerak production'da
    return eval(expression)

@agent.tool
async def search_web(ctx: RunContext, query: str) -> str:
    """Internetdan qidiradi."""
    # Tavily, Serper, Brave Search API
    return await tavily_search(query)

# Run
result = await agent.run("Toshkent havosi va 25*4 qancha?")
print(result.data)
```

### Manual ReAct loop (raw API)

```python
from anthropic import AsyncAnthropic
import json

client = AsyncAnthropic()

tools = [
    {
        "name": "search",
        "description": "Internet search",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    },
    {
        "name": "calculator",
        "description": "Mathematical calculation",
        "input_schema": {
            "type": "object",
            "properties": {"expression": {"type": "string"}},
            "required": ["expression"],
        },
    },
]

async def execute_tool(name: str, args: dict) -> str:
    if name == "search":
        return await search_web(args["query"])
    elif name == "calculator":
        return str(eval(args["expression"]))
    else:
        return "Unknown tool"

async def run_agent(user_input: str, max_iterations: int = 10):
    messages = [{"role": "user", "content": user_input}]
    
    for _ in range(max_iterations):
        response = await client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            tools=tools,
            messages=messages,
        )
        
        # Check if model wants to use tools
        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = await execute_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })
            
            messages.append({"role": "user", "content": tool_results})
        else:
            # Final answer
            return response.content[0].text
    
    return "Max iterations reached"

# Run
result = await run_agent("Toshkent havosi va 25*4 qancha?")
print(result)
```

### CrewAI — multi-agent

```python
from crewai import Agent, Task, Crew, Process

# Define agents (har biri specialist)
researcher = Agent(
    role="Senior Research Analyst",
    goal="Provide deep, accurate research on given topics",
    backstory="Sen 10 yillik tajribali analitiksan...",
    tools=[search_tool, web_scraper_tool],
    llm="gpt-4o-mini",
)

writer = Agent(
    role="Tech Content Strategist",
    goal="Write clear, engaging articles based on research",
    backstory="Sen mashhur tech writerssan...",
    tools=[markdown_tool],
    llm="claude-sonnet-4-6",
)

editor = Agent(
    role="Senior Editor",
    goal="Review and polish articles for publication",
    backstory="Sen 15 yil davomida texnik kitoblar muharririsan...",
    tools=[grammar_tool],
    llm="claude-haiku-4-5",
)

# Define tasks
research_task = Task(
    description="Research the latest trends in AI agents (2025-2026)",
    expected_output="A detailed research report with citations",
    agent=researcher,
)

write_task = Task(
    description="Write a 1500-word article based on research",
    expected_output="A complete article in markdown",
    agent=writer,
    context=[research_task],  # depends on research
)

edit_task = Task(
    description="Review and polish the article",
    expected_output="Final publication-ready article",
    agent=editor,
    context=[write_task],
)

# Crew (collaboration)
crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, write_task, edit_task],
    process=Process.sequential,  # yoki Process.hierarchical
)

result = crew.kickoff()
print(result)
```

### LangGraph — stateful workflows

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    next_action: str
    iterations: int

# Nodes
def planner(state):
    """Decide what to do next."""
    last_msg = state["messages"][-1] if state["messages"] else ""
    
    if state["iterations"] > 5:
        return {"next_action": "finish"}
    
    # Use LLM to plan
    response = client.chat.completions.create(...)
    return {"next_action": response.choices[0].message.content}

def search_node(state):
    """Run web search."""
    query = state["messages"][-1]
    result = search_web(query)
    return {"messages": [result], "iterations": state["iterations"] + 1}

def code_node(state):
    """Execute code."""
    code = state["messages"][-1]
    result = execute_code_sandbox(code)
    return {"messages": [result], "iterations": state["iterations"] + 1}

def finish_node(state):
    """Generate final answer."""
    response = client.chat.completions.create(...)
    return {"messages": [response.choices[0].message.content]}

# Build graph
workflow = StateGraph(AgentState)
workflow.add_node("planner", planner)
workflow.add_node("search", search_node)
workflow.add_node("code", code_node)
workflow.add_node("finish", finish_node)

workflow.set_entry_point("planner")

# Conditional routing
def route(state):
    action = state["next_action"]
    if action == "finish":
        return "finish"
    elif "search" in action.lower():
        return "search"
    elif "code" in action.lower():
        return "code"
    else:
        return "planner"

workflow.add_conditional_edges("planner", route, {
    "search": "search",
    "code": "code",
    "finish": "finish",
    "planner": "planner",
})

workflow.add_edge("search", "planner")
workflow.add_edge("code", "planner")
workflow.add_edge("finish", END)

app = workflow.compile()

# Run
result = app.invoke({"messages": ["Build a Python TODO app"], "iterations": 0})
```

### MCP (Model Context Protocol) — Anthropic's standard

MCP — bu agent va tool'lar orasidagi standart protokol. 2024'da paydo bo'ldi.

```python
# MCP server (oddiy)
from mcp.server import Server
from mcp.types import Tool

server = Server("my-tools")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [Tool(
        name="get_database_info",
        description="Get info from internal DB",
        inputSchema={
            "type": "object",
            "properties": {"table": {"type": "string"}},
        },
    )]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "get_database_info":
        return [{"type": "text", "text": query_db(arguments["table"])}]
```

Endi har qanday MCP-compatible client (Claude Desktop, Cline, va h.k.) bu tool'ni avtomatik ishlatadi.

### Agent xavfsizligi

```python
# Tool execution sandbox
import resource
import subprocess

def execute_code_sandbox(code: str, timeout: int = 5, memory_mb: int = 256):
    """Restricted code execution."""
    
    # Variant 1: subprocess + ulimit
    try:
        result = subprocess.run(
            ["python", "-c", code],
            timeout=timeout,
            capture_output=True,
            text=True,
            # Resource limits via preexec_fn
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        return "Code execution timed out"
    
    # Variant 2: Docker container (production)
    # Variant 3: WebAssembly (browser-grade isolation)
    # Variant 4: E2B (cloud sandbox)

# Permission system
ALLOWED_TOOLS = {
    "user_123": ["search", "calculator"],
    "admin_456": ["search", "calculator", "execute_code", "db_query"],
}

def check_permission(user_id: str, tool: str) -> bool:
    return tool in ALLOWED_TOOLS.get(user_id, [])
```

## 🔌 Backend integratsiyasi

### Agent FastAPI service

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class AgentRequest(BaseModel):
    user_id: str
    goal: str
    available_tools: list[str] = []
    max_iterations: int = 10

class AgentResponse(BaseModel):
    final_answer: str
    iterations: int
    tool_calls: list[dict]
    cost_usd: float

@app.post("/agent/run", response_model=AgentResponse)
async def run_agent_endpoint(req: AgentRequest):
    # Permission check
    allowed = [t for t in req.available_tools if check_permission(req.user_id, t)]
    
    if not allowed:
        raise HTTPException(403, "No tools available for user")
    
    # Run agent
    result = await run_agent(
        user_input=req.goal,
        tools=allowed,
        max_iterations=req.max_iterations,
    )
    
    return AgentResponse(**result)
```

### Streaming agent traces (Langfuse)

```python
from langfuse import Langfuse

langfuse = Langfuse()

async def run_traced_agent(user_input: str, user_id: str):
    trace = langfuse.trace(
        name="customer_support_agent",
        user_id=user_id,
        input=user_input,
    )
    
    for iteration in range(10):
        # LLM call
        span = trace.span(name=f"llm_call_{iteration}")
        response = await client.messages.create(...)
        span.end(output=response.content[0].text)
        
        # Tool call
        if response.stop_reason == "tool_use":
            tool_span = trace.span(name=f"tool_{tool_name}")
            result = await execute_tool(...)
            tool_span.end(output=result)
    
    trace.update(output=final_answer)
    return final_answer
```

## 📚 Resurslar

- **Anthropic — "Building effective agents"** ([blog post](https://www.anthropic.com/research/building-effective-agents))
- **MCP docs** — [modelcontextprotocol.io](https://modelcontextprotocol.io/)
- **CrewAI docs** — [docs.crewai.com](https://docs.crewai.com/)
- **AutoGen docs** — [microsoft.github.io/autogen](https://microsoft.github.io/autogen/)
- **LangGraph docs** — [langchain-ai.github.io/langgraph](https://langchain-ai.github.io/langgraph/)
- **Pydantic AI** — [ai.pydantic.dev](https://ai.pydantic.dev/)
- **ReAct paper** — Yao et al., 2022

## 🏋️ Mashqlar

### 🟢 Easy
1. 3 ta tool (calculator, weather, time) bilan oddiy agent.
2. Pydantic AI bilan structured agent.
3. CrewAI quickstart — 2 agentli pipeline.

### 🟡 Medium
1. **ReAct loop**: manual implementation — Thought → Action → Observation.
2. **Multi-tool agent**: search + DB query + email send.
3. **LangGraph workflow**: 4 nodali conditional graph.

### 🔴 Hard
1. **Production agent backend**: FastAPI + Postgres (memory) + Redis + Langfuse + permissions.
2. **MCP server**: o'z tool'laringizni MCP-compatible qiling, Claude Desktop bilan ishlating.
3. **Multi-agent debate**: 3 ta agent (proponent, opponent, judge) — savol bo'yicha debat → consensus.

## 🚀 Capstone

`notebooks/month-05/07_ai_agents.ipynb`:
- **Loyiha:** "Customer Support Agent" o'zbek tilida
- Tools: search FAQ, DB query (orders), refund, escalate
- LangGraph workflow
- Memory (Postgres)
- Telegram bot integration
- Langfuse traces

## ✅ Tekshirish ro'yxati

- [ ] Agent vs simple LLM call farqini bilaman
- [ ] ReAct pattern
- [ ] Tool use (OpenAI function calling, Anthropic tool use)
- [ ] Pydantic AI bilan agent yozish
- [ ] CrewAI / LangGraph multi-agent
- [ ] Memory implementation (short + long term)
- [ ] Tool sandbox xavfsizligi
- [ ] Observability (Langfuse)

[Fine-tuning](./08-fine-tuning.md) ga o'tamiz — oxirgi bobga.
