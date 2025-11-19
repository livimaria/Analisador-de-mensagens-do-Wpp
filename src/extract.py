import json
import pandas as pd
import re


# ============================================================
# EXTRACT JSON
# ============================================================
def extract_json(file):
    data = json.load(file)
    rows = []

    for item in data:
        messages = item.get("messages", [])

        attendance_id = item.get("attendanceId", "")
        protocolo = item.get("protocol", "")
        contato = item.get("contact", {})
        nome = contato.get("name", "Desconhecido")
        numero = contato.get("number", "")

        for msg in messages:
            dh = msg.get("dhMessage", "")

            rows.append({
                "id": attendance_id,
                "data": dh[:10] if len(dh) >= 10 else "",
                "hora": dh[11:] if len(dh) >= 11 else "",
                "remetente": msg.get("senderName", "Desconhecido"),
                "mensagem": msg.get("text", ""),
                "numero": numero,
                "nome": nome
            })

    return pd.DataFrame(rows)


# ============================================================
# EXTRACT CSV — NORMALIZA PARA O MESMO PADRÃO DO JSON
# ============================================================
def extract_csv(file):
    df = pd.read_csv(file, low_memory=False)

    # Criar ID se não existir
    if "id" not in df.columns:
        df["id"] = df.index.astype(str)

    # DETECTA coluna de mensagens
    candidate_cols = [c for c in df.columns if "message" in c.lower() or "text" in c.lower()]
    if not candidate_cols:
        raise ValueError("Nenhuma coluna de mensagem encontrada no CSV.")
    text_col = candidate_cols[0]

    # DETECTA coluna de data/hora
    date_cols = [c for c in df.columns if "date" in c.lower() or "dh" in c.lower()]
    date_col = date_cols[0] if date_cols else None

    # NOVO: Normalizar para o mesmo formato do JSON
    data = pd.DataFrame()
    data["id"] = df["id"]
    data["mensagem"] = df[text_col].astype(str)

    # Remetente -> se existir
    remetente_cols = [c for c in df.columns if "sender" in c.lower() or "from" in c.lower()]
    if remetente_cols:
        data["remetente"] = df[remetente_cols[0]].astype(str)
    else:
        data["remetente"] = "Desconhecido"

    if date_col:
        # separa data e hora se vier junto
        dh_series = pd.to_datetime(df[date_col], errors="coerce")

        data["data"] = dh_series.dt.date.astype(str)
        data["hora"] = dh_series.dt.time.astype(str)
    else:
        data["data"] = ""
        data["hora"] = ""

    # adicionar campos extras opcionais
    data["nome"] = df.columns[df.columns.str.contains("name", case=False)].tolist()[0] \
        if any("name" in c.lower() for c in df.columns) else "Desconhecido"

    data["numero"] = df.columns[df.columns.str.contains("number", case=False)].tolist()[0] \
        if any("number" in c.lower() for c in df.columns) else ""

    return data
