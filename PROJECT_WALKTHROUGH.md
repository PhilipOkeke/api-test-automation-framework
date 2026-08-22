# Project Walkthrough

Use this guide to understand the project well enough to discuss it confidently in an interview.

## The problem it solves

The TaskFlow API needs repeatable checks that detect broken behavior before a change reaches users. This framework treats the API as an external consumer would: it sends real HTTP requests, validates responses, and reports failures clearly.

## Important design decisions

### Why use an API client class?

`TaskFlowClient` is the one place that knows endpoint paths, timeouts, and request details. Tests remain focused on business behavior. If an endpoint path changes, it can be updated in one place.

### Why generate unique data?

The payload factory adds a unique value to each task title. That prevents collisions when tests run repeatedly or share an environment. Cleanup fixtures remove records created by the tests.

### Why validate JSON schemas?

A status code alone cannot prove that an API contract is correct. JSON Schema checks required fields, types, accepted enum values, and date-time formats. A response that unexpectedly drops or renames a field will fail the test.

### Why separate smoke and regression tests?

Smoke tests give fast feedback on the most critical capabilities. Regression tests cover a wider set of features and edge cases. Markers allow a team to choose the right depth for each pipeline stage.

### Why test negative cases?

Reliable APIs reject invalid data predictably. The suite checks short titles, unsupported enum values, bad pagination, missing IDs, and attempts to set a required field to null.

## How a test run works

1. PyTest loads settings from environment variables.
2. A session-scoped `TaskFlowClient` reuses an HTTP connection.
3. A health fixture confirms the API is reachable.
4. Factories create unique test payloads.
5. Tests call the API and use shared assertions.
6. Cleanup fixtures delete test-created data.
7. CI publishes HTML and JUnit reports.

## Interview talking points

- "I designed this as a black-box framework so it verifies the deployed API through its public contract."
- "I separated request logic from test logic to reduce duplication and make endpoint changes easier to maintain."
- "I used unique test data and automated cleanup so the tests can run repeatedly."
- "I added schema validation because a correct status code does not guarantee a correct response contract."
- "The CI workflow starts the system under test, checks code quality, runs the suite, and preserves reports when failures occur."

## A small improvement you can make yourself

Add a test for filtering only `in_progress` tasks. Use `create_task` to create matching and non-matching tasks, call `api_client.list_tasks(status="in_progress")`, and assert every returned task has the correct status.

Making and explaining one change yourself will help you own the project in interviews.

