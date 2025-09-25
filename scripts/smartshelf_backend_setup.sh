#!/usr/bin/env bash
set -euo pipefail

### ========= Config (edit if you like) =========
APP_ROOT="/opt/smartshelf"
REPO_URL="https://github.com/Acash2018/SmartShelf"
BRANCH="Aakash_BackEnd"
SERVICE="smartshelf-backend"
MODULE="app:app"                 # change if your entry is different
PORT="8000"
PY="python3"
### ============================================

REPO_DIR="$APP_ROOT/SmartShelf"
BACKEND_DIR="$REPO_DIR/backend"
VENV_DIR="$BACKEND_DIR/.venv"
SERVICE_FILE="/etc/systemd/system/${SERVICE}.service"
ENV_FILE="$BACKEND_DIR/.env"

msg() { echo -e "\033[1;32m[OK]\033[0m $*"; }
info() { echo -e "\033[1;34m[i]\033[0m $*"; }
warn() { echo -e "\033[1;33m[!]\033[0m $*"; }

require_cmd() { command -v "$1" >/dev/null 2>&1 || { echo "Missing $1"; exit 1; }; }

install_prereqs() {
  info "Installing system prerequisites..."
  sudo apt update
  sudo apt -y install git "${PY}" "${PY}-venv" python3-pip curl
}

ensure_swap() {
  if ! sudo swapon --show | grep -q swapfile; then
    info "Adding 1G swap (helps on micro instances)..."
    sudo fallocate -l 1G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab >/dev/null
  fi
}

clone_or_update_repo() {
  sudo mkdir -p "$APP_ROOT"
  sudo chown -R ubuntu:ubuntu "$APP_ROOT"
  if [ -d "$REPO_DIR/.git" ]; then
    info "Repo exists; fetching updates..."
    git -C "$REPO_DIR" fetch --all --prune
  else
    info "Cloning $REPO_URL ..."
    git clone "$REPO_URL" "$REPO_DIR"
  fi
  info "Checking out branch: $BRANCH"
  git -C "$REPO_DIR" checkout "$BRANCH" || git -C "$REPO_DIR" checkout -b "$BRANCH" "origin/$BRANCH"
}

make_venv_and_install() {
  info "Creating venv and installing requirements..."
  mkdir -p "$BACKEND_DIR"
  if [ ! -d "$VENV_DIR" ]; then
    ${PY} -m venv "$VENV_DIR"
  fi
  # shellcheck disable=SC1090
  source "$VENV_DIR/bin/activate"
  pip install --upgrade pip wheel
  if [ -f "$BACKEND_DIR/requirements.txt" ]; then
    pip install -r "$BACKEND_DIR/requirements.txt" || true
  fi
  # ensure known deps your app used during manual run
  pip install gunicorn python-dotenv sendgrid openai
  deactivate
}

write_env_if_missing() {
  if [ ! -f "$ENV_FILE" ]; then
    info "Creating .env (you can edit later)…"
    cat > "$ENV_FILE" <<EOF
FLASK_ENV=production
SMARTSHELF_DB=$BACKEND_DIR/food_items.db
# SENDGRID_API_KEY=put-key-here
# OPENAI_API_KEY=put-key-here
SECRET_KEY=$(tr -dc A-Za-z0-9 </dev/urandom | head -c 32)
EOF
  fi
}

write_service() {
  info "Writing systemd service: $SERVICE"
  sudo tee "$SERVICE_FILE" >/dev/null <<EOF
[Unit]
Description=SmartShelf Flask API (Gunicorn)
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=$BACKEND_DIR
# App reads $ENV_FILE via python-dotenv; we also pass a couple envs here
Environment=FLASK_ENV=production
Environment=SMARTSHELF_DB=$BACKEND_DIR/food_items.db
ExecStart=$VENV_DIR/bin/gunicorn --workers 2 --bind 127.0.0.1:${PORT} ${MODULE}
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF
  sudo systemctl daemon-reload
  sudo systemctl enable --now "$SERVICE"
}

status_and_smoke() {
  sudo systemctl status "$SERVICE" --no-pager || true
  info "Local curl smoke test:"
  curl -sS -i "http://127.0.0.1:${PORT}/" || true
}

do_update() {
  info "Updating code + deps, then restarting…"
  git -C "$REPO_DIR" fetch --all --prune
  git -C "$REPO_DIR" checkout "$BRANCH"
  git -C "$REPO_DIR" pull --ff-only || true
  # shellcheck disable=SC1090
  source "$VENV_DIR/bin/activate"
  if [ -f "$BACKEND_DIR/requirements.txt" ]; then
    pip install -r "$BACKEND_DIR/requirements.txt" || true
  fi
  deactivate
  sudo systemctl restart "$SERVICE"
  status_and_smoke
}

usage() {
  cat <<USAGE
Usage: $0 [install|update|restart|logs]
  install  - (default) full setup or re-setup: packages, repo, venv, service
  update   - git pull + pip install -r + restart the service
  restart  - restart the systemd service
  logs     - tail last 200 lines of service logs
USAGE
}

case "${1:-install}" in
  install)
    install_prereqs
    ensure_swap
    clone_or_update_repo
    make_venv_and_install
    write_env_if_missing
    write_service
    status_and_smoke
    msg "Done. Service '${SERVICE}' should be running on 127.0.0.1:${PORT}"
    ;;
  update)
    do_update
    ;;
  restart)
    sudo systemctl restart "$SERVICE"
    status_and_smoke
    ;;
  logs)
    sudo journalctl -u "$SERVICE" -n 200 --no-pager
    ;;
  *)
    usage
    exit 1
    ;;
esac

