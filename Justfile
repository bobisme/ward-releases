dev:
  miniserve --index index.html --port 8081

deploy:
  wrangler pages deploy . --project-name=wardsecurity-io
