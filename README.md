# Web Builder

An AI-powered web development assistant built with LangGraph and OpenAI. This tool leverages advanced language models to automate website creation, file management, and project scaffolding within a secure, sandboxed environment.

## Workflow

The Web Builder uses a LangGraph-based architecture to process user requests through a series of AI agents. Below is a visual representation of the workflow:

```mermaid
flowchart TD
    Start([User Prompt]) --> Planner[Planner Agent: Converts prompt to Plan]
    Planner --> Architect[Architect Agent: Creates TaskPlan]
    Architect --> Coder[Coder Agent: Processes implementation steps]
    Coder --> Check{All steps completed?}
    Check -->|Yes| End([Project Generated])
    Check -->|No| Coder
```

- **Planner Agent**: Analyzes the user's prompt and generates a high-level plan.
- **Architect Agent**: Breaks down the plan into actionable tasks.
- **Coder Agent**: Executes each task using tools to generate and modify files. It iterates until all tasks are complete.

This modular design ensures a structured and iterative approach to web development.

1. **Clone the Repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd web-builder
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Environment Variables**:
   - Copy `.env.example` to `.env` (if provided) or create a new `.env` file in the `agent/` directory.
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```
   - Ensure other necessary variables (e.g., for LangSmith or additional services) are configured as needed.

2. **Project Root Initialization**:
   - The agent dynamically sets `PROJECT_ROOT` for secure file operations. Ensure your working directory is correctly configured.

## Usage

1. **Run the Agent**:
   - Navigate to the project root and execute the main script (e.g., if a `main.py` or entry point exists):
     ```bash
     python -m agent.graph  # Adjust based on your entry point
     ```
   - Interact with the agent via prompts or input to describe the website you want to build.

2. **Generate Projects**:
   - The agent will create new project directories (e.g., `generated_project_1`) containing generated files, HTML, CSS, JavaScript, and other assets based on your specifications.
   - Use the provided tools for file creation, editing, and command execution within the secure boundaries.

3. **Monitor Logs**:
   - Check `agent_execution.log` for detailed execution history and any errors.

## Project Structure

```
web-builder/
├── agent/
│   ├── graph.py          # Main LangGraph workflow definition
│   ├── tools.py          # File system and utility tools
│   ├── prompts.py        # Prompt templates for the AI agent
│   ├── states.py         # State management for the graph
│   └── .env              # Environment configuration
├── generated_project_*/  # Output directories for generated projects
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Dependencies

- **LangChain & LangGraph**: For building the AI agent and workflow.
- **OpenAI**: For language model interactions.
- **Python-DotEnv**: For loading environment variables.
- **Pydantic**: For data validation.
- **LangSmith**: For tracing and debugging (optional but recommended).

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues or questions, please open an issue on the repository or refer to the execution logs for debugging information.

---

*Built with ❤️ using LangGraph and OpenAI.*
