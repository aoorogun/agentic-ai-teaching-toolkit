from __future__ import annotations
import argparse
import json

from agentcore.bootstrap import build_agent, build_default_registry, build_orchestrator


def _run_command(args: argparse.Namespace) -> None:
    agent = build_agent(provider_name=args.provider, model_name=args.model)
    result = agent.run(args.query)
    print(result.final_text)


def _orchestrate_command(args: argparse.Namespace) -> None:
    orchestrator = build_orchestrator(provider_name=args.provider, model_name=args.model)
    result = orchestrator.run(args.task)
    for subtask_result in result.subtask_results:
        print(subtask_result.final_text)
    print(result.combined_summary)


def _list_tools_command(args: argparse.Namespace) -> None:
    registry = build_default_registry()
    print(json.dumps(registry.list_specs(), indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agentcore")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("query")
    run_parser.add_argument("--provider", default="rule_based")
    run_parser.add_argument("--model", default="claude-sonnet-4-6")
    run_parser.set_defaults(func=_run_command)

    orchestrate_parser = subparsers.add_parser("orchestrate")
    orchestrate_parser.add_argument("task")
    orchestrate_parser.add_argument("--provider", default="rule_based")
    orchestrate_parser.add_argument("--model", default="claude-sonnet-4-6")
    orchestrate_parser.set_defaults(func=_orchestrate_command)

    list_tools_parser = subparsers.add_parser("list-tools")
    list_tools_parser.set_defaults(func=_list_tools_command)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
