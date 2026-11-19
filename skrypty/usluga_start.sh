#!/bin/sh
# Start usługi dla aplikacji na ksefbot.pl (OMEN, karta, port 8770). Z ThinkPada/kontenera, w tle:
#   nohup setsid sh skrypty/usluga_start.sh > /tmp/usluga.log 2>&1 &
# OMEN_HOST = adres OMENa w sieci lokalnej (nie w repo). Kończy się sama po BEZCZYNNOSC minutach bez żądań (domyślnie 90).
cd "$(dirname "$0")/.." && ORKIESTRATOR_SSH_OMEN="-i /data/.ssh/omen_hackathon hackathon@${OMEN_HOST:?ustaw OMEN_HOST}" \
  node /data/orkiestrator-klient/klient/orkiestrator.mjs uruchom --maszyna omen --klasa gpu-tlo --sesja Programista \
  --repo hacknation --konto hackathon --bez-zapasowej --ssh --wyslij . -- \
  sh -c "touch . && . ~/venv/bin/activate && python -m rtg.usluga --port 8770 --bezczynnosc ${BEZCZYNNOSC:-90}"
