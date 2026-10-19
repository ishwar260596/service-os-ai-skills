# Issue playbooks

Select the symptom first. Generic errors are leads, not diagnoses. Multiple categories can apply.

## Missing task

Trace assignment notification if available → date/status selection → task-list request → response → pagination → categorization/cache. Check historical assignment/reassignment/cancellation evidence, scheduled interval, `from_date_time`, `to_date_time`, status filters, page/size, failures, offline fallback. Distinguish not returned by API from returned but not displayed. Mobile success filters/response may be absent. Name missing assignment/response evidence rather than accessing backend systems.

To claim date exclusion, require the actual request interval and task schedule, normalize timezones, and verify the relevant API inclusion behavior. A schedule screenshot alone doesn't establish the sent interval.

## Start Trip absent, disabled, or unsuccessful

Distinguish absent button, disabled button, no response after tap, and locally started but dashboard unchanged. Trace task config/page → visibility/required-input rules → tap → one-shot location/geofence → validation API if configured → queued update → executor response → later state. Search `Start task`, `validate-start-trip`, task-update URLs, `FooterLocationDiagnostics`, distance validation, executor messages. Journey actions/order vary; inspect actual configuration when available.

The local `start_task` callback changes app state and records battery information; it isn't proof of accepted backend `in_progress`. Continuous tracking is separate from click-time location/task updates. Empty tracking windows or a kill switch cannot explain a blocked task start without linking evidence.

## Photo upload/sync

Trace each photo/input key: selected → local path saved → file exists → compression → upload → returned document references → persisted local replacement → dependent task update → subtask complete.

Check missing files, empty document inputs, compression timeouts/exceptions, resource limits, transport/auth/server failures, malformed responses, persistence failure, and failed downstream actions. Compression may fall back to the original file: check subsequent upload before labeling it terminal. “Upload end” isn't success. Successful upload followed by failed persistence is a different failure stage. Local-only stages may require a file attachment.

## Stuck sync

Identify the first unfinished action/input key. Check pending actions, execution start, connectivity, overlapping execution, cache/version changes, HTTP 409, network response, persistence, retries, service errors, final callbacks. Match the same execution/cache where evidence allows. A queued action, response, persisted completion, and final task state are distinct stages. One subtask complete isn't whole-task sync. Don't recommend clearing the DB, reinstalling, or logging out as a generic remedy for unsynced data.

## Completed locally, incomplete on dashboard

Trace user-completed metadata → pending uploads/updates → completion request → acceptance → app refresh. Establish whether a preceding failure blocked the completion request, it was rejected, or acceptance exists but dashboard state is unavailable. Don't infer dashboard implementation failure from mobile-only evidence.

## Cross-cutting checks

- Auth: 401 → refresh/recovery or logout; a recovered 401 needn't block a task.
- Network: no connection, slow response, timeout, HTTP rejection, and unusable success payload are different.
- Resources/services: missing file, memory/storage pressure, process exit, background-service interruption; use actual exit timestamps, not only later reporting time.
- Flutter errors: correlate stack/session/action; a home-screen error doesn't automatically explain this task.
- Stale config/reassignment: require response/state evidence; a newer config isn't proof of resolution.

Retain supplied inputs when evidence conflicts. Other-job/session activity can explain ambiguity but cannot resolve this incident. State the gap and inspect offered local logs.
