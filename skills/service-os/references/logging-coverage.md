# Logging coverage

Source snapshot: app commit `496c84f4e609137efc0980ab2226e2f0a61ed101`, logger dependency `46e2df71183bc6ee9c63b232324efadaf8ad1666`, reviewed 2026-10-19. Verify against the affected app version before source-level conclusions. This describes call sites, not guaranteed delivery or retention. Repository paths below are optional source pointers; users don't need the app checkout.

## Routing

`lib/utilities/logger/file_logger/logger.dart` forwards every error and any `firebase: true` call to `AckoLoggerManager`. Despite the flag name, the resolved dependency enables Coralogix; its Firebase logger is commented out. Forwarded non-errors become info. Other calls remain console/local-file logs. The logger's separate `taskId` argument isn't structured metadata: IDs must appear in messages/payloads to be searchable.

Firebase receives explicit `recordError`/`recordFlutterError` calls separately, not the entire operational stream. Local rotating filenames don't prove date coverage; inspect timestamps.

| Operation / source pointer | Remote evidence and gaps |
|---|---|
| `features/allTasks/repo/tasks_repo.dart` | Task-list failures forwarded; called/success local-only; no explicit remote success filters/response log in this path |
| `utilities/network/helpers/network_helper.dart` | cURL after helper calls return; doesn't cover every direct networking call or prove response status |
| `utilities/network/interceptors/access_code_interceptor.dart` | Network errors with URL/status/response; 401/logout evidence; not all errors explicitly sent to Crashlytics |
| `features/taskFlow/repo/task_config_repo.dart` | Input-update helper forwards maps/changes; several direct fetch/config messages local-only |
| `features/task_sync/task_executor.dart` | Selected action responses, subtask completions, null-response/DB failures; many routine decisions local-only |
| `features/task_sync/tasks_sync_manager.dart` | Caught executor failures also explicitly recorded in Crashlytics |
| `utilities/sdui/actions/upload_file_action.dart` | Error-level compression/missing-file events; explicit Crashlytics compression exceptions/missing files; routine progress mostly local-only |
| `utilities/sdui/actions/service_os_network_actions.dart` | Selected input values/stale-version/battery events; null lookup logs don't prove final request fields were null, because config/click-time props may supply values |
| `utilities/utils/location/`, `utilities/sdui/util.dart` | Tracking/window/location/distance diagnostics; selected location exceptions also in Crashlytics |
| `main.dart` | Flutter handler logs and Firebase exception recording; not all operational failures throw |
| `features/login/utility/auth_utility.dart` | Assignee assignment/logout; Crashlytics user identifier is FE ID, with no guaranteed structured job key |

An invalid location window produces a disabled-tracking fallback in inspected code. Stopped tracking doesn't itself prove a failed task-status update. Context can be blank before attachment or in headless execution: correlate explicit identity and session evidence, not device model alone.

Payloads may contain task inputs, request headers/bodies, notification text, exact coordinates, and document URLs. No general redaction layer was found. Redact tokens/cookies/customer contacts/signed URLs and unnecessary coordinates from reports and packages.

If source inspection is available, match its release/build. The latest checkout isn't automatically the installed or historical code. Ship these coverage notes, not the whole source tree.
