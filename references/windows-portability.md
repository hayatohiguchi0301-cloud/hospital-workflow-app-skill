# Windows PC portability and hospital LAN sharing

Use these rules to make a generated app movable to another Windows PC and, when requested, usable from other PCs on the same trusted hospital LAN.

## Choose the deployment mode

- **Move to another PC:** copy the project and its data to a new host, rebuild `.venv` there, and run one local app instance.
- **Share from one host PC:** run one Streamlit process on a designated host. Other PCs use only a browser. Keep the host awake and the launcher window open.
- Do not put an SQLite database on a network share and start the app independently from multiple PCs. SQLite remains owned by the one host process.

State the selected mode in `README.md`. LAN sharing is not internet publishing and must not be represented as strong authentication or access control.

## Portable project invariants

- Resolve the database, uploads, exports, and configuration from `Path(__file__).resolve().parent` or another project-relative base. Never embed a developer PC path.
- Keep durable data in a clearly named directory such as `data/`. Exclude `.venv`, caches, local databases, exports, and secrets from Git, while documenting which data files must be copied for migration.
- Use compatible dependency ranges in `requirements.txt`. Do not copy `.venv` between PCs as the runtime; recreate it on the destination PC.
- Before copying or restoring SQLite data, stop the app. If WAL mode is used, use SQLite's backup API or make sure the database is cleanly closed and copy the database together with any required `-wal`/`-shm` files. Prefer a documented in-app or scripted backup for important data.
- Keep machine-specific values such as host name, IP address, port, shared folder, and hospital name outside application logic. Treat a `.url` shortcut as deployment-specific; generate or edit it only after the destination host is known.

## Windows launcher

Adapt `assets/windows-launcher/起動.bat` and keep these behaviors:

- Start with `cd /d "%~dp0"` so double-clicking works regardless of the current directory.
- Prefer the Windows `py -3` launcher and fall back to `python`.
- Create `.venv` on first run. If its Python executable exists but cannot run after a PC copy, clearly explain that it is being recreated.
- Install from `requirements.txt` using the virtual environment's Python and stop with an actionable message on failure.
- Start Streamlit through `python -m streamlit`, not an assumed global executable.
- Keep the console open on errors so a non-engineer can report what happened.

Package installation normally needs access to the configured Python package source. If the hospital PC is offline or outbound access is restricted, do not imply that the launcher solves this; provide an approved offline wheelhouse or involve hospital IT.

## Hospital LAN mode

Only enable LAN mode when requested or clearly required:

```text
python -m streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

- Show both `http://localhost:<port>` and `http://<host-ip-or-name>:<port>` in the instructions.
- Prefer a stable, IT-managed host name or reserved address for shortcuts. A hard-coded address copied from the development PC is not portable.
- Document that Windows Firewall may ask to allow Python/Streamlit on the private or domain network. Do not tell users to disable the firewall. If hospital policy blocks the port, direct them to hospital IT.
- Verify the host locally first, then from a second PC on the intended network when available. Guest Wi-Fi, VPN segmentation, VLAN rules, proxy settings, or endpoint controls may prevent peer access.
- Do not expose the Streamlit port directly to the public internet. For sensitive or multi-department use, require an institution-approved reverse proxy, TLS, identity provider, authorization design, audit logging, and data-retention review.

## README acceptance checklist

Document all of the following in Japanese:

- supported Windows and Python versions;
- double-click startup, manual startup, and clean shutdown;
- first-run dependency installation and its network requirement;
- exact durable data location and backup/restore procedure;
- migration steps, explicitly excluding `.venv`;
- local-only or LAN-host mode, including host/client responsibilities;
- URL format, port, firewall/network troubleshooting, and escalation to hospital IT;
- confirmation that no patient data, credentials, or production database belongs in GitHub.

## Verification

In addition to ordinary tests:

1. Check the launcher from a path containing spaces and Japanese characters when possible.
2. Confirm a missing `.venv` is created and a copied/broken `.venv` is recovered.
3. Confirm data paths stay inside the project regardless of the shell's current directory.
4. For LAN mode, confirm `localhost` health first and record whether a second-PC connection was actually tested.
5. Stop and restart the app and confirm existing records remain.
