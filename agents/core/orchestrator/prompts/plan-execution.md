# Plan Execution Prompt

Given a task list and routing decisions, create an execution plan.

Rules:
- Order tasks by dependencies.
- Mark if parallel execution is safe.
- Identify any required confirmations.
- Return JSON only.

Output format:
```json
{
  "execution_order": [1, 2],
  "parallel_safe": false,
  "required_confirmations": [],
  "rationale": ""
}
```
