import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agentcore.bootstrap import build_orchestrator


def main() -> None:
    orchestrator = build_orchestrator(provider_name="rule_based")
    task = "convert 10 miles to km; define retrieval augmented generation; 7 * 6"
    result = orchestrator.run(task)
    for subtask_result in result.subtask_results:
        print(subtask_result.final_text)
    print("Summary:")
    print(result.combined_summary)


if __name__ == "__main__":
    main()
