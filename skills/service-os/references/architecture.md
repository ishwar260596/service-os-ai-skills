# Service OS workflow context

Source snapshot: central-service-os-app commit `496c84f4e609137efc0980ab2226e2f0a61ed101`, inspected 2026-10-19. Logger dependency resolved to AckoFlutterPlugins `46e2df71183bc6ee9c63b232324efadaf8ad1666`. These are source provenance, not deployed versions. Match an incident release before using source behavior as its cause. Normal users do not need a source checkout.

## Task listing and identity

`lib/features/allTasks/repo/tasks_repo.dart` computes an end date one day after the selected start, queries by assignee/date/status and paginates with size 50. Older-day requests add `done`; offline reads use cached date-range keys. Distinguish request failure, response exclusion, pagination, cache and display categorization. The inspected path logs success locally and failures remotely; missing remote success is expected.

`lib/features/login/utility/auth_utility.dart` sets the Crashlytics/Analytics user ID to assigneeId and sends an `AssigneeID assigned` event through the logger manager. FE ID equals assigneeId; Job ID equals taskId. Identity can be absent before login or in headless work.

## Workflow and Start Trip

`features/taskFlow/` fetches/caches task configuration, splits pages, persists input variables and resumes visited pages. `features/taskScreen/` renders server-driven widgets and evaluates action/input/navigation rules. Available buttons and action order vary with actual journey config. Local start callbacks, click-time location/geofence, network validation, and accepted task updates are separate stages. Continuous location tracking is another path; its failure alone does not establish task-start failure.

## Photo and task sync

`utilities/sdui/actions/upload_file_action.dart`: local file lookup -> compression (with retry/fallback behavior) -> upload -> document-reference persistence. `features/task_sync/task_executor.dart` executes queued subtasks; `tasks_sync_manager.dart` orchestrates execution and records selected failures in Crashlytics. A successful upload does not prove its reference was saved or the dependent completion update succeeded.

`utilities/storage/offline/offline_manager.dart` stores offline requests and progress. UI completion, queueing, one subtask completion, accepted final update and dashboard refresh are distinct observations. Never clear pending local data as a generic troubleshooting step.

## Telemetry interpretation

Read `logging-coverage.md` before drawing conclusions from absent records. The `firebase: true` logger flag routes through the logger manager; its name does not mean every forwarded record reaches Crashlytics. Task IDs must actually appear in remote messages/payloads to be searchable. This skill queries dashboards only; it does not call task/business APIs.
