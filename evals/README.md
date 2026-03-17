# Evals

This directory exists to verify outcomes, not just agent text.

## Core concepts

- Task: one scenario with a clear goal.
- Trial: one run of the task.
- Transcript: the recorded steps taken during the run.
- Outcome: the final state in the environment.
- Grader: the logic or rubric used to score the result.

## Recommended structure

- Put task definitions in `evals/tasks/`.
- Put grader notes or grader code in `evals/graders/`.
- Record outcomes in whatever artifact format fits your project.

## Evaluation guidance

- Prefer end-state checks over stylistic checks.
- Use multiple trials for unstable tasks.
- Combine code-based graders with occasional human calibration.
- Read transcripts when scores move unexpectedly.
- Turn production failures into regression evals.