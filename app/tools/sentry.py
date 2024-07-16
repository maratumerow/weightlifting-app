import sentry_sdk


def sentry_init() -> None:
    sentry_sdk.init(
        dsn="https://6b267d4948c52d64832640acb7b89ed4@o4507611205795840.ingest.de.sentry.io/4507611208220752",
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
    )
