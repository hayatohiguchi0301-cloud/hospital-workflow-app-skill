from __future__ import annotations

import csv
import io
from datetime import date

import streamlit as st

import db

STATUSES = ["未着手", "対応中", "確認待ち", "完了"]
st.set_page_config(page_title="業務管理", page_icon="🏥", layout="wide")
db.initialize()
st.title("業務管理")
st.caption("対応状況と期限を、チームで分かりやすく共有します。")

with st.expander("新しい業務を登録", expanded=False):
    with st.form("create_task", clear_on_submit=True):
        title = st.text_input("件名（必須）")
        owner = st.text_input("担当者")
        use_due = st.checkbox("期限を設定する", value=True)
        due = st.date_input("期限", value=date.today(), disabled=not use_due)
        status = st.selectbox("ステータス", STATUSES)
        note = st.text_area("備考")
        if st.form_submit_button("登録する", type="primary", use_container_width=True):
            try:
                db.create_task(title, owner, due.isoformat() if use_due else None, status, note)
                st.success("登録しました。")
                st.rerun()
            except ValueError as exc:
                st.error(str(exc))

col1, col2 = st.columns([2, 1])
query = col1.text_input("検索", placeholder="件名・担当者・備考")
status_filter = col2.selectbox("ステータスで絞り込み", ["すべて"] + STATUSES)
rows = db.list_tasks(query, "" if status_filter == "すべて" else status_filter)
st.subheader(f"業務一覧（{len(rows)}件）")

if not rows:
    st.info("該当する業務はありません。「新しい業務を登録」から追加できます。")
else:
    for row in rows:
        due_label = row["due_date"] or "期限なし"
        with st.expander(f'{row["title"]}｜{row["status"]}｜{due_label}'):
            with st.form(f'edit_{row["id"]}'):
                edit_title = st.text_input("件名（必須）", row["title"])
                edit_owner = st.text_input("担当者", row["owner"])
                edit_due = st.text_input("期限（YYYY-MM-DD、空欄可）", row["due_date"] or "")
                edit_status = st.selectbox("ステータス", STATUSES, index=STATUSES.index(row["status"]))
                edit_note = st.text_area("備考", row["note"])
                if st.form_submit_button("変更を保存", type="primary"):
                    try:
                        db.update_task(row["id"], edit_title, edit_owner, edit_due or None, edit_status, edit_note)
                        st.success("変更を保存しました。")
                        st.rerun()
                    except ValueError as exc:
                        st.error(str(exc))
            confirm = st.checkbox("削除する対象を確認しました", key=f'confirm_{row["id"]}')
            if st.button("この業務を削除", key=f'delete_{row["id"]}', disabled=not confirm):
                db.delete_task(row["id"])
                st.success("削除しました。")
                st.rerun()

buffer = io.StringIO()
writer = csv.writer(buffer)
writer.writerow(["ID", "件名", "担当者", "期限", "ステータス", "備考", "登録日時", "更新日時"])
for row in rows:
    writer.writerow([row[key] for key in row.keys()])
st.download_button("表示中の一覧をCSV保存", buffer.getvalue().encode("utf-8-sig"), "業務一覧.csv", "text/csv")

