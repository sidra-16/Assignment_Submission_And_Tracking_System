import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time
from db import get_db, get_collection
from styles import CSS

st.set_page_config(page_title="SASTS — Assignment Tracker", page_icon="🎓", layout="wide", initial_sidebar_state="collapsed")
st.markdown(CSS, unsafe_allow_html=True)

# ── Top Banner ──
try:
    db_status = "🟢 Connected" if get_db().command("ping") else "🔴 Disconnected"
except:
    db_status = "🔴 Disconnected"

st.markdown(f'''
<div class="top-banner">
    <h2>🎓 SASTS — Student Assignment Tracker</h2>
    <div class="mongo-badge">MongoDB {db_status}</div>
</div>
''', unsafe_allow_html=True)

# ── Top Navigation (selectbox) ──
PAGE_OPTIONS = [
    "📊 Dashboard", "👨‍🎓 Students", "👨‍🏫 Instructors", "📚 Courses",
    "📝 Assignments", "📤 Submissions", "🏢 Departments", "🔔 Notifications",
    "📈 Aggregations", "🔄 Transactions", "🔒 Locking Demo", "👁 Views", "⚡ Indexing"
]
page = st.selectbox("Navigation", PAGE_OPTIONS, label_visibility="collapsed")

st.markdown("---")

COLLECTIONS = {
    "students": {"fields": ["_id","name","email","department_id","semester_id","courses"], "icon": "👨‍🎓"},
    "instructors": {"fields": ["_id","name","email","department_id"], "icon": "👨‍🏫"},
    "courses": {"fields": ["_id","course_name","instructor_id"], "icon": "📚"},
    "assignments": {"fields": ["_id","title","course_id","deadline"], "icon": "📝"},
    "submissions": {"fields": ["_id","student_id","assignment_id","submission_date","file","grade","feedback"], "icon": "📤"},
    "departments": {"fields": ["_id","department_name"], "icon": "🏢"},
    "notifications": {"fields": ["_id","message","date","student_id"], "icon": "🔔"},
}

# ── Generic CRUD ──
def crud_page(name, info):
    col = get_collection(name)
    st.subheader(f"{info['icon']} {name.title()} Collection")

    # Show success/error messages from previous action
    if st.session_state.get(f"msg_{name}"):
        mtype, mtxt = st.session_state[f"msg_{name}"]
        if mtype == "success":
            st.success(mtxt)
        else:
            st.error(mtxt)
        del st.session_state[f"msg_{name}"]

    tab1, tab2, tab3 = st.tabs(["📋 Browse & Delete", "➕ Insert New", "✏️ Update"])

    with tab1:
        total_count = col.count_documents({})
        docs = list(col.find())
        if docs:
            flat = []
            for d in docs:
                row = {}
                for k, v in d.items():
                    row[k] = str(v) if isinstance(v, (dict, list)) else v
                flat.append(row)
            df = pd.DataFrame(flat)
            st.dataframe(df, use_container_width=True, height=400)
            st.caption(f"Total documents: {total_count}")
            with st.expander("🗑 Delete a document"):
                del_id = st.number_input(f"Enter _id to delete", min_value=0, key=f"del_{name}")
                if st.button("Delete", key=f"delbtn_{name}", type="primary"):
                    r = col.delete_one({"_id": del_id})
                    if r.deleted_count:
                        st.session_state[f"msg_{name}"] = ("success", f"✅ Deleted document _id={del_id} successfully!")
                    else:
                        st.session_state[f"msg_{name}"] = ("error", "❌ Document not found")
                    st.rerun()
        else:
            st.info("No documents found. Add some!")

    with tab2:
        st.markdown("##### Fill in the fields below and click Save")
        with st.form(f"add_{name}", clear_on_submit=True):
            vals = {}
            simple_fields = [f for f in info["fields"] if f != "_id"]
            for f in simple_fields:
                if f in ["department_id","semester_id","instructor_id","course_id","student_id","assignment_id"]:
                    vals[f] = st.number_input(f, min_value=0, key=f"add_{name}_{f}")
                elif f == "courses":
                    vals[f] = st.text_input("courses (comma-separated IDs)", "0,1", key=f"add_{name}_{f}")
                elif f == "file":
                    vals[f] = {"file_name": st.text_input("file_name", "file.pdf", key=f"add_{name}_fn"), "file_path": st.text_input("file_path", "/uploads/file.pdf", key=f"add_{name}_fp")}
                elif f == "grade":
                    vals[f] = {"marks": st.number_input("marks", 0, 100, 75, key=f"add_{name}_marks")}
                elif f == "feedback":
                    vals[f] = {"comments": st.selectbox("feedback", ["Good","Average","Excellent","Needs Improvement"], key=f"add_{name}_fb")}
                elif f == "deadline" or f == "submission_date" or f == "date":
                    vals[f] = st.text_input(f, value="2026-05-15", key=f"add_{name}_{f}")
                else:
                    vals[f] = st.text_input(f, key=f"add_{name}_{f}")
            submitted = st.form_submit_button("💾 Save", type="primary")
            if submitted:
                # Parse courses field from string to list
                if "courses" in vals and isinstance(vals["courses"], str):
                    vals["courses"] = [int(x.strip()) for x in vals["courses"].split(",") if x.strip().isdigit()]
                max_doc = col.find_one(sort=[("_id", -1)])
                vals["_id"] = (max_doc["_id"] + 1) if max_doc else 0
                try:
                    col.insert_one(vals)
                    st.session_state[f"msg_{name}"] = ("success", f"✅ Added document with _id={vals['_id']} successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")

    with tab3:
        ec1, ec2 = st.columns([3, 1])
        with ec1:
            edit_id = st.number_input("Enter _id to edit", min_value=0, key=f"edit_{name}")
        with ec2:
            st.markdown("<br>", unsafe_allow_html=True)
            load_clicked = st.button("🔍 Load", key=f"loadbtn_{name}", type="primary")
        if load_clicked:
            found = col.find_one({"_id": edit_id})
            if found:
                st.session_state[f"edit_doc_{name}"] = found
                st.session_state[f"edit_id_{name}"] = edit_id
            else:
                st.error(f"❌ No document found with _id={edit_id}")
                if f"edit_doc_{name}" in st.session_state:
                    del st.session_state[f"edit_doc_{name}"]
        doc = st.session_state.get(f"edit_doc_{name}")
        if doc:
            st.info(f"Editing document _id={doc['_id']}")
            with st.form(f"editform_{name}"):
                updates = {}
                for f in [x for x in info["fields"] if x != "_id"]:
                    if f in ["department_id","semester_id","instructor_id","course_id","student_id","assignment_id"]:
                        updates[f] = st.number_input(f, value=int(doc.get(f,0)), key=f"ef_{name}_{f}")
                    elif f == "courses":
                        updates[f] = st.text_input(f, value=",".join(str(c) for c in doc.get(f,[])), key=f"ef_{name}_{f}")
                    elif f in ["file","grade","feedback"]:
                        st.markdown(f"**{f}:**")
                        st.json(doc.get(f, {}))
                    else:
                        updates[f] = st.text_input(f, value=str(doc.get(f,"")), key=f"ef_{name}_{f}")
                if st.form_submit_button("💾 Save Changes", type="primary"):
                    # Parse courses from string to list
                    if "courses" in updates and isinstance(updates["courses"], str):
                        updates["courses"] = [int(x.strip()) for x in updates["courses"].split(",") if x.strip().isdigit()]
                    eid = st.session_state.get(f"edit_id_{name}", doc["_id"])
                    col.update_one({"_id": eid}, {"$set": updates})
                    st.session_state[f"msg_{name}"] = ("success", f"✅ Updated document _id={eid} successfully!")
                    del st.session_state[f"edit_doc_{name}"]
                    st.rerun()

# ── Dashboard ──
def dashboard():
    st.subheader("📊 System Overview")
    names = ["students","instructors","courses","assignments","submissions","departments","notifications"]
    cols = st.columns(7)
    for i, n in enumerate(names):
        cnt = get_collection(n).count_documents({})
        with cols[i]:
            st.markdown(f'<div class="stat-card"><div class="stat-number">{cnt}</div><div class="stat-label">{n.upper()}</div></div>', unsafe_allow_html=True)
    st.markdown("")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📊 Feedback Distribution")
        subs = list(get_collection("submissions").find({}, {"feedback.comments":1, "_id":0}))
        if subs:
            fb = [s.get("feedback",{}).get("comments","N/A") for s in subs]
            df = pd.DataFrame(fb, columns=["Feedback"]).value_counts().reset_index()
            df.columns = ["Feedback","Count"]
            st.bar_chart(df.set_index("Feedback"))
    with c2:
        st.subheader("🏢 Students per Department")
        studs = list(get_collection("students").find({}, {"department_id":1, "_id":0}))
        if studs:
            df = pd.DataFrame(studs)
            dc = df["department_id"].value_counts().sort_index().reset_index()
            dc.columns = ["Department","Count"]
            st.bar_chart(dc.set_index("Department"))

# ── Aggregations ──
def aggregations_page():
    st.subheader("📈 Aggregation Pipelines")
    left, right = st.columns([1, 2])
    with left:
        choice = st.radio("Select Pipeline", [
            "Avg Marks / Assignment", "Top 5 Students", "Submissions / Student",
            "Late Submissions", "Submissions / Course"
        ])
        run = st.button("▶ Run Pipeline", type="primary")
    with right:
        col = get_collection("submissions")
        if not run:
            st.info("👉 Select a pipeline and click **Run Pipeline** to see results.")
        else:
            if choice == "Avg Marks / Assignment":
                st.code('db.submissions.aggregate([{$group:{_id:"$assignment_id",avg:{$avg:"$grade.marks"}}}])', language="javascript")
                r = list(col.aggregate([{"$group":{"_id":"$assignment_id","avg":{"$avg":"$grade.marks"}}}]))
                df = pd.DataFrame(r).rename(columns={"_id":"Assignment","avg":"Avg Marks"}).sort_values("Assignment").head(30)
                st.dataframe(df, use_container_width=True)
                st.bar_chart(df.set_index("Assignment"))
            elif choice == "Top 5 Students":
                st.code('db.submissions.aggregate([{$group:{_id:"$student_id",total:{$sum:"$grade.marks"}}},{$sort:{total:-1}},{$limit:5}])', language="javascript")
                r = list(col.aggregate([{"$group":{"_id":"$student_id","total":{"$sum":"$grade.marks"}}},{"$sort":{"total":-1}},{"$limit":5}]))
                df = pd.DataFrame(r).rename(columns={"_id":"Student","total":"Total Marks"})
                st.dataframe(df, use_container_width=True)
                st.bar_chart(df.set_index("Student"))
            elif choice == "Submissions / Student":
                st.code('db.submissions.aggregate([{$group:{_id:"$student_id",count:{$sum:1}}}])', language="javascript")
                r = list(col.aggregate([{"$group":{"_id":"$student_id","count":{"$sum":1}}}]))
                df = pd.DataFrame(r).rename(columns={"_id":"Student","count":"Submissions"}).sort_values("Submissions", ascending=False).head(20)
                st.dataframe(df, use_container_width=True)
                st.bar_chart(df.set_index("Student"))
            elif choice == "Late Submissions":
                st.code('db.submissions.aggregate([{$lookup:{from:"assignments",...}},{$unwind},{$match:{$expr:{$gt:["$submission_date","$assignment.deadline"]}}}])', language="javascript")
                r = list(col.aggregate([{"$lookup":{"from":"assignments","localField":"assignment_id","foreignField":"_id","as":"a"}},{"$unwind":"$a"},{"$match":{"$expr":{"$gt":["$submission_date","$a.deadline"]}}},{"$project":{"student_id":1,"assignment_id":1,"submission_date":1,"deadline":"$a.deadline"}},{"$limit":30}]))
                if r:
                    st.dataframe(pd.DataFrame(r), use_container_width=True)
                else:
                    st.info("No late submissions found")
            elif choice == "Submissions / Course":
                st.code('db.submissions.aggregate([{$lookup:{from:"assignments",...}},{$unwind},{$group:{_id:"$a.course_id",count:{$sum:1}}}])', language="javascript")
                r = list(col.aggregate([{"$lookup":{"from":"assignments","localField":"assignment_id","foreignField":"_id","as":"a"}},{"$unwind":"$a"},{"$group":{"_id":"$a.course_id","count":{"$sum":1}}}]))
                df = pd.DataFrame(r).rename(columns={"_id":"Course","count":"Submissions"}).sort_values("Course").head(30)
                st.dataframe(df, use_container_width=True)
                st.bar_chart(df.set_index("Course"))

# ── Transactions ──
def transactions_page():
    st.subheader("🔄 ACID Transactions")
    c1,c2,c3,c4 = st.columns(4)
    for col_w, letter, title, desc in [(c1,"A","Atomicity","All or nothing"), (c2,"C","Consistency","Valid state transitions"), (c3,"I","Isolation","No interference"), (c4,"D","Durability","Persists after failure")]:
        with col_w:
            st.markdown(f'<div class="acid-card"><div class="acid-letter">{letter}</div><br><strong>{title}</strong><br><small>{desc}</small></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("#### ► Submit Assignment Transaction")
    tc1, tc2 = st.columns(2)
    with tc1:
        sid = st.number_input("Student ID", 0, 999, 5)
        aid = st.number_input("Assignment ID", 0, 399, 10)
        marks = st.number_input("Marks", 0, 100, 85)
        force_fail = st.checkbox("⚠ Force failure (simulate rollback)")
        run = st.button("▶ Execute Transaction", type="primary")
    with tc2:
        if run:
            steps = []
            try:
                steps.append(("Step 1: Verify student exists", "pending"))
                student = get_collection("students").find_one({"_id": sid})
                if not student:
                    steps[-1] = ("Step 1: Verify student exists", "fail")
                    raise Exception("Student not found")
                steps[-1] = (f"Step 1: Student '{student['name']}' found ✅", "pass")

                steps.append(("Step 2: Verify assignment exists", "pending"))
                assign = get_collection("assignments").find_one({"_id": aid})
                if not assign:
                    steps[-1] = ("Step 2: Verify assignment exists", "fail")
                    raise Exception("Assignment not found")
                steps[-1] = (f"Step 2: Assignment '{assign['title']}' found ✅", "pass")

                steps.append(("Step 3: Insert submission", "pending"))
                if force_fail:
                    steps[-1] = ("Step 3: ⚠ FORCED FAILURE", "fail")
                    raise Exception("Forced failure for rollback demo")
                max_sub = get_collection("submissions").find_one(sort=[("_id",-1)])
                new_id = (max_sub["_id"]+1) if max_sub else 0
                get_collection("submissions").insert_one({"_id":new_id,"student_id":sid,"assignment_id":aid,"submission_date":datetime.now().strftime("%Y-%m-%d"),"file":{"file_name":f"file_{new_id}.pdf","file_path":f"/uploads/file_{new_id}.pdf"},"grade":{"marks":marks},"feedback":{"comments":"Pending Review"}})
                steps[-1] = (f"Step 3: Submission #{new_id} inserted ✅", "pass")

                steps.append(("Step 4: Transaction COMMITTED ✅", "pass"))
                for msg, status in steps:
                    if status == "pass":
                        st.success(msg)
                    elif status == "fail":
                        st.error(msg)
            except Exception as e:
                for msg, status in steps:
                    if status == "pass": st.success(msg)
                    elif status == "fail": st.error(msg)
                st.warning(f"🔄 ROLLBACK: {e}")

# ── Locking ──
def locking_page():
    st.subheader("🔒 Concurrency Control & Locking")
    tab1, tab2 = st.tabs(["🔓 Optimistic Locking", "🔒 Pessimistic Locking"])
    with tab1:
        st.markdown('<div class="info-box">💡Each document has a <code>version</code> field. Update only succeeds if version matches.</div>', unsafe_allow_html=True)
        sub_id = st.number_input("Submission ID", 0, 1999, 0, key="opt_id")
        new_marks = st.number_input("New Marks", 0, 100, 95, key="opt_marks")
        conflict = st.checkbox("Simulate version conflict")
        if st.button("🔄 Update with Optimistic Lock", type="primary"):
            col = get_collection("submissions")
            doc = col.find_one({"_id": sub_id})
            if not doc:
                st.error("Document not found")
            else:
                # Initialize version field if it doesn't exist
                if "version" not in doc:
                    col.update_one({"_id": sub_id}, {"$set": {"version": 1}})
                    doc["version"] = 1
                ver = doc.get("version", 1)
                st.info(f"📋 Current version: **{ver}** | Current marks: **{doc.get('grade',{}).get('marks','N/A')}**")
                if conflict:
                    col.update_one({"_id":sub_id}, {"$set":{"version": ver+1}})
                    st.warning("⚠ Another writer updated the document! Version bumped to " + str(ver+1))
                result = col.update_one({"_id":sub_id, "version":ver}, {"$set":{"grade.marks":new_marks, "version":ver+1}})
                if result.matched_count == 1:
                    st.success(f"✅ Update succeeded! Marks → {new_marks}, Version → {ver+1}")
                else:
                    st.error("❌ VERSION CONFLICT! Update rejected. The document was modified by another process. Retry needed.")

    with tab2:
        st.markdown('<div class="info-box">💡A <code>locks</code> collection stores active locks. Before updating, admin must acquire a lock.</div>', unsafe_allow_html=True)
        res_id = st.number_input("Resource ID", 0, 1999, 0, key="pess_id")
        locked_by = st.text_input("Locked By", "Admin_1", key="pess_by")
        lc1, lc2 = st.columns(2)
        locks_col = get_collection("locks")
        with lc1:
            if st.button("🔒 Acquire Lock", type="primary"):
                existing = locks_col.find_one({"resource_id": res_id, "expires_at": {"$gt": datetime.now().isoformat()}})
                if existing:
                    st.markdown(f'<div class="error-toast">❌ LOCK DENIED — held by {existing["locked_by"]}</div>', unsafe_allow_html=True)
                else:
                    locks_col.insert_one({"resource_id":res_id, "locked_by":locked_by, "locked_at":datetime.now().isoformat(), "expires_at":(datetime.now()+timedelta(seconds=30)).isoformat()})
                    st.markdown(f'<div class="success-toast">✅ Lock acquired by {locked_by} (30s expiry)</div>', unsafe_allow_html=True)
        with lc2:
            if st.button("🔓 Release Lock", type="secondary"):
                r = locks_col.delete_one({"resource_id": res_id, "locked_by": locked_by})
                if r.deleted_count:
                    st.markdown('<div class="success-toast">✅ Lock released</div>', unsafe_allow_html=True)
                else:
                    st.error("No lock found for this resource/admin")
        active = list(locks_col.find())
        if active:
            st.markdown("#### Active Locks")
            for lk in active:
                st.markdown(f'<div class="lock-card">🔒 Resource {lk["resource_id"]} — Locked by <b>{lk["locked_by"]}</b> — Expires: {lk.get("expires_at","N/A")}</div>', unsafe_allow_html=True)

# ── Views ──
def views_page():
    st.subheader("👁 MongoDB Views")
    st.markdown('<div class="info-box">💡A MongoDB View is a read-only virtual collection defined by an aggregation pipeline. Views compute results on-the-fly.</div>', unsafe_allow_html=True)
    v1, v2 = st.columns(2)
    with v1:
        st.markdown("#### 👨‍🎓 Active Students View")
        st.code('db.createView("active_students_view","students",[{$lookup:{from:"submissions",localField:"_id",foreignField:"student_id",as:"subs"}},{$match:{"subs.0":{$exists:true}}},{$project:{name:1,email:1,totalSubs:{$size:"$subs"}}}])', language="javascript")
        if st.button("▶ Query View", key="v1"):
            r = list(get_collection("submissions").aggregate([{"$group":{"_id":"$student_id","totalSubs":{"$sum":1}}},{"$lookup":{"from":"students","localField":"_id","foreignField":"_id","as":"student"}},{"$unwind":"$student"},{"$project":{"name":"$student.name","email":"$student.email","totalSubs":1}},{"$sort":{"totalSubs":-1}},{"$limit":20}]))
            if r: st.dataframe(pd.DataFrame(r), use_container_width=True)
    with v2:
        st.markdown("#### 📊 Submission Summary View")
        st.code('db.createView("submission_summary","submissions",[{$group:{_id:"$assignment_id",avgMarks:{$avg:"$grade.marks"},count:{$sum:1}}},{$sort:{avgMarks:-1}}])', language="javascript")
        if st.button("▶ Query View", key="v2"):
            r = list(get_collection("submissions").aggregate([{"$group":{"_id":"$assignment_id","avgMarks":{"$avg":"$grade.marks"},"count":{"$sum":1}}},{"$sort":{"avgMarks":-1}},{"$limit":20}]))
            if r: st.dataframe(pd.DataFrame(r).rename(columns={"_id":"Assignment"}), use_container_width=True)

# ── Indexing ──
def indexing_page():
    st.subheader("⚡ Indexing & Query Optimization")
    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown("##### 🔗 Compound Index")
        st.code('db.assignments.createIndex({course_id:1, deadline:-1})')
        st.caption("Retrieves assignments sorted by deadline")
    with c2:
        st.markdown("##### 👈 Student ID Index")
        st.code('db.submissions.createIndex({student_id:1})')
        st.caption("Fast student submission lookups")
    with c3:
        st.markdown("##### 📄 Assignment ID Index")
        st.code('db.submissions.createIndex({assignment_id:1})')
        st.caption("Optimizes lookup operations")
    st.markdown("---")
    st.markdown("#### 🔍 explain() Demo")
    st.code('db.submissions.find({student_id:10}).explain("executionStats")')
    if st.button("▶ Run Explain", type="primary"):
        r = get_db().command("explain", {"find":"submissions","filter":{"student_id":10}}, verbosity="executionStats")
        st.json(r)
    st.markdown("---")
    st.markdown("#### 🌟 Optimization Techniques")
    oc1,oc2,oc3 = st.columns(3)
    with oc1:
        st.markdown("##### 🎯 Projection")
        st.code('db.students.find({dept:2},{name:1,email:1})')
        st.caption("Return only required fields")
    with oc2:
        st.markdown("##### 📄 Pagination")
        st.code('db.students.find().skip(10).limit(5)')
        st.caption("Load data in parts")
    with oc3:
        st.markdown("##### 🔀 Hybrid Modeling")
        st.code('Embedding: grade, feedback\nReferencing: student_id, course_id')
        st.caption("Best of both approaches")

# ── Main Router ──
p = page.split(" ", 1)[1] if " " in page else page
if p == "Dashboard": dashboard()
elif p == "Students": crud_page("students", COLLECTIONS["students"])
elif p == "Instructors": crud_page("instructors", COLLECTIONS["instructors"])
elif p == "Courses": crud_page("courses", COLLECTIONS["courses"])
elif p == "Assignments": crud_page("assignments", COLLECTIONS["assignments"])
elif p == "Submissions": crud_page("submissions", COLLECTIONS["submissions"])
elif p == "Departments": crud_page("departments", COLLECTIONS["departments"])
elif p == "Notifications": crud_page("notifications", COLLECTIONS["notifications"])
elif p == "Aggregations": aggregations_page()
elif p == "Transactions": transactions_page()
elif p == "Locking Demo": locking_page()
elif p == "Views": views_page()
elif p == "Indexing": indexing_page()
