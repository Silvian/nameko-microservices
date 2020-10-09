.PHONY: shell

run-orders:
	nameko run orders.services --broker amqp://guest:guest@localhost

run-alerts:
	nameko run alerts.services --broker amqp://guest:guest@localhost

shell:
	nameko shell --broker amqp://guest:guest@localhost