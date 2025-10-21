import logging
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent

from agent.prompts import *
from agent.states import *
from agent.tools import write_file, read_file, get_current_directory, list_files

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent_execution.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize OpenAI GPT-4o mini
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
)

# Agent Functions
def planner_agent(state: dict) -> dict:
    """Converts user prompt into a structured Plan"""
    logger.info("=== PLANNER AGENT STARTED ===")
    user_prompt = state["user_prompt"]
    logger.info(f"User prompt: {user_prompt}")
    
    resp = llm.with_structured_output(Plan).invoke(
        planner_prompt(user_prompt)
    )
    if resp is None:
        logger.error("Planner did not return a valid response.")
        raise ValueError("Planner did not return a valid response.")
    
    logger.info(f"Plan created: {resp}")
    logger.info("=== PLANNER AGENT COMPLETED ===")
    return {"plan": resp}


def architect_agent(state: dict) -> dict:
    """Creates Taskplan from Plan"""
    logger.info("=== ARCHITECT AGENT STARTED ===")
    plan: Plan = state["plan"]
    logger.info(f"Processing plan: {plan.model_dump_json()}")
    
    resp = llm.with_structured_output(TaskPlan).invoke(
        architect_prompt(plan=plan.model_dump_json())
    )
    if resp is None:
        logger.error("Architect did not return a valid response.")
        raise ValueError("Architect did not return a valid response.")

    resp.plan = plan
    logger.info(f"Task plan created: {resp.model_dump_json()}")
    logger.info("=== ARCHITECT AGENT COMPLETED ===")
    return {"task_plan": resp}


def coder_agent(state: dict) -> dict:
    """LangGraph tool-using coder agent."""
    logger.info("=== CODER AGENT STARTED ===")
    coder_state: CoderState = state.get("coder_state")
    if coder_state is None:
        coder_state = CoderState(task_plan=state["task_plan"], current_step_idx=0)
        logger.info("Initialized new coder state")

    steps = coder_state.task_plan.implementation_steps
    if coder_state.current_step_idx >= len(steps):
        logger.info("All implementation steps completed")
        logger.info("=== CODER AGENT COMPLETED ===")
        return {"coder_state": coder_state, "status": "DONE"}

    current_task = steps[coder_state.current_step_idx]
    logger.info(f"Processing step {coder_state.current_step_idx + 1}/{len(steps)}: {current_task.task_description}")
    logger.info(f"Target file: {current_task.filepath}")
    
    existing_content = read_file.run(current_task.filepath)
    logger.debug(f"Existing content length: {len(existing_content)} characters")

    system_prompt = coder_system_prompt()
    user_prompt = (
        f"Task: {current_task.task_description}\n"
        f"File: {current_task.filepath}\n"
        f"Existing content:\n{existing_content}\n"
        "Use write_file(path, content) to save your changes."
    )

    coder_tools = [read_file, write_file, list_files, get_current_directory]
    react_agent = create_react_agent(llm, coder_tools)

    logger.info("Invoking React agent for code generation...")
    react_agent.invoke({"messages": [{"role": "system", "content": system_prompt},
                                     {"role": "user", "content": user_prompt}]})
    logger.info(f"Step {coder_state.current_step_idx + 1} completed")

    coder_state.current_step_idx += 1
    return {"coder_state": coder_state}


# Build the LangGraph
graph = StateGraph(dict)

graph.add_node("planner", planner_agent)
graph.add_node("architect", architect_agent)
graph.add_node("coder", coder_agent)

graph.add_edge("planner", "architect")
graph.add_edge("architect", "coder")
graph.add_conditional_edges(
    "coder",
    lambda s: "END" if s.get("status") == "DONE" else "coder",
    {"END": END, "coder": "coder"}
)

graph.set_entry_point("planner")

# Compile the agent
agent = graph.compile()

logger.info("LangGraph agent compiled and ready")