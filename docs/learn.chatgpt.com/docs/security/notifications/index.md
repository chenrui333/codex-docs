---
source_type: 'learn'
source_area: 'learn_security'
source_url: 'https://learn.chatgpt.com/docs/security/notifications'
source_kind: 'learn_markdown'
---

# Daybreak notifications

Source: https://learn.chatgpt.com/docs/security/notifications

> For the complete documentation index, see [llms.txt](https://learn.chatgpt.com/llms.txt). Markdown versions of documentation pages are available by appending `.md` to the page URL.

You can send scan events to a service you control using a workspace webhook. For
example, you can use it to update a security dashboard when a scan finishes or
refresh a ticket when the scan results change. Each destination receives the
events you select from across your ChatGPT workspace.

## Add a workspace webhook

1. In Daybreak, go to **Settings** > **Notifications** and select **Add**.
2. Enter a **Name** and an **Endpoint URL**. Use a publicly reachable HTTPS
   endpoint that accepts `POST` requests on port 443.
3. Choose which events to receive.
   - **Scan finished** (`scan.finished`) reports scan completions, failures, and cancellations.
   - **Scan updated** (`scan.updated`) reports later changes to a scan’s results, such as updated validation or severity.

> Illustration: Add notification form for a security dashboard webhook with Scan finished and Scan updated selected.

4. Select **Add**. Copy the signing secret and store it securely. Daybreak
   shows the full secret once.
5. In the destination’s menu, select **Send test notification**, then **Send
   test**. Daybreak sends a sample `scan.finished` event with `is_test: true`
   and reports delivery when your endpoint returns a `2xx` response.

## Verify and handle deliveries

Daybreak sends a JSON `POST` signed with HMAC-SHA256. The signature covers the
`webhook-id`, `webhook-timestamp`, and original request body. Verify the request using the
`webhook-signature` header before processing the event.
Pass the original request bytes to your verifier so changes to whitespace or
JSON formatting don’t invalidate the signature. For details, see the [Standard Webhooks specification](https://github.com/standard-webhooks/standard-webhooks/blob/main/spec/standard-webhooks.md#verifying-signatures).
For language-specific verification libraries, see the [Standard Webhooks reference implementations](https://github.com/standard-webhooks/standard-webhooks#reference-implementations).

Check `is_test` before triggering your production workflow. You can identify
repeat deliveries by the payload’s `id` and group events for the same scan by
`data.scan_id`. Daybreak allows
10 seconds per delivery attempt, including test deliveries. Return a `2xx`
response within that window once your service has accepted the event. For
longer processing, save the event to a queue and respond before processing it.

## Manage destinations and rotate secrets

Select **Edit** in the destination’s menu. You can change the URL, choose
different events, or turn off **Enabled** to pause deliveries. Select
**Rotate secret** to replace the signing secret. Copy the replacement and update your receiver. Select
**Keep the current secret active for 24 hours** when rotating if your receiver
needs time to switch. Daybreak signs with both secrets during that window, so
either secret can verify the delivery. With immediate rotation, update the
receiver before sending a new test.
