## Feature flags

Use the `[features]` table in `config.toml` to toggle optional capabilities.

### Common feature flags

| Key | Default | Maturity | Description |
| --- | --- | --- | --- |
| `apps` | true | Stable | Enable apps |
| `memories` | false | Experimental | Enable memories |

This table lists common user-facing flags.

### Enabling features

Add a feature key under `[features]`.
