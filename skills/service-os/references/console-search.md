# Console search and identity

## Authorized sources

- Firebase: https://console.firebase.google.com/project/acko-service-os-prod-53a46/overview
- Android Crashlytics: https://console.firebase.google.com/project/acko-service-os-prod-53a46/crashlytics/app/android:acko.serviceos.android/issues
- Mobile Coralogix: https://acko-mobile.app.coralogix.in/
- Supplied mobile entry point: https://acko-mobile.app.coralogix.in/query-new/archive-logs?id=SXiBNhpoySNHj4FnNFabi&page=0

The saved entry point is navigation, not incident evidence. Verify its applied filters/time range. Other apps exist in this tenant: constrain findings to `serviceos-prod`. Do not access backend `acko-prod` Coralogix.

## Firebase

Read “Latest release” including build in ServiceOS Android Crashlytics. If absent, report unavailable rather than treating the largest version in a limited error table as authoritative. Read the published Remote Config `app_update_check` default and relevant conditions separately; capture version, update type, scope, publication date. Remote Config's configuration revision is not the app version. Do not edit/publish anything.

Use “Search by user ID” with the FE ID and incident-covering dates. Include nonfatal events and crashes. Capture event time separately from upload/receipt time and timestamps embedded in “previous crash” reports. Inspect selected-event identity, device, version/build, stack, keys, breadcrumbs. Aggregated issue counts do not describe this FE/job alone. For latest-release checks, compare a specific signature/variant using version/build and dates; report insufficient population/coverage rather than inferring a fix.

## Coralogix candidate fields

Observed in expanded pilot events on 2026-10-19; verify against a full event before use because schema/indexing/layout can change.

| Field | Purpose |
|---|---|
| `cx_rum.version_metadata.app_name` | `serviceos-prod` |
| `cx_rum.version_metadata.app_version` | Event app version |
| `cx_rum.session_context.user_id` | FE context, sometimes blank |
| `cx_rum.session_context.session_id` | Session correlation |
| `cx_rum.device_context.device` | Model, not unique phone identity |
| `cx_rum.timestamp` | Observed epoch milliseconds |
| `cx_rum.log_context.message` | Often generic event title |
| `cx_rum.log_context.data` | Payload, sometimes stringified nested data |

Example Lucene queries, adapting to verified current schema:

```text
cx_rum.version_metadata.app_name:"serviceos-prod" AND "434834"
cx_rum.version_metadata.app_name:"serviceos-prod" AND cx_rum.session_context.user_id:"1289"
cx_rum.session_context.session_id:"SESSION_ID_FROM_EVENT"
```

IDs above illustrate format, not a known resolved case. Numeric searches can match timestamp fractions: verify semantic references such as `taskId: 434834`, `/task/434834`, or `Start task 434834` in the event. Do not attribute unrelated hits to the job. Plain quoted words may not match substrings of larger tokens; verify search behavior before relying on broad exclusions or declaring no matches.

Set and verify the actual time picker. A verified numeric timestamp range can further constrain searches. Convert IST explicitly: 08:54 IST = 03:24 UTC. For a full local day, use IST midnight boundaries, not UTC midnight. Corroborate displayed, local-message, and UTC fields before normalizing. Treat malformed/unknown timestamps as uncertain.

Inspect complete records when the grid truncates payloads. Read counts, pagination, sampling, storage-tier/retention indicators. If capped, narrow time/session/signature and report remaining gaps. Check later successes before labeling a retryable failure unresolved. Preserve direct query/event links and describe their scope.

## Browser pilot reliability

Use the browser tools supported for the executing user. Their own account needs project/tenant access; the author's sessions are not shared. Never invent API/MCP availability, endpoints, field names, saved-query IDs, or successful checks.

After navigation/query execution verify the active view, displayed query, applied dates, completed state, and consistent counts/results. Stale rows may persist briefly. Don't read cached rows from an inactive Explore view. Links may create new views and the UI may switch between legacy/new Explore: rediscover controls. If a tiny panel prevents interaction, use supported controls to make the layout usable and restore temporary overrides afterward.
