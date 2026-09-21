import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agentcore.bootstrap import build_agent


def main() -> None:
    agent = build_agent(provider_name="rule_based")
    queries = [
        "define agentic ai",
        "convert 5 km to m",
        "18 / 3",
        "summarize: Agentic AI systems combine language models with tools. They plan multi step tasks and call external functions to complete goals. Responsible use requires guardrails, logging and human oversight.",
    ]
    for query in queries:
        result = agent.run(query)
        print(f"Query: {query}")
        print(f"Response: {result.final_text}")
        print("-")


if __name__ == "__main__":
    main()
