import paramiko

DEVICE_IP = ""
USERNAME = "comma"

RUNNER_DIR = "/data/github-runner"
RUNNER_TOKEN = ""
RUNNER_URL = "https://github.com/FrogAi/FrogPilot"
RUNNER_VERSION = "2.316.0"

RUNNER_START_CMD = (
  "tmux has-session -t github-runner 2>/dev/null || "
  "cd /data/github-runner && tmux new-session -d -s github-runner './run.sh'"
)

commands = [
  f"mkdir -p {RUNNER_DIR} && cd {RUNNER_DIR}",
  f"cd {RUNNER_DIR} && curl -L -o runner.tar.gz https://github.com/actions/runner/releases/download/v{RUNNER_VERSION}/actions-runner-linux-arm64-{RUNNER_VERSION}.tar.gz",
  f"cd {RUNNER_DIR} && TMPDIR={RUNNER_DIR} tar --no-same-owner -xzf runner.tar.gz",
  f"cd {RUNNER_DIR} && ./config.sh --unattended --url {RUNNER_URL} --token {RUNNER_TOKEN} --name c3x-runner --labels c3x,arm64,openpilot",
  f"cd {RUNNER_DIR} && {RUNNER_START_CMD}",
  f"cd {RUNNER_DIR} && rm -f runner.tar.gz"
]

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(DEVICE_IP, username=USERNAME)

for cmd in commands:
  print(f"Running: {cmd}")
  stdin, stdout, stderr = client.exec_command(cmd)
  print(stdout.read().decode())
  print(stderr.read().decode())

client.close()
